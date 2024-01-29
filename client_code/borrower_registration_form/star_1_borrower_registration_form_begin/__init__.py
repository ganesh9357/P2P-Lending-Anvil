from ._anvil_designer import star_1_borrower_registration_form_beginTemplate
from anvil import *
import anvil.server
import anvil.google.auth, anvil.google.drive
from anvil.google.drive import app_files
import anvil.users
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
from datetime import datetime,timedelta
import re
class star_1_borrower_registration_form_begin(star_1_borrower_registration_form_beginTemplate):
    def __init__(self, user_id, **properties):
        self.userId = user_id
        user_data=app_tables.fin_user_profile.get(customer_id=user_id)
        if user_data:
          self.borrower_full_name_test.text=user_data['full_name']
          self.borrower_date_of_birth_date_picker.date=user_data['date_of_birth']
          user_data.update()
          options = app_tables.fin_borrower_gender.search()
          option_strings = [str(option['borrower_gender']) for option in options]
          self.gender_dd.items = option_strings

        # Set the selected value in the dropdown if it matches the user's gender
          # if user_data and str(user_data['gender']) in option_strings:
          #   self.gender_dd.selected_value = str(user_data['gender'])
        self.init_components(**properties)
        
        
    def home_borrower_registration_form_click(self, **event_args):
        open_form('bank_users.user_form')

    def next_butto_for_step_2_click(self, **event_args):
        full_name = self.borrower_full_name_test.text
        gender = self.gender_dd.selected_value
        dob = self.borrower_date_of_birth_date_picker.date
        user_id = self.userId
        
        # Clear previous error messages
        self.full_name_label.text = ''
        self.dob_label.text = ''

        # Validate full name
        if not re.match(r'^[A-Za-z\s]+$', full_name):
            self.full_name_label.text = 'Enter a valid full name'
          
        elif not dob or dob > datetime.now().date():
            self.dob_label.text = 'Enter a valid date of birth'

        # Validate age (must be 18 or older)
        elif datetime.now().date() - dob < timedelta(days=365 * 18):
            self.dob_label.text = 'You must be at least 18 years old'
        elif not full_name or not gender or not dob:
            Notification('Please fill all details').show()
        else:
            anvil.server.call('add_borrower_step1', full_name, gender, dob, user_id)
            Notification("Step 1 form fill up submitted successfully")
            open_form('borrower_registration_form.star_1_borrower_registration_form_begin_2', user_id=user_id)
            row=app_tables.fin_user_profile.get(customer_id=user_id)
            if row:
              self.full_name_label.text=row['full_name']

    def borrower_full_name_test_change(self, **event_args):
        # This event is triggered when the text in the full name text box changes.
        # Check the format and hide the error label if the format is correct.
        full_name = self.borrower_full_name_test.text
        if re.match(r'^[A-Za-z\s]+$', full_name):
            self.full_name_label.text = ''
    
    def borrower_date_of_birth_date_picker_change(self, **event_args):
        # This event is triggered when the date in the date picker changes.
        # Check if the date is valid and hide the error label if it is correct.
        dob = self.borrower_date_of_birth_date_picker.date
        if not dob or dob > datetime.now().date():
            self.dob_label.text = ''



