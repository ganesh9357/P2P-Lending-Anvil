import anvil.secrets
import anvil.email
import anvil.google.auth, anvil.google.drive, anvil.google.mail
from anvil.google.drive import app_files
import anvil.users
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
import anvil.server
from datetime import datetime 
from datetime import datetime, timezone


@anvil.server.callable
def fetch_user_profile(email):
    user_profile = app_tables.fin_user_profile.get(email_user=email)
    return user_profile


  
@anvil.server.callable
def fetch_profile_data_and_insert(email, customer_id):
    try:
        # Fetch user profile based on customer_id
        profile = app_tables.fin_user_profile.get(email_user=email)
        
        if profile is not None:
            # Fetch wallet data based on customer_id
            wallet_data = app_tables.fin_wallet.get(user_email=email)
            
            if wallet_data is not None:
                wallet_id = wallet_data['wallet_id']
                account_id = wallet_data['account_id']
                
                # Check if account_number is a string before converting to number
                account_number_value = int(profile['account_number']) if isinstance(profile['account_number'], str) else profile['account_number']
                
                # Check if a row with the same user_email already exists in wallet_bank_account_table
                existing_row = app_tables.fin_wallet_bank_account_table.get(user_email=profile['email_user'])
                
                if existing_row is None:
                    # Add a new row to wallet_bank_account_table
                    app_tables.fin_wallet_bank_account_table.add_row(
                        user_email=profile['email_user'], 
                        account_name=profile['account_name'],
                        account_number=account_number_value,
                        bank_name=profile['bank_name'],  
                        branch_name=profile['branch_name'],  
                        bank_id=profile['bank_id'],
                        account_type=profile['account_type'],
                        wallet_id=wallet_id,
                        account_id=account_id
                    )
                    
                    return True
                else:
                    print("Row with the same user_email already exists in wallet_bank_account_table.")
                    return False
            else:
                print("Wallet data not found for the provided customer_id.")
                return False
        else:
            print("Profile not found for the provided customer_id.")
            return False
    except Exception as e:
        print(f"Error occurred: {e}")
        return False

# code for wallet_transactions
def generate_transaction_id():
    latest_transaction = app_tables.fin_wallet_transactions.search(
        tables.order_by("transaction_id", ascending=False)
    )

    if latest_transaction and len(latest_transaction) > 0:
        last_transaction_id = latest_transaction[0]['transaction_id']
        counter = int(last_transaction_id[2:]) + 1
    else:
        counter = 1

    return f"TA{counter:04d}"

@anvil.server.callable
def deposit_money(email, deposit_amount, customer_id):
    transaction_id = generate_transaction_id()
    
    try:
        # Fetch user_email and wallet_id based on  customer_id
        wallet_row = app_tables.fin_wallet.get(user_email=email)
        
        if wallet_row is None:
            # Create a new row in the wallet table if the user does not exist
            wallet_row = app_tables.fin_wallet.add_row(user_email=email, wallet_amount=0)
        elif wallet_row['wallet_amount'] is None:
            # Set default value for wallet_amount if it's None
            wallet_row['wallet_amount'] = 0
        
        user_email = wallet_row['user_email']
        wallet_id = wallet_row['wallet_id']
        
        # Add a row to wallet_transactions table with transaction timestamp
        new_transaction = app_tables.fin_wallet_transactions.add_row(
            user_email=str(user_email),
            wallet_id=str(wallet_id),
            customer_id=customer_id,
            transaction_id=transaction_id,
            amount=deposit_amount,
            transaction_type='deposit',
            transaction_time_stamp=datetime.now(),
            status='success' 
        )
        
        # Retrieve the deposit status from the added row in wallet_transactions
        deposit_status = new_transaction['status']
        
        # Update wallet_amount only if the deposit status is 'success'
        if deposit_status == 'success':
            wallet_row['wallet_amount'] += deposit_amount
            wallet_row.update()
            return True
        else:
            print("Deposit status not successful. Wallet amount not updated.")
            return False
    
    except Exception as e:
        print(f"Deposit failed: {e}")
        app_tables.fin_wallet_transactions.add_row(
            customer_id=customer_id,
            transaction_id=transaction_id,
            amount=deposit_amount,
            transaction_type='deposit',
            transaction_time_stamp=datetime.now(),  
            status='fail'
        )
        return False

