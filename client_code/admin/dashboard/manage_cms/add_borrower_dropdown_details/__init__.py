from ._anvil_designer import add_borrower_dropdown_detailsTemplate
from anvil import *
import anvil.server
import anvil.google.auth, anvil.google.drive
from anvil.google.drive import app_files
import anvil.users
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables

class add_borrower_dropdown_details(add_borrower_dropdown_detailsTemplate):
  def __init__(self, **properties):
    # Set Form properties and Data Bindings.
    self.init_components(**properties)
    self.refresh()


    # Any code you write here will run before the form opens.

  def gender_button_click(self, **event_args):
    """This method is called when the button is clicked"""
    entered_data = self.text_box_1.text
    new_row = app_tables.fin_borrower_gender.add_row(borrower_gender=entered_data)
    self.refresh()

  def refresh(self):
        """Refresh repeating panels with the latest data"""
        self.repeating_panel_1.items = app_tables.fin_borrower_gender.search()
        self.repeating_panel_2.items = app_tables.fin_borrower_marrital_status.search()

  def marital_button_click(self, **event_args):
    """This method is called when the button is clicked"""
    entered_data = self.text_box_2.text
    new_row = app_tables.fin_borrower_marrital_status.add_row(borrower_marrital_status=entered_data)
    self.refresh()
