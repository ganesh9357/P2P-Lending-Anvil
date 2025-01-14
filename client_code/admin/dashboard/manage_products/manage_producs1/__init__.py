# from ._anvil_designer import manage_producs1Template
# from anvil import *
# import anvil.server
# import anvil.google.auth, anvil.google.drive
# from anvil.google.drive import app_files
# import anvil.users
# import anvil.tables as tables
# import anvil.tables.query as q
# from anvil.tables import app_tables
# import json

# class manage_producs1(manage_producs1Template):
#     def __init__(self, **properties):
#         # Set Form properties and Data Bindings.
#         self.init_components(**properties)

#         options = app_tables.fin_product_group.search()
#         option_strings = [option['name'] for option in options]
#         self.name.items = option_strings
#         self.name.selected_value = None

#         # Any code you write here will run before the form opens.
#         self.id = 'PD' + str(1000)
#         self.label_1.text = self.id
#         self.data = tables.app_tables.fin_product_details.search()

#         a = -1
#         self.list_1 = []

#         for i in self.data:
#             a += 1
#             self.list_1.append(i['product_id'])
#         if a == -1:
#             self.id = 'PD' + str(1000)
#             self.label_1.text = self.id
#         else:
#             last_product_id = self.list_1[-1]
#             numeric_part = last_product_id[2:]  # Assuming the prefix is always two characters ('PD')
#             self.id = 'PD' + str(int(numeric_part) + 1)
#             self.label_1.text = self.id

#     def name_change(self, **event_args):
#         self.label_3_copy.visible = True
#         self.label_5.visible = True
#         self.name.visible = True
#         self.product_category.visible = True
#         self.selected_value = self.name.selected_value
#         print(f"Selected Value: {self.selected_value}")

#         if self.selected_value:
#             # Fetch product categories based on the selected loan type
#             product_categories = app_tables.fin_product_categories.search(
#                 name_group=self.selected_value
#             )
#             print(f"Product Categories: {product_categories}")

#             if product_categories:
#                 # Display product categories in drop_down_2
#                 category_names = [category['name_categories'] for category in product_categories]
#                 print(f"Category Names: {category_names}")

#                 # Insert a placeholder or default value at the beginning
#                 # category_names.insert(0, "Select a Category")
#                 self.product_category.items = category_names
#                 self.product_category.selected_value = category_names[0] if category_names else None

#     def foreclose_type_change(self, **event_args):
#         """This method is called when an item is selected"""
#         selected_value = self.foreclose_type.selected_value
#         if selected_value == "Eligible":
#             self.label_9.visible = True
#             self.foreclosure_fee.visible = True
#             self.label_11.visible = True
#             self.min_months.visible = True
#         else:
#             self.label_9.visible = False
#             self.foreclosure_fee.visible = False
#             self.label_11.visible = False
#             self.min_months.visible = False

#     def extension_allowed_change(self, **event_args):
#         """This method is called when an item is selected"""
#         selected_value = self.extension_allowed.selected_value
#         if selected_value == "Yes":
#             self.label_7_copy.visible = True
#             self.text_box_4.visible = True
#         else:
#             self.label_7_copy.visible = False
#             self.text_box_4.visible = False

#     def button_1_click(self, **event_args):
#         """This method is called when the button is clicked"""
#         product_name = self.product_name.text
#         product_group = self.name.selected_value
#         product_discription = self.text_area_1.text
#         product_categories = self.product_category.selected_value
#         processing_fee = int(self.text_box_3.text)
#         membership_type = self.drop_down_2.selected_value
#         if self.radio_button_1.selected:
#             interest_type = self.radio_button_1.text
#         else:
#             interest_type = self.radio_button_2.text

#         min_amount = int(self.min_amount.text)
#         max_amount = int(self.max_amount.text)
#         min_tenure = int(self.min_tenure.text)
#         max_tenure = int(self.max_tenure.text)
#         roi = int(self.text_box_5.text)
#         foreclose_type = str(self.foreclose_type.selected_value)
#         foreclosure_fee = 0
#         min_months = 0
#         if foreclose_type == "Eligible":
#             self.label_9.hidden = False
#             self.foreclosure_fee.hidden = False
#             # Assign a value to foreclosure_fee based on your logic
#             foreclosure_fee = int(self.foreclosure_fee.text)
#             min_months = int(self.min_months.text)
#         else:
#             self.label_9.hidden = True
#             self.foreclosure_fee.hidden = True

#         extension_allowed = self.extension_allowed.selected_value
#         extension_fee = 0
#         if extension_allowed == "Yes":
#             self.label_7_copy.visible = True
#             self.text_box_4.visible = True
#             extension_fee = int(self.text_box_4.text)
#         else:
#             self.label_7_copy.visible = False
#             self.text_box_4.visible = False

#         emi_payment = [
#             "Monthly" if self.monthly.checked else "",
#             "One Time" if self.one_time.checked else "",
#             "Three Month" if self.three_month.checked else "",
#             "Six Month" if self.six_month.checked else "",
#         ]
#         emi_payment = json.dumps(emi_payment)

