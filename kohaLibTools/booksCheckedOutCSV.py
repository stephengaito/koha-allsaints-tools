
import csv
from datetime import date
import io

import fastapi

from nicegui import app, ui

from kohaLibTools.configuration import config
from kohaLibTools.uiPage import UIPage
import kohaLibTools.theme as theme

from kohaLibTools.booksCheckedOut import columnHeaders, getData

@app.get('/booksCheckedOut/csv')
def createCsv() :
  fileName = date.today().strftime(
    'booksCheckedOut_%Y-%m-%d.csv'
  )
  report = getData()
  print(f"Creating CSV as {fileName}")
  csvFile = io.StringIO()
  csvWriter = csv.writer(csvFile, quoting=csv.QUOTE_ALL)
  csvWriter.writerow(columnHeaders)
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
