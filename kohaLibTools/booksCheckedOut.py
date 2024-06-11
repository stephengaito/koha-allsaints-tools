
import csv
from datetime import date
import io
import yaml

import fastapi
import mariadb

from nicegui import app, ui

from kohaLibTools.uiPage import UIPage
import kohaLibTools.theme as theme

reportQuery = """
SELECT
 categories.description AS className,
 CONCAT(firstname, ' ', surname) AS pupilName,
 GROUP_CONCAT(biblio.title) AS bookTitle,
 DATE_FORMAT(issuedate, '%Y %b %e') AS dateIssued,
 DATEDIFF(CURDATE(), issuedate) DIV 7 AS weeksOut,
 DATE_FORMAT(date_due, '%Y %b %e') AS dateDue,
 DATEDIFF(CURDATE(), date_due) AS daysOverdue,
 borrowernumber AS borrowerNumber,
 biblionumber AS biblioNumber
FROM borrowers
JOIN issues USING (borrowernumber)
JOIN items USING (itemnumber)
JOIN biblio USING (biblionumber)
JOIN categories USING (categorycode)
GROUP BY categorycode,date_due,firstname,surname
"""

htmlHeader = """
<HTML>
<head>
 <title>Koha: Books checked out : Report</title>
</head>
<body>
<div id="doc3">

<table border=1>
  <thead>
    <tr>
      <th>Class Name</th>
      <th>Pupil Name</th>
      <th>Book Title</th>
      <th>Date Issued</th>
      <th>Weeks Out</th>
      <th>Date Due</th>
    </tr>
  </thead>

  <tbody>
"""

htmlRow = """
      <tr>
        <td>{className}</td>
        <td><a target="_blank" href="/cgi-bin/koha/members/moremember.pl?borrowernumber={borrowerNumber}">{pupilName}</a></td>
        <td><a target="_blank" href="/cgi-bin/koha/catalogue/detail.pl?biblionumber={biblioNumber}">{bookTitle}</a></td>
        <td>{dateIssued}</td>
        <td>{weeksOut}</td>
        <td><span [% IF 7 < daysOverdue %]style="color:red;font-weight:700"[% END %]>{dateDue}</span></td>
      </tr>
"""

htmlFooter = """
  </tbody>
</table>
</body>
</HTML>
"""

csvHeaders = [
  'className',
  'pupilName',
  'bookTitle',
  'dateIssued',
  'weeksOut',
  'dateDue',
  'daysOverdue',
  'borrowerNumber',
  'biblioNumber'
]

def convertRow(aRow) :
  theRowList = list(aRow)
  theRowDict = {}
  for aField in csvHeaders :
    theRowDict[aField] = theRowList.pop(0)
  return theRowDict

def getData() :
  config = {}
  try :
    with open('config.yaml') as configFile :
      config = yaml.safe_load(configFile.read())
  except Exception as err :
    print(repr(err))

  if not config : return []

  if 'password' not in config :
    print("CAN NOT connect to the Koha database without a password!!!")
    return []

  # NOTE: if host is specified as `localhost` then the socket is used
  # if host is specified as an IP address (`127.0.0.1`) the the port is used

  if 'database' not in config : config['database'] = 'koha_allsaints'
  if 'user'     not in config : config['user']     = 'koha_allsaints'
  if 'host'     not in config : config['host']     = '127.0.0.1'
  if 'port'     not in config : config['port']     = '3306'
  if not isinstance(config['port'], int) :
    config['port'] = int(config['port'])

  print("getting report data")
  db = mariadb.connect(**config)
  cursor = db.cursor()
  print(reportQuery)
  cursor.execute(reportQuery)
  result = cursor.fetchall()
  return result

@app.get('/booksCheckedOut/html')
def createHtml() :
  report = getData()
  print("Creating HTML table")
  htmlContent = [ htmlHeader ]
  for aRow in report :
    rowDict = convertRow(aRow)
    htmlContent.append(
      htmlRow.format(**rowDict)
    )
  htmlContent.append(htmlFooter)
  return fastapi.responses.HTMLResponse(
    content='\n'.join(htmlContent)
  )

@app.get('/booksCheckedOut/csv')
def createCsv() :
  fileName = date.today().strftime(
    'booksCheckedOut_%Y-%m-%d.csv'
  )
  report = getData()
  print(f"Creating CSV as {fileName}")
  csvFile = io.StringIO()
  csvWriter = csv.writer(csvFile, quoting=csv.QUOTE_ALL)
  csvWriter.writerow(csvHeaders)
  for aRow in report :
    csvWriter.writerow(aRow)
  csvContent = csvFile.getvalue()
  csvFile.close()
  return fastapi.responses.Response(
    content=csvContent,
    headers={
      'Content-Disposition': f'inline; filename="{fileName}"'
    },
    media_type='text/csv'
  )

@app.get('/booksCheckedOut/pdf')
def createPdf() :
  fileName = date.today().strftime(
    'booksCheckedOut_%Y-%m-%d.pdf'
  )
  report = getData()
  print(f"Creating PDF as {fileName}")
  return fastapi.responses.RedirectResponse(
    '/booksCheckedOut'
  )

class BooksCheckedOut(UIPage) :

  def __init__(self) :
    super().__init__(
      '/booksCheckedOut',
      'Books Checked Out',
      'Get a report of the books currently checked out'
    )

  def create(self) :
    print(f"Created {self.title}")
    @ui.page(self.route)
    def thePage() :
      print(f"Drawn {self.title}")
      with theme.frame(self.title) :
        #theme.message('Report format')
        ui.markdown("""
          ## Choose a report format :

          - [**Browser**](/booksCheckedOut/html) :
               display the list of books checked out in the browser
          - [**PDF File**](/booksCheckedOut/pdf) : download a PDF file suitable for printing
          - [**Spreadsheet (CSV) File**](/booksCheckedOut/csv) : download a CSV file suitable for loading into a spreadsheet
        """)

theBooksCheckedOut = BooksCheckedOut()
