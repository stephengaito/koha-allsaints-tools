
from nicegui import ui

from kohaLibTools.uiPage import UIPage
import kohaLibTools.theme as theme

class ClassLists(UIPage) :

  def __init__(self) :
    super().__init__(
      '/classLists',
      'Class Lists',
      'Get a PDF of the bar codes for each child in a given class'
    )

  def create(self) :
    print(f"Created {self.title}")
    @ui.page(self.route)
    def thePage() :
      print(f"Drawn {self.title}")
      with theme.frame(self.title) :
        theme.message(self.title)
        ui.label(f"This is the {self.title} page")

theClassLists = ClassLists()
