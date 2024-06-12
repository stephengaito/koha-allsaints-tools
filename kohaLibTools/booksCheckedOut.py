
import csv
from datetime import date
import io
import yaml

import fastapi
import mariadb

from nicegui import app, ui

from kohaLibTools.configuration import dbConfig, kohaConfig
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
 barcode AS barCode,
 biblionumber AS biblioNumber
FROM borrowers
JOIN issues USING (borrowernumber)
JOIN items USING (itemnumber)
JOIN biblio USING (biblionumber)
JOIN categories USING (categorycode)
GROUP BY categorycode,date_due,firstname,surname
"""

columnHeaders = [
  'className',
  'pupilName',
  'bookTitle',
  'dateIssued',
  'weeksOut',
  'dateDue',
  'daysOverdue',
  'borrowerNumber',
  'barCode',
  'biblioNumber'
]

def convertRow(aRow) :
  theRowList = list(aRow)
  theRowDict = {}
  for aField in columnHeaders :
    theRowDict[aField] = theRowList.pop(0)
  return theRowDict

def getData() :
  if not dbConfig : return []

  if 'password' not in dbConfig :
    print("CAN NOT connect to the Koha database without a password!!!")
    return []

  # NOTE: if host is specified as `localhost` then the socket is used
  # if host is specified as an IP address (`127.0.0.1`) the the port is used

  if 'database' not in dbConfig : dbConfig['database'] = 'koha_allsaints'
  if 'user'     not in dbConfig : dbConfig['user']     = 'koha_allsaints'
  if 'host'     not in dbConfig : dbConfig['host']     = '127.0.0.1'
  if 'port'     not in dbConfig : dbConfig['port']     = '3306'
  if not isinstance(dbConfig['port'], int) :
    dbConfig['port'] = int(dbConfig['port'])

  print("getting report data")
  db = mariadb.connect(**dbConfig)
  cursor = db.cursor()
  #print(reportQuery)
  cursor.execute(reportQuery)
  result = cursor.fetchall()
  return result

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
