from ._anvil_designer import today_duesTemplate
from anvil import *
import anvil.server
import anvil.google.auth, anvil.google.drive
from anvil.google.drive import app_files
import anvil.users
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
from datetime import datetime, timedelta, timezone
from .. import main_form_module as main_form_module

class today_dues(today_duesTemplate):
    def __init__(self, **properties):
        self.user_id = main_form_module.userId
        # Set Form properties and Data Bindings.
        self.init_components(**properties)
        
        # Fetch all loan details
        all_loans = app_tables.fin_loan_details.search(
            loan_updated_status=q.like('%accept%')
        )
        
        # Calculate days left and days gone for each loan
        for loan in all_loans:
            due_date = loan['emi_due_date']

            # Check if due_date is not None before processing
            if due_date is not None:
                now = datetime.now(timezone.utc)
                due_date_aware = datetime.combine(due_date, datetime.min.time()).replace(tzinfo=timezone.utc)
                
                days_left = (due_date_aware - now).days
                days_gone = (now - due_date_aware).days

                # Update the 'days_positive' and 'days_negative' columns in the database
                loan['days_left'] = max(0, days_left) 
                loan['days_gone'] = max(0, days_gone) * -1 
                loan.update()

        # Display loans with the calculated values in the repeating panel
        self.repeating_panel_1.items = all_loans

    def home_borrower_registration_form_copy_1_click(self, **event_args):
        """This method is called when the button is clicked"""
        open_form('borrower_registration_form.dashboard')