#         if self.radio_button_3.selected:
#             # Code to execute when radio_button_3 is selected
#             discount_coupons = self.radio_button_3.text
#         elif self.radio_button_4.selected:
#             # Code to execute when radio_button_4 is selected
#             discount_coupons = self.radio_button_4.text
#         else:
#             # Code to execute when neither radio_button_3 nor radio_button_4 is selected
#             discount_coupons = None
#         lapsed_fee = int(self.lapsed_fee.text)
#         default_fee = int(self.default_fee.text)
#         npa = int(self.npa.text)

#         existing_product = app_tables.fin_product_details.get(
#             product_name=product_name,
#             product_categories=product_categories
#         )

#         if existing_product:
#             Notification("Product with the same name and category already exists").show()
#             return

#         anvil.server.call('product_details', self.id, product_name, product_group, product_discription,
#                           product_categories, processing_fee, extension_fee, membership_type, interest_type, max_amount,
#                           min_amount, min_tenure, max_tenure, roi, foreclose_type, foreclosure_fee, extension_allowed,
#                           emi_payment, min_months, discount_coupons, lapsed_fee, default_fee, npa)
#         product_id = self.label_1.text
#         Notification("Products added successfully").show()
#         open_form('admin.dashboard.manage_products')

#     # def link_1_copy_click(self, **event_args):
#     #     """This method is called when the link is clicked"""
#     #     open_form('admin.dashboard.manage_products')

#     def button_1_copy_3_click(self, **event_args):
#       """This method is called when the button is clicked"""
#       open_form('admin.dashboard.manage_products')

#     def text_box_1_copy_pressed_enter(self, **event_args):
#       """This method is called when the user presses Enter in this text box"""
#       pass


from ._anvil_designer import manage_producs1Template
from anvil import *
import anvil.server
import anvil.google.auth, anvil.google.drive
from anvil.google.drive import app_files
import anvil.users
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
import json

