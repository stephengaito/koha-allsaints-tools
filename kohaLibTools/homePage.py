
from nicegui import ui

from kohaLibTools.uiPage import UIPage
import kohaLibTools.theme as theme

class HomePage(UIPage) :

  def __init__(self) :
    super().__init__(
      '/',
      'Home Page',
      'Home Page'
    )

  def create(self) :
    print(f"Created {self.title}")
    @ui.page(self.route)
    def thePage() :
      print(f"Drawn {self.title}")
      with theme.frame(self.title) :
        ui.markdown("""
        ## Home page

        - [**Books Checked Out**](/booksCheckedOut) :
          Produces a report of the books currently checked out of the library.

        """)

theHomePage = HomePage()
