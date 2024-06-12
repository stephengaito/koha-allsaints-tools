
import fastapi

from nicegui import app, ui

from kohaLibTools.configuration import kohaConfig
from kohaLibTools.booksCheckedOut import getData, convertRow
import kohaLibTools.theme as theme

overdueDays = 7
if 'overdueDays' in kohaConfig : overdueDays = kohaConfig['overdueDays']

htmlTableHeader = """
    <tr>
      <th style="text-align:start">Class Name</th>
      <th style="text-align:start">Pupil Name</th>
      <th style="text-align:start">Bar Code</th>
      <th style="text-align:start">Book Title</th>
      <th style="text-align:start">Date Issued</th>
      <th style="text-align:start">Weeks Out</th>
      <th style="text-align:start">Date Due</th>
    </tr>
"""

htmlHeader = f"""
<HTML>
<head>
 <title>Koha: Books checked out : Report</title>
</head>
<body>
<div id="doc3">

<table border=1>
  <!--thead>
{htmlTableHeader}
  </thead -->

  <tbody>
"""
#      <th>Days overdue</th>

htmlRow = """
      <tr>
        <td>{className}</td>
        <td><a style="color:blue" target="_blank" href="{baseUrl}/cgi-bin/koha/members/moremember.pl?borrowernumber={borrowerNumber}">{pupilName}</a></td>
        <td><a style="color:blue" target="_blank" href="{baseUrl}/cgi-bin/koha/catalogue/detail.pl?biblionumber={biblioNumber}">{barCode}</a></td>
        <td><a style="color:blue" target="_blank" href="{baseUrl}/cgi-bin/koha/catalogue/detail.pl?biblionumber={biblioNumber}">{bookTitle}</a></td>
        <td>{dateIssued}</td>
        <td>{weeksOut}</td>
        <td><span {htmlColor}>{dateDue}</span></td>
      </tr>
"""
#        <td>{daysOverdue}</td>

htmlFooter = """
  </tbody>
</table>
</body>
</HTML>
"""

@ui.page('/booksCheckedOut/html')
def createHtml() :
  report = getData()
  print("Creating HTML table")
  htmlContent = [ htmlHeader ]
  lastClass = ""
  for aRow in report :
    rowDict = convertRow(aRow)
    if lastClass != rowDict['className'] :
      htmlContent.append(htmlTableHeader)
      lastClass = rowDict['className']
    rowDict['htmlColor'] = ''
    if overdueDays < rowDict['daysOverdue'] :
      rowDict['htmlColor'] = 'style="color:red;font-weight:700"'
    rowDict['baseUrl'] = kohaConfig['baseUrl']
    htmlContent.append(
      htmlRow.format(**rowDict)
    )
  htmlContent.append(htmlFooter)
  with theme.frame('Books Checked Out : Browser') :
    ui.html('\n'.join(htmlContent))

