from ._anvil_designer import star_1_borrower_registration_form_begin_3dTemplate
from anvil import *
import anvil.server
import anvil.google.auth, anvil.google.drive
from anvil.google.drive import app_files
import anvil.users
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables

class star_1_borrower_registration_form_begin_3d(star_1_borrower_registration_form_begin_3dTemplate):
  def __init__(self,user_id, **properties):
    self.userId = user_id
    user_data=app_tables.fin_user_profile.get(customer_id=user_id)
    if user_data:
      self.text_box_1.text=user_data['company_name']
      self.drop_down_1.selected_value=user_data['employment_type']
      self.drop_down_2.selected_value=user_data['organization_type']
      user_data.update()

    options_1 = app_tables.fin_borrower_employee_type.search()
    option_strings_1 = [str(option['borrower_employee_type']) for option in options_1]
    self.drop_down_1.items = option_strings_1

        # Populate drop_down_2 with data from 'organization_type' column
    options_2 = app_tables.fin_borrower_organization_type.search()
    option_strings_2 = [str(option['borrower_organization_type']) for option in options_2]
    self.drop_down_2.items = option_strings_2
    # Set Form properties and Data Bindings.
    self.init_components(**properties)


  def button_2_click(self, **event_args):
    emp_type = self.drop_down_1.selected_value
    org_type = self.drop_down_2.selected_value
    company_name = self.text_box_1.text
    user_id = self.userId
    if not emp_type or not org_type or not company_name:
      Notification("please fill the required fields ").show()
    else:
      anvil.server.call('add_lendor_individual_form_1', company_name,org_type,emp_type,user_id)
      open_form('borrower_registration_form.star_1_borrower_registration_form_begin_3.star_1_borrower_registration_form_begin_3e',user_id=self.userId)




  # this is prev button
  def button_1_click(self, **event_args):
    open_form('borrower_registration_form.star_1_borrower_registration_form_begin_3.star_1_borrower_registration_form_begin_3c',user_id=self.userId)


  def button_3_click(self, **event_args):
    open_form("bank_users.user_form")
