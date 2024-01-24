from ._anvil_designer import ItemTemplate4Template
from anvil import *
import anvil.server
import anvil.google.auth, anvil.google.drive
from anvil.google.drive import app_files
import anvil.users
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables

class ItemTemplate4(ItemTemplate4Template):
  def __init__(self, **properties):
    # Set Form properties and Data Bindings.
    self.init_components(**properties)
    self.data_row = None  # Keep track of the data row associated with this item
    self.edit_mode = False

    # Any code you write here will run before the form opens.


  def merrital_button_click(self, **event_args):
    """This method is called when the button is clicked"""
    if not self.edit_mode:
            # If not in edit mode, enter edit mode
            self.edit_mode = True
            self.original_data = self.text_box_1.text
    else:
            # If already in edit mode, save the changes
            edited_data = self.text_box_1.text
            self.original_data = None
            self.edit_mode = False
            Notification("Data saved successfully")

  def delete_button_copy_click(self, **event_args):
    """This method is called when the button is clicked"""
    if self.original_data:
            # If in edit mode, cancel editing and do not delete
            self.text_box_1.text = self.original_data
            self.original_data = None
            self.edit_mode = False
    else:
            # If not in edit mode, delete the data
            self.raise_event('delete_row', data=self.text_box_1.text)
