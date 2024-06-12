
from contextlib import contextmanager

from nicegui import ui

from kohaLibTools.uiPage import UIPage

class message(ui.label):

    def __init__(self, text: str) -> None:
        super().__init__(text)
        self.classes('text-h4 text-grey-8')

def menu() -> None:
  for aPage in UIPage.getPages() :
    ui.link(
      aPage.title, aPage.route
    ).classes(
      replace='text-white'
    ).tooltip(
      aPage.toolTip
    )

@contextmanager
def frame(navigation_title: str):
  """Custom page frame to share the same styling and behavior across all pages"""
  ui.page_title(navigation_title)
  ui.colors(primary='#6E93D6', secondary='#53B689', accent='#111B1E', positive='#53B689')
  with ui.header():
    #ui.button(
    #  on_click=lambda: left_drawer.toggle(), icon='menu'
    #).props('flat color=white')
    ui.label(
      'All Saints Koha Library Tools'
    ).classes('font-bold')
    ui.space()
    ui.label(navigation_title)
    ui.space()
    with ui.row():
      menu()

  #with ui.footer(value=False) as footer :
  #  ui.label('Footer')

  #with ui.left_drawer().classes('bg-blue-100') as left_drawer :
  #  ui.label('Side menu')
  #  with ui.column() :
  #    menu()

  #with ui.page_sticky(position='bottom-right', x_offset=20, y_offset=20) :
  #  ui.button(
  #    on_click=footer.toggle, icon='contact_support'
  #  ).props('fab')

  #with ui.column().classes('absolute-center items-center'):
  with ui.column().classes('items-center'):
    yield
