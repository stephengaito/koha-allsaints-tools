
from abc import ABC, abstractmethod
import weakref
import yaml

from nicegui import ui

class UIPage :
  instances = []

  @classmethod
  def getPages(cls) :
    return list(cls.instances)

  def __init__(self, route, title, toolTip) :
    self.route = route
    self.title = title
    self.toolTip = toolTip
    UIPage.instances.append(self)

  def title(self) :
    return self.title

  def route(self) :
    return self.route

  def toolTip(self) :
    return self.toolTip

  @abstractmethod
  def create(self) :
    pass