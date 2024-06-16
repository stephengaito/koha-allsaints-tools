
from datetime import date
import io
import yaml

import fastapi
from fpdf import FPDF
from fpdf.fonts import FontFace
from fpdf.enums import TableCellFillMode
from fpdf.drawing import DeviceRGB

from nicegui import app, ui

from kohaLibTools.configuration import kohaConfig
from kohaLibTools.uiPage import UIPage
import kohaLibTools.theme as theme

from kohaLibTools.booksCheckedOut import columnHeaders, getData, convertRow

########################################################################
# PDF Configuration

overdueDays = 7
if 'overdueDays' in kohaConfig : overdueDays = kohaConfig['overdueDays']

numRowsPerPage  = 35
numRowsPerGroup = 5

# PDF configuration (in pixels)
#   setting for A4 landscape
#pdfWidth       = 842
#pdfHeight      = 595
pdfTopMargin   = 25
pdfLeftMargin  = 15
pdfLineSkip    = 15
pdfHRuleLength = 800

pdfOverdue     = '#FF0000'
pdfFontFamily  = 'helvetica'
pdfFontType    = 'B'
pdfFontSize    = 12

pdfBlack = DeviceRGB(0,0,0)
pdfWhite = DeviceRGB(1,1,1)
pdfGrey  = DeviceRGB(0.5,0.5,0.5)
pdfRed   = DeviceRGB(1,0,0)

#                 class, name, bookCode, title, issue, weeks, due
tableWidths    = [85,    150,  75,      250,   85,    75,    100]

columnNames = [
  'className', 'pupilName', 'bookCode', 'bookTitle',
  'dateIssued', 'weeksOut', 'dateDue'
]

columnHeaders = {
  'className'  : 'Class Name',
  'pupilName'  : 'Pupil Name',
  'bookCode'    : 'Book Code',
  'bookTitle'  : 'Book Title',
  'dateIssued' : 'Date Issued',
  'weeksOut'   : 'Weeks Out',
  'dateDue'    : 'Date Due'
}

pdfToday = date.today().strftime('%Y-%b-%d')

def truncateTextTo(someText, maxWidth) :
  someText = str(someText)
  return (someText[:maxWidth] + '..') if len(someText) > maxWidth else someText

class PDF(FPDF) :
  ########################################################################
  # PDF local subroutines

  def __init__(self) :
    super().__init__(orientation="landscape", unit="pt", format="A4")
    self.set_top_margin(pdfTopMargin)
    self.set_left_margin(pdfLeftMargin)
    self.set_font(pdfFontFamily, pdfFontType, pdfFontSize)
    self.lastClass    = ""
    self.curClass     = "unknown"
    self.classPageNum = 1
    self.curRow       = 0
    curX = pdfLeftMargin
    self.tableX = {}
    for colNum in range(len(tableWidths)) :
      self.tableX[columnNames[colNum]] = curX
      curX += tableWidths[colNum]

  def header(self) :
    self.set_xy(pdfLeftMargin, pdfTopMargin)
    self.set_text_color(pdfBlack)
    self.text(
      x=pdfLeftMargin, y = pdfTopMargin,
      text=self.curClass
    )
    self.set_text_color(pdfGrey)
    self.text(
      x=pdfLeftMargin+ tableWidths[0], y = pdfTopMargin,
      text=f"{pdfToday} ; page {self.classPageNum}"
    )
    self.set_text_color(pdfBlack)

    self.newLine(scale=1.5)
    for colName in columnNames :
      self.text(
        x=self.tableX[colName], y = self.get_y(),
        text=columnHeaders[colName]
      )
    self.newLine()
    self.newLine(scale=0.5)
    self.classPageNum += 1

  def addNewPageIfNeeded(self, curClass) :
    self.curClass = curClass
    if (self.curClass != self.lastClass) or (numRowsPerPage <= self.curRow) :
      if (self.curClass != self.lastClass) : self.classPageNum = 1
      self.add_page()
      self.curRow = 0
      self.lastClass = self.curClass

  def newLine(self, scale=1.0) :
    self.ln(h=pdfLineSkip*scale)
    self.curRow += 1
    if self.curRow % numRowsPerGroup == 0 :
      self.addHRule(lineColor=pdfGrey)
      self.ln(h=pdfLineSkip*0.5)

  def addHRule(self, lineColor=pdfBlack) :
    x = self.get_x()
    y = self.get_y()
    self.set_draw_color(lineColor)
    self.line(x, y-9, x+pdfHRuleLength, y-9)

@app.get('/booksCheckedOut/pdf')
def createPdf() :
  fileName = date.today().strftime(
    'booksCheckedOut_%Y-%m-%d.pdf'
  )
  report = getData()
  print(f"Creating PDF as {fileName}")
  pdf = PDF()

  pdf.lastClass    = ""
  pdf.curClass     = "unknown"
  pdf.classPageNum = 1
  pdf.curRow       = 0

  for aRow in report :
    aRowDict = convertRow(aRow)
    pdf.addNewPageIfNeeded(aRowDict['className'])
    for colName in columnNames :
      if colName == 'dateDue' and overdueDays < aRowDict['daysOverdue'] :
        pdf.set_text_color(pdfRed)
      else :
        pdf.set_text_color(pdfBlack)
      pdf.text(
        x = pdf.tableX[colName], y = pdf.get_y(),
        text=truncateTextTo(aRowDict[colName], 40)
      )
    pdf.newLine()

  return fastapi.responses.Response(
    content=bytes(pdf.output()),
    headers={
      'Content-Disposition': f'inline; filename="{fileName}"'
    },
    media_type='application/pdf'
  )