class manage_producs1(manage_producs1Template):
    def __init__(self, **properties):
        # Set Form properties and Data Bindings.
        self.init_components(**properties)
        self.occupation = []
        self.emi_payment = []
      
        options = app_tables.fin_product_group.search()
        option_strings = [option['name'] for option in options]
        self.name.items = option_strings
        self.name.selected_value = None

        # Any code you write here will run before the form opens.
        self.id = 'PD' + str(1000)
        self.label_1.text = self.id
        self.data = tables.app_tables.fin_product_details.search()

        a = -1
        self.list_1 = []

        for i in self.data:
            a += 1
            self.list_1.append(i['product_id'])
        if a == -1:
            self.id = 'PD' + str(1000)
            self.label_1.text = self.id
        else:
            last_product_id = self.list_1[-1]
            numeric_part = last_product_id[2:]  # Assuming the prefix is always two characters ('PD')
            self.id = 'PD' + str(int(numeric_part) + 1)
            self.label_1.text = self.id

    def name_change(self, **event_args):
        self.label_3_copy.visible = True
        self.label_5.visible = True
        self.name.visible = True
        self.product_category.visible = True
        self.selected_value = self.name.selected_value
        print(f"Selected Value: {self.selected_value}")

        if self.selected_value:
            # Fetch product categories based on the selected loan type
            product_categories = app_tables.fin_product_categories.search(
                name_group=self.selected_value
            )
            print(f"Product Categories: {product_categories}")

            if product_categories:
                # Display product categories in drop_down_2
                category_names = [category['name_categories'] for category in product_categories]
                print(f"Category Names: {category_names}")

                # Insert a placeholder or default value at the beginning
                # category_names.insert(0, "Select a Category")
                self.product_category.items = category_names
                self.product_category.selected_value = category_names[0] if category_names else None

    def foreclose_type_change(self, **event_args):
        """This method is called when an item is selected"""
        selected_value = self.foreclose_type.selected_value
        if selected_value == "Eligible":
            self.label_9.visible = True
            self.foreclosure_fee.visible = True
            self.label_11.visible = True
            self.min_months.visible = True
        else:
            self.label_9.visible = False
            self.foreclosure_fee.visible = False
            self.label_11.visible = False
            self.min_months.visible = False

    def extension_allowed_change(self, **event_args):
        """This method is called when an item is selected"""
        selected_value = self.extension_allowed.selected_value
        if selected_value == "Yes":
            self.label_7_copy.visible = True
            self.text_box_4.visible = True
        else:
            self.label_7_copy.visible = False
            self.text_box_4.visible = False

    def button_1_click(self, **event_args):
        """This method is called when the button is clicked"""
        if not all([self.product_name.text.strip(),
                self.name.selected_value,
                self.product_category.selected_value,
                self.text_box_3.text.strip(),
                self.drop_down_2.selected_value,
                (self.radio_button_1.selected or self.radio_button_2.selected),
                self.min_amount.text.strip(),
                self.max_amount.text.strip(),
                self.min_tenure.text.strip(),
                self.max_tenure.text.strip(),
                self.text_box_5.text.strip(),
                self.foreclose_type.selected_value,
                self.extension_allowed.selected_value,
                (self.button_1_1.enabled or self.button_2_1.enabled or self.button_3_1.enabled or self.button_4_1.enabled),
                (self.business.enabled or self.student.enabled or self.student.enabled ),
                
                self.lapsed_fee.text.strip(),
                self.default_fee.text.strip(),
                self.npa.text.strip()]):
                
            Notification("Please fill in all the details").show()
            return
        # Retrieve and validate input values
        try:
            processing_fee = int(self.text_box_3.text.strip())
            min_amount = int(self.min_amount.text.strip())
            max_amount = int(self.max_amount.text.strip())
            min_tenure = int(self.min_tenure.text.strip())
            max_tenure = int(self.max_tenure.text.strip())
            roi = int(self.text_box_5.text.strip())
            lapsed_fee = int(self.lapsed_fee.text.strip())
            default_fee = int(self.default_fee.text.strip())
            npa = int(self.npa.text.strip())
    
            # Validate non-negative values
            if processing_fee < 0 or min_amount < 0 or max_amount < 0 or min_tenure < 0 or max_tenure < 0 or roi < 0 or lapsed_fee < 0 or default_fee < 0 or npa < 0:
                raise ValueError("Values cannot be negative")
    
        except ValueError:
            Notification("Please enter valid integer values").show()
            return
    
        # Process the rest of the code if all validations pass
        product_name = self.product_name.text
        product_group = self.name.selected_value
        product_discription = self.text_area_1.text
        product_categories = self.product_category.selected_value
    
        membership_type = self.drop_down_2.selected_value
        interest_type = self.radio_button_1.text if self.radio_button_1.selected else self.radio_button_2.text
    
        foreclose_type = str(self.foreclose_type.selected_value)
        foreclosure_fee = int(self.foreclosure_fee.text.strip()) if foreclose_type == "Eligible" else 0
        min_months = int(self.min_months.text.strip()) if foreclose_type == "Eligible" else 0
    
        extension_allowed = self.extension_allowed.selected_value
        extension_fee = int(self.text_box_4.text.strip()) if extension_allowed == "Yes" else 0

      
      #   emi_payment = [
      #       "Monthly" if self.button_1_1.enabled else "",
      #       "One Time" if self.button_2_1.enabled else "",
      #       "Three Month" if self.button_3_1.enabled else "",
      #       "Six Month" if self.button_4_1.enabled else "",
      # ]
      #   emi_payment = json.dumps(emi_payment)


        emi_payment = self.emi_payment
        emi_payment = ', '.join(emi_payment)

        occupation = self.occupation
        occupation = ', '.join(occupation)
      
        existing_product = app_tables.fin_product_details.get(
            product_name=product_name,
            product_categories=product_categories
        )
    
        if existing_product:
            Notification("Product with the same name and category already exists").show()
            return
    
        # Call the server function to add product details
        anvil.server.call('product_details', self.id, product_name, product_group, product_discription,
                          product_categories, processing_fee, extension_fee, membership_type, interest_type, max_amount,
                          min_amount, min_tenure, max_tenure, roi, foreclose_type, foreclosure_fee, extension_allowed,
                          emi_payment, min_months, lapsed_fee, default_fee, npa,occupation)
    
        # Update product ID and show success notification
        product_id = self.label_1.text
        Notification("Products added successfully").show()
        open_form('admin.dashboard.manage_products')


    # def link_1_copy_click(self, **event_args):
    #     """This method is called when the link is clicked"""
    #     open_form('admin.dashboard.manage_products')

    def button_1_copy_3_click(self, **event_args):
      """This method is called when the button is clicked"""
      open_form('admin.dashboard.manage_products')

    def text_box_1_copy_pressed_enter(self, **event_args):
      """This method is called when the user presses Enter in this text box"""
      pass

    def button_2_click(self, **event_args):
      """This method is called when the button is clicked"""
      open_form("admin.dashboard")


      


    def button_1_1_click(self, **event_args):
      """This method is called when the button is clicked"""
      self.button_1_1.background = "#0770e8"
      self.emi_payment.append("One Time")

    def button_2_1_click(self, **event_args):
      """This method is called when the button is clicked"""
      self.button_2_1.background = "#0770e8" 
      self.emi_payment.append("Monthly")

    def button_3_1_click(self, **event_args):
      """This method is called when the button is clicked"""
      self.button_3_1.background = "#0770e8" 
      self.emi_payment.append("Three Months")

    def button_4_1_click(self, **event_args):
      """This method is called when the button is clicked"""
      self.button_4_1.background = "#0770e8"
      self.emi_payment.append("Six Months")


  
    def business_click(self, **event_args):
      """This method is called when the button is clicked"""
      self.business.background = "#0770e8" #if self.business.enabled else "#FFFFFF"
      self.occupation.append("Business")

    def student_click(self, **event_args):
      """This method is called when the button is clicked"""
      self.student.background = "#0770e8" #if self.student.enabled else "#FFFFFF"
      self.occupation.append("Student")

    def employee_click(self, **event_args):
      """This method is called when the button is clicked"""
      self.employee.background = "#0770e8" #if self.employee.enabled else "#FFFFFF"
      self.occupation.append("Employee")

