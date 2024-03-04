from ._anvil_designer import view_loansTemplate
from anvil import *
import anvil.server
import anvil.google.auth, anvil.google.drive
from anvil.google.drive import app_files
import anvil.users
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
from .. import main_form_module as main_form_module

class view_loans(view_loansTemplate):
    def __init__(self, **properties):
        # Set Form properties and Data Bindings.
        self.init_components(**properties)
        self.user_id = main_form_module.userId

        # Fetch data based on loan status and user ID
        self.repeating_panel_6.items = app_tables.fin_loan_details.search(
            loan_updated_status=q.any_of(
                q.like('accept%'),
                q.like('Approved%'),
                q.like('approved%'),
                q.like('under process%'),
                q.like('foreclosure%'),
                #q.like('close%'),
                #q.like('Close%'),
                #q.like('closed loans%'),
                q.like('disbursed loan%'),
                q.like('Disbursed loan%'),
                q.like('Under Process%')
            ),
            borrower_customer_id=self.user_id
        )
        self.repeating_panel_7.items = app_tables.fin_loan_details.search(loan_updated_status=q.like('close%'), borrower_customer_id=self.user_id)
        self.repeating_panel_8.items = app_tables.fin_loan_details.search(loan_updated_status=q.like('reject%'), borrower_customer_id=self.user_id)
        self.repeating_panel_9.items = app_tables.fin_loan_details.search(loan_updated_status=q.like('under process%'), borrower_customer_id=self.user_id)
        self.repeating_panel_10.items = app_tables.fin_loan_details.search(loan_updated_status=q.like('foreclosure%'), borrower_customer_id=self.user_id)

        # Update label texts with the count of items in each repeating panel
        self.label_5.text = str(len(self.repeating_panel_6.items))
        self.label_6.text = str(len(self.repeating_panel_7.items))
        self.label_7.text = str(len(self.repeating_panel_8.items))
        self.label_8.text = str(len(self.repeating_panel_9.items))
        self.label_9.text = str(len(self.repeating_panel_10.items))

    def home_borrower_registration_form_copy_1_click(self, **event_args):
        """This method is called when the button is clicked"""
        open_form('borrower_registration_form.dashboard')

    def button_1_click(self, **event_args):
        """This method is called when the button is clicked"""
        self.label_1.visible = True
        self.label_2.visible = False
        self.label_3.visible = False
        self.label_4.visible = False
        self.label_10.visible = False
        #self.data_grid_1.visible = True
        # self.data_grid_2.visible = False
        # self.data_grid_3.visible = False
        # self.data_grid_4.visible = False
        # self.data_grid_5.visible = False
        self.repeating_panel_6.visible = True
        self.repeating_panel_7.visible = False
        self.repeating_panel_8.visible = False
        self.repeating_panel_9.visible = False
        self.repeating_panel_10.visible = False

    def button_2_click(self, **event_args):
        """This method is called when the button is clicked"""
        self.label_1.visible = False
        self.label_2.visible = True
        self.label_3.visible = False
        self.label_4.visible = False
        self.label_10.visible = False
        #self.data_grid_1.visible = False
        self.repeating_panel_6.visible = False
        self.repeating_panel_7.visible = True
        self.repeating_panel_8.visible = False
        self.repeating_panel_9.visible = False
        self.repeating_panel_10.visible = False 
      
        # self.data_grid_3.visible = False
        # self.data_grid_4.visible = False
        # self.data_grid_5.visible = False

    def button_3_click(self, **event_args):
        """This method is called when the button is clicked"""
        self.label_1.visible = False
        self.label_2.visible = False
        self.label_3.visible = True
        self.label_4.visible = False
        self.label_10.visible = False
        # self.data_grid_1.visible = False
        # self.data_grid_2.visible = False
        # self.data_grid_3.visible = True
        # self.data_grid_4.visible = False
        # self.data_grid_5.visible = False
        self.repeating_panel_6.visible = False
        self.repeating_panel_7.visible = False
        self.repeating_panel_8.visible = True
        self.repeating_panel_9.visible = False
        self.repeating_panel_10.visible = False

    def button_4_click(self, **event_args):
        """This method is called when the button is clicked"""
        self.label_1.visible = False
        self.label_2.visible = False
        self.label_3.visible = False
        self.label_4.visible = True
        self.label_10.visible = False
        # self.data_grid_1.visible = False
        # self.data_grid_2.visible = False
        # self.data_grid_3.visible = False
        # self.data_grid_4.visible = True
        # self.data_grid_5.visible = False
        self.repeating_panel_6.visible = False
        self.repeating_panel_7.visible = False
        self.repeating_panel_8.visible = False
        self.repeating_panel_9.visible = True
        self.repeating_panel_10.visible = False

    def button_5_click(self, **event_args):
        """This method is called when the button is clicked"""
        self.label_1.visible = False
        self.label_2.visible = False
        self.label_3.visible = False
        self.label_4.visible = False
        self.label_10.visible = True
        # self.data_grid_1.visible = False
        # self.data_grid_2.visible = False
        # self.data_grid_3.visible = False
        # self.data_grid_4.visible = False
        # self.data_grid_5.visible = True
        self.repeating_panel_6.visible = False
        self.repeating_panel_7.visible = False
        self.repeating_panel_8.visible = False
        self.repeating_panel_9.visible = False
        self.repeating_panel_10.visible = True