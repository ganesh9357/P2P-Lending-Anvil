from ._anvil_designer import ItemTemplate3Template
from anvil import *
import anvil.server
import anvil.google.auth, anvil.google.drive
from anvil.google.drive import app_files
import anvil.users
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables

class ItemTemplate3(ItemTemplate3Template):
  def __init__(self, **properties):
    # Set Form properties and Data Bindings.
    self.init_components(**properties)
    self.data_row = None  # Keep track of the data row associated with this item
    self.edit_mode = False
    # Any code you write here will run before the form opens.

  def gender_button_click(self, **event_args):
    """This method is called when the button is clicked"""
    if self.edit_mode:
            # If already in edit mode, save the changes
            edited_data = self.text_box_data.text
            self.data_row['data_column'] = edited_data
            self.edit_mode = False
            Notification("Data saved successfully")
    else:
            # If not in edit mode, enter edit mode
            self.edit_mode = True

  def gender_button_copy_click(self, **event_args):
    """This method is called when the button is clicked"""
    if self.data_row:
            # Delete the data row from the database
            self.data_row.delete()
            self.data_row = None  # Clear the data_row after deleting
            self.edit_mode = False
            Notification("Data deleted successfully")
