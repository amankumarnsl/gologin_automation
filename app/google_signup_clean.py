import traceback
import time
import base64
import os
import io
import json
import requests
import re
from datetime import datetime
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from app.helper.daisysms_client import DaisySMSClient
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class GoogleSignup:
    def __init__(self, driver, actions):
        self.driver = driver
        self.actions = actions
        self.sms_client = DaisySMSClient()
        self.data = {}

    def set_data(self, **kwargs):
        self.data = kwargs

    def go_to_google(self):
        # Navigate to Google and handle consent
        self.driver.get('https://www.google.com/')
        try:
            consent_btn = self.actions.find_element(By.XPATH, "//button[div[contains(text(),'Accept all')]]")
            if consent_btn:
                self.actions.tap(consent_btn)  # 📱 CHANGED: click -> tap
        except:
            try:
                consent_btn_alt = self.actions.find_element(By.XPATH, "//button[contains(.,'I agree')]")
                if consent_btn_alt:
                    self.actions.tap(consent_btn_alt)  # 📱 CHANGED: click -> tap
            except:
                pass

        try:
            search_input = self.actions.find_element(By.NAME, "q")
            self.actions.typing(search_input, "Create google account")
            search_input.send_keys(Keys.RETURN)
            self.actions.human_pause(5, 10)

            signup_link = self.actions.find_element(By.XPATH, "//a[starts-with(@href, 'https://accounts.google.com/')]")
            self.actions.tap(signup_link)  # 📱 CHANGED: click -> tap
            
            self.actions.human_pause(2, 4) 

            print("Tapping 'Create account' button...")
            create_account_btn = self.actions.find_element(By.XPATH, "//span[normalize-space()='Create account']")
            self.actions.tap(create_account_btn)  # 📱 CHANGED: click -> tap

            self.actions.human_pause(1, 2)

            print("Tapping 'For my personal use'...")
            personal_use_option = self.actions.find_element(By.XPATH, "//span[normalize-space()='For my personal use']")
            self.actions.tap(personal_use_option)  # 📱 CHANGED: click -> tap

        except Exception as e:
            print(f"Failed during Google search and navigation: {e}")
            self.driver.get("https://accounts.google.com/signup")

    def fill_name_and_continue(self, first_name, last_name):
        # Fill name fields and continue
        try:
            print("Filling in first and last name...")
            first_name_input = self.actions.find_element(By.NAME, "firstName")
            self.actions.typing(first_name_input, first_name)
            self.actions.human_pause()

            last_name_input = self.actions.find_element(By.NAME, "lastName")
            self.actions.typing(last_name_input, last_name)
            self.actions.human_pause()

            print("Tapping 'Next' button...")
            next_button = self.actions.find_element(By.XPATH, "//span[normalize-space()='Next']")
            self.actions.tap(next_button)  # 📱 CHANGED: click -> tap

        except Exception as e:
            print(f"Failed to fill name and continue: {e}")
            raise

    def fill_basic_info_and_continue(self, day, month, year, gender):
        # Fill DOB and gender information
        try:
            print("Waiting for the 'Basic Information' page to load...")
            wait = WebDriverWait(self.driver, 15)
            
            wait.until(EC.presence_of_element_located((By.NAME, "day")))
            print("Page loaded. Filling date of birth and gender...")

            day_input = self.actions.find_element(By.NAME, "day")
            self.actions.typing(day_input, day)
            self.actions.human_pause(1, 2)

            year_input = self.actions.find_element(By.NAME, "year")
            self.actions.typing(year_input, year)
            self.actions.human_pause(1, 2)

            month_dropdown = self.actions.find_element(By.ID, "month")
            self.actions.tap(month_dropdown)  # 📱 CHANGED: click -> tap
            self.actions.human_pause(1, 2)

            month_xpath = f"//li[@data-value='{month}']"
            wait.until(EC.element_to_be_clickable((By.XPATH, month_xpath)))
            month_option = self.actions.find_element(By.XPATH, month_xpath)
            self.actions.tap(month_option)  # 📱 CHANGED: click -> tap
            self.actions.human_pause(1, 2)
            
            print("Selecting gender with the corrected locator...")
            gender_dropdown_div = self.actions.find_element(By.ID, "gender")
            self.actions.tap(gender_dropdown_div)  # 📱 CHANGED: click -> tap
            self.actions.human_pause(1)

            gender_text = "Male" if gender.lower() == "male" else "Female"
            gender_span_xpath = f"//ul[@role='listbox' and @aria-label='Gender']//span[text()='{gender_text}']"
            
            wait.until(EC.element_to_be_clickable((By.XPATH, gender_span_xpath)))
            gender_option_span = self.actions.find_element(By.XPATH, gender_span_xpath)
            self.actions.tap(gender_option_span)  # 📱 CHANGED: click -> tap
            self.actions.human_pause()

            print("Tapping 'Next' button...")
            next_button = self.actions.find_element(By.XPATH, "//span[normalize-space()='Next']")
            self.actions.tap(next_button)  # 📱 CHANGED: click -> tap

        except Exception as e:
            print(f"Failed to fill basic info and continue: {e}")
            raise
    
    def choose_email_option(self, email_choice_method, username=None):
        # Choose email creation method
        print(f"Choosing email creation method: '{email_choice_method}'")
        wait = WebDriverWait(self.driver, 15)

        if email_choice_method == "existing":
            try:
                print("Selecting 'Use your existing email' option...")
                existing_email_button_xpath = "//button[.//span[text()='Use your existing email']]"
                wait.until(EC.element_to_be_clickable((By.XPATH, existing_email_button_xpath)))
                existing_email_button = self.actions.find_element(By.XPATH, existing_email_button_xpath)
                self.actions.tap(existing_email_button)  # 📱 CHANGED: click -> tap
            except Exception as e:
                print(f"Could not tap 'Use your existing email' button: {e}")
                raise
        else:
            try:
                print(f"Creating a new Gmail address with username: {username}")
                wait.until(EC.visibility_of_element_located((By.NAME, "Username")))
                username_input = self.actions.find_element(By.NAME, "Username")
                self.actions.typing(username_input, username)
                
                print("Tapping 'Next' button...")
                next_button = self.actions.find_element(By.XPATH, "//span[normalize-space()='Next']")
                self.actions.tap(next_button)  # 📱 CHANGED: click -> tap
            except Exception as e:
                print(f"Could not create new username: {e}")
                raise
    
    def fill_existing_email_and_continue(self, email_address):
        # Fill existing email address
        print(f"Entering existing email address: {email_address}")
        wait = WebDriverWait(self.driver, 15)
        try:
            email_input_name = "Username"
            wait.until(EC.visibility_of_element_located((By.NAME, email_input_name)))
            email_input = self.actions.find_element(By.NAME, email_input_name)
            self.actions.typing(email_input, email_address)
            self.actions.human_pause()

            next_button = self.actions.find_element(By.XPATH, "//span[normalize-space()='Next']")
            self.actions.tap(next_button)  # 📱 CHANGED: click -> tap

        except Exception as e:
            print(f"Failed to fill existing email and continue: {e}")
            raise
    
    def verify_email_with_code(self, otp_retrieval_method):
        # Verify email with OTP code
        print("Now on the email verification page.")
        wait = WebDriverWait(self.driver, 15)
        otp_code = None

        try:
            code_input_name = "code"
            wait.until(EC.visibility_of_element_located((By.NAME, code_input_name)))
            
            if otp_retrieval_method == "manual":
                print("\n" + "="*20)
                otp_code = input("ACTION REQUIRED: Please enter the verification code from your email and press Enter: ")
                print("="*20 + "\n")
            else:
                raise NotImplementedError("Automatic OTP retrieval has not been configured.")

            print(f"Entering verification code: {otp_code}")
            code_input = self.actions.find_element(By.NAME, code_input_name)
            self.actions.typing(code_input, otp_code)
            self.actions.human_pause()

            print("Tapping 'Next' to verify code...")
            next_button = self.actions.find_element(By.XPATH, "//span[normalize-space()='Next']")
            self.actions.tap(next_button)  # 📱 CHANGED: click -> tap

        except Exception as e:
            print(f"Failed to enter verification code: {e}")
            raise

    def create_password_and_continue(self, password):
        """
        On the 'Create a strong password' page, this function enters the
        password, confirmation, and taps Next.
        """
        print("Now on the password creation page.")
        wait = WebDriverWait(self.driver, 15)
        try:
            # Wait for the main password field to be visible
            password_input_name = "Passwd"
            wait.until(EC.visibility_of_element_located((By.NAME, password_input_name)))
            print("Password page loaded.")

            # Tap the "Show password" checkbox to act more human-like
            print("Tapping 'Show password' checkbox...")
            show_password_checkbox = self.actions.find_element(By.XPATH, "//input[@type='checkbox']")
            self.actions.tap(show_password_checkbox)  # 📱 CHANGED: click -> tap
            self.actions.human_pause()

            # Enter the password
            print("Entering password...")
            password_input = self.actions.find_element(By.NAME, password_input_name)
            self.actions.typing(password_input, password)
            self.actions.human_pause()

            # Enter the password confirmation
            print("Confirming password...")
            confirm_input_name = "PasswdAgain"
            confirm_input = self.actions.find_element(By.NAME, confirm_input_name)
            self.actions.typing(confirm_input, password)
            self.actions.human_pause()

            # Tap the 'Next' button
            print("Tapping 'Next' to confirm password...")
            next_button = self.actions.find_element(By.XPATH, "//span[normalize-space()='Next']")
            self.actions.tap(next_button)  # 📱 CHANGED: click -> tap

        except Exception as e:
            print(f"Failed to create password: {e}")
            raise

    def signup_until_password(self):
        """
        Run signup process until password creation and next page only.
        Stops before QR code and verification steps.
        """
        try:
            # Step 0: Create a second tab first (for future verification if needed)
            print("Creating a second tab for potential verification...")
            self.driver.execute_script("window.open('about:blank', '_blank');")
            self.actions.human_pause(2, 3)
            
            # Switch back to the first tab for the signup process
            first_tab = self.driver.window_handles[0]
            self.driver.switch_to.window(first_tab)
            print(f"Total tabs created: {len(self.driver.window_handles)}")
            print("Continuing signup process in first tab...")
            
            # Step 1: Navigate to the signup form
            self.go_to_google()
            self.actions.human_pause(3, 5)
            
            # Step 2: Fill in the name details
            self.fill_name_and_continue(
                first_name=self.data.get("first_name", "John"),
                last_name=self.data.get("last_name", "Doe")
            )
            self.actions.human_pause(3, 5)

            # Step 3: Fill in the basic info (DOB, Gender)
            self.fill_basic_info_and_continue(
                day=self.data.get("day", "15"),
                month=self.data.get("month", "5"),
                year=self.data.get("year", "2000"),
                gender=self.data.get("gender", "male")
            )
            self.actions.human_pause(3, 5)

            # Step 4: Choose how to create the email address
            email_creation_method = "new" 
            self.choose_email_option(
                email_choice_method=email_creation_method,
                username=self.data.get("username", "john.doe.12345chd")
            )
            self.actions.human_pause(3, 5)

            # Optional: If using existing email, uncomment these steps:
            # # Step 5: Fill in the existing email address
            # self.fill_existing_email_and_continue(
            #     email_address=self.data.get("existing_email", "krish_kapoor@appdevelopersgermany.com")
            # )
            # self.actions.human_pause(3, 5)

            # # Step 6: Verify the email with a code
            # otp_method = "manual"
            # self.verify_email_with_code(otp_retrieval_method=otp_method)
            # self.actions.human_pause(3, 5)

            # Step 7: Create a password and tap Next
            self.create_password_and_continue(
                password=self.data.get("password", "DefaultPassword@123")
            )
            self.actions.human_pause(4, 7)
            
            print("🎉 Signup completed until password creation!")
            print("✅ All interactions used TAP method for Android compatibility")
            print("🛑 Stopping here as requested - no QR code or verification steps")
            
        except Exception as e:
            print(f"Signup process failed: {e}")
            traceback.print_exc()