@anvil.server.callable
def withdraw_money(email, withdraw_amount, customer_id):
    transaction_id = generate_transaction_id()

    try:
        # Fetch user_email and wallet_id based on customer_id
        wallet_row = app_tables.fin_wallet.get(user_email=email)
        
        if wallet_row is None:
            # Create a new row in the wallet table if the user does not exist
            wallet_row = app_tables.fin_wallet.add_row(user_email=email, wallet_amount=0)

        if wallet_row['wallet_amount'] is not None and wallet_row['wallet_amount'] >= withdraw_amount:
        
        # Assign user_email and wallet_id outside the condition
          user_email = wallet_row['user_email']
          wallet_id = wallet_row['wallet_id']

        # Check if sufficient funds are available for withdrawal
        if wallet_row['wallet_amount'] >= withdraw_amount:
            # Add a row to wallet_transactions table with transaction timestamp
            new_transaction = app_tables.fin_wallet_transactions.add_row(
                user_email=str(user_email),
                wallet_id=str(wallet_id),
                customer_id=customer_id,
                transaction_id=transaction_id,
                amount=withdraw_amount,  
                transaction_type='withdraw',
                transaction_time_stamp=datetime.now(),
                status='success'
            )
            
            # Retrieve the withdrawal status from the added row in wallet_transactions
            withdraw_status = new_transaction['status']

            # Update wallet_amount only if the withdrawal status is 'success'
            if withdraw_status == 'success':
                wallet_row['wallet_amount'] -= withdraw_amount
                wallet_row.update() 
                return True
            else:
                print("Withdrawal failed.")
                return False
        else:
            print("Insufficient funds for withdrawal.")
            return False

    except Exception as e:
        print(f"Withdrawal failed: {e}")
        app_tables.fin_wallet_transactions.add_row(
            customer_id=customer_id,
            transaction_id=transaction_id,
            amount=withdraw_amount,
            transaction_type='withdraw',
            transaction_time_stamp=datetime.now(),
            status='fail'
        )
        return False


@anvil.server.callable
def get_borrower_email(customer_id):
    # Fetch the borrower's email from the fin_wallet table based on the customer ID
    borrower_wallet_row = app_tables.fin_wallet.get(customer_id=customer_id, user_type='borrower')
    if borrower_wallet_row:
        return borrower_wallet_row['user_email']
    else:
        return None
      
@anvil.server.callable
def transfer_money(customer_id, transfer_amount):
    transaction_id = generate_transaction_id()
    customer_id = customer_id
    transfer_amount = transfer_amount
    print("customer_id", customer_id)
    print("transfer_amount", transfer_amount)
    
    try:
        # Obtain the current timestamp
        transaction_timestamp = datetime.now()
        
        # Fetch the borrower's email using the customer_id from the fin_wallet table
        borrower_email = get_borrower_email(customer_id)
        print("borrower_email", borrower_email)
        
        # Ensure that borrower_email is not None
        if borrower_email is None:
            raise ValueError("Borrower email not found.")
        
        # Fetch the wallet row for the borrower
        borrower_wallet_row = app_tables.fin_wallet.get(user_email=borrower_email)
        
        # Ensure that wallet row exists for the borrower
        if borrower_wallet_row is None:
            raise ValueError("Wallet not found for borrower.")
        
        # Add a row to wallet_transactions table for the transfer to the borrower
        borrower_transaction = app_tables.fin_wallet_transactions.add_row(
            user_email = borrower_email,
            wallet_id = borrower_wallet_row['wallet_id'],
            transaction_id=transaction_id,
            amount=transfer_amount,   # Positive amount for addition to borrower's wallet
            transaction_type='received from',
            transaction_time_stamp=transaction_timestamp,
            status='success',
            reciever_email = borrower_email,
            receiver_customer_id = customer_id
        )
        
        # Update borrower's wallet amount
        borrower_wallet_row['wallet_amount'] += transfer_amount
        
        # Update the wallet row
        borrower_wallet_row.update()
        
        return True
    
    except Exception as e:
        print(f"Transfer failed: {e}")
        # Log the failed transaction in wallet_transactions table
        app_tables.fin_wallet_transactions.add_row(
            transaction_id=transaction_id,
            amount = transfer_amount,
            transaction_type ='transferred to',
            transaction_time_stamp=datetime.now(),  
            status='fail'
        )
        return False