
from nicegui import ui

from kohaLibTools.uiPage import UIPage
import kohaLibTools.theme as theme

class BookBarCodes(UIPage) :

  def __init__(self) :
    super().__init__(
      '/bookBarCodes',
      'Book Bar Codes',
      'Get a PDF of a collection of book bar codes'
    )

  def create(self) :
    print(f"Created {self.title}")
    @ui.page(self.route)
    def thePage() :
      print(f"Drawn {self.title}")
      with theme.frame(self.title) :
        theme.message(self.title)
        ui.label(f"This is the {self.title} page")

theBookBarCodes = BookBarCodes()
