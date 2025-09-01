import traceback
import time
import base64
import os
import io
import json
import requests
import re
import random
from datetime import datetime
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from app.helper.daisysms_client import DaisySMSClient
from app.helper.actions import HumanActions


class GoogleSignupAutomation:
    """
    Comprehensive Google Account Signup Automation
    
    This class handles the complete Google account creation process including:
    - Navigation and form filling
    - QR code extraction and processing
    - SMS verification
    - Network monitoring and data extraction
    """
    
    def __init__(self, driver):
        self.driver = driver
        self.actions = HumanActions(driver)
        self.sms_client = DaisySMSClient()
        self.data = {}
        self.session_context = {
            'is_human': True,
            'interaction_count': 0,
            'last_interaction': time.time(),
            'session_start': time.time()
        }
        
        print("🚀 GoogleSignupAutomation initialized")
    


    def ensure_indian_environment(self):
        """Ensure English US environment with Indian location is applied on every Google page load"""
        try:
            reapply_script = """
            // Reapply US English environment on new page load
            if (window.location.href.includes('google.com')) {
                // Language settings
                Object.defineProperty(navigator, 'language', {
                    get: function() { return 'en-US'; },
                    configurable: true
                });
                Object.defineProperty(navigator, 'languages', {
                    get: function() { return ['en-US', 'en', 'en-IN', 'hi-IN']; },
                    configurable: true
                });
                
                // Document language
                document.documentElement.lang = 'en-US';
                if (document.body) {
                    document.body.setAttribute('lang', 'en-US');
                }
                
                // Google cookies for English US with Indian location
                document.cookie = 'hl=en; path=/; domain=.google.com; max-age=31536000';
                document.cookie = 'gl=IN; path=/; domain=.google.com; max-age=31536000';
                document.cookie = 'lr=lang_en; path=/; domain=.google.com; max-age=31536000';
                
                console.log('🇺🇸🇮🇳 English US environment reapplied for Google page (Indian location)');
            }
            """
            self.driver.execute_script(reapply_script)
        except Exception as e:
            print(f"⚠️  Could not reapply English US environment: {e}")
    
    def find_button_with_fallbacks(self, button_text_variants, additional_selectors=None):
        """Find button using multiple text variants and selector fallbacks"""
        selectors = []
        
        # Add text-based selectors for each variant
        for text in button_text_variants:
            selectors.extend([
                f"//span[normalize-space()='{text}']",
                f"//button[normalize-space()='{text}']",
                f"//div[@role='button' and normalize-space()='{text}']",
                f"//div[contains(text(), '{text}')]"
            ])
        
        # Add generic selectors
        selectors.extend([
            "//button[@type='button' and contains(@class, 'VfPpkd')]//span",
            "//button[contains(@class, 'VfPpkd') and .//span]",
            "//div[@role='button']",
            "//div[@data-primary-action-label]",
            "button[type='submit']"
        ])
        
        # Add any additional custom selectors
        if additional_selectors:
            selectors.extend(additional_selectors)
        
        for selector in selectors:
            try:
                if selector.startswith("//"):
                    element = self.actions.find_element(By.XPATH, selector, timeout=2)
                else:
                    element = self.actions.find_element(By.CSS_SELECTOR, selector, timeout=2)
                print(f"✅ Found button using: {selector}")
                return element
            except:
                continue
        
        return None
    
    def set_data(self, **kwargs):
        """Set automation data parameters"""
        self.data = kwargs
        print(f"📋 Data configured: {list(kwargs.keys())}")
    
    def update_session_context(self, action_type="interaction"):
        """Update session context to maintain human-like session state"""
        try:
            self.session_context['interaction_count'] += 1
            self.session_context['last_interaction'] = time.time()
            self.session_context['is_human'] = True
            
            # Update browser session context
            self.driver.execute_script("""
                // Update session context in browser
                let context = JSON.parse(sessionStorage.getItem('session_context') || '{}');
                context.interactionCount = (context.interactionCount || 0) + 1;
                context.lastInteraction = Date.now();
                context.isHuman = true;
                context.lastAction = arguments[0];
                sessionStorage.setItem('session_context', JSON.stringify(context));
                
                // Simulate human-like session behavior
                if (context.interactionCount % 3 === 0) {
                    // Every 3rd interaction, simulate natural browser behavior
                    setTimeout(() => {
                        window.dispatchEvent(new Event('focus'));
                        document.dispatchEvent(new Event('click'));
                    }, Math.random() * 1000 + 500);
                }
            """, action_type)
            
        except Exception as e:
            print(f"⚠️ Session context update failed: {e}")

    def go_to_google(self):
        """Navigate to Google using search-based approach"""
        print("🌐 Navigating to Google...")
        
        # Navigate to Google homepage
        self.driver.get('https://www.google.com/')
        self.actions.wait_for_page_load()
        
        # Handle consent dialogs
        try:
            consent_btn = self.actions.find_element(By.XPATH, "//button[div[contains(text(),'Accept all')]]", timeout=5)
            if consent_btn:
                print("👆 Clicking consent button...")
                self.actions.tap(consent_btn)
        except:
            try:
                consent_btn_alt = self.actions.find_element(By.XPATH, "//button[contains(.,'I agree')]", timeout=5)
                if consent_btn_alt:
                    print("👆 Clicking I agree button...")
                    self.actions.tap(consent_btn_alt)
            except:
                print("ℹ️  No consent dialog found")

        try:
            # Search for "Create google account"
            print("🔍 Searching for 'Create google account'...")
            search_input = self.actions.find_element(By.NAME, "q")
            
            print("👆 Activating search box...")
            self.actions.tap(search_input)
            time.sleep(random.uniform(0.3, 0.7))
            
            print("⌨️ Typing search query...")
            self.actions.typing(search_input, "Create google account")
            
            # Click search button or use Enter key
            print("👆 Clicking search button...")
            try:
                search_button = self.actions.find_element(By.XPATH, "//input[@name='btnK'] | //button[@name='btnK']")
                self.actions.tap(search_button)
            except:
                print("⌨️ Using Enter key instead...")
                search_input.send_keys(Keys.RETURN)
            
            time.sleep(random.uniform(5, 10))

            # Find and click the signup link
            print("🔗 Looking for signup link...")
            signup_link = self.actions.find_element(By.XPATH, "//a[starts-with(@href, 'https://accounts.google.com/')]")
            
            print("👆 Clicking signup link...")
            self.actions.tap(signup_link)
            
            time.sleep(random.uniform(2, 4)) 

            # Wait for page to fully load
            time.sleep(random.uniform(2, 3))
            
            # 🌍 SELECT ENGLISH LANGUAGE FIRST
            print("🌍 Selecting English language on Create Account page...")
            self.select_english_language_direct()
            
            # Now look for Create account button
            print("👆 Looking for 'Create account' button...")
            create_account_selectors = [
                "//span[normalize-space()='Create account']",
                "//button[contains(text(), 'Create account')]",
                "//div[contains(text(), 'Create account')]",
                "//a[contains(text(), 'Create account')]",
                "//span[contains(text(), 'Create')]",
                "[data-l10n-id='create-account']",
                "//button[contains(@class, 'VfPpkd') and contains(., 'Create')]"
            ]
            
            create_account_btn = None
            for i, selector in enumerate(create_account_selectors):
                try:
                    print(f"🔍 Trying Create account selector {i+1}: {selector}")
                    create_account_btn = self.actions.find_element(By.XPATH, selector, timeout=5)
                    print(f"✅ Found Create account button using selector {i+1}")
                    break
                except:
                    print(f"⚠️  Create account selector {i+1} failed")
                    continue
            
            if not create_account_btn:
                print("❌ Could not find Create account button, taking screenshot...")
                self.actions.take_screenshot("create_account_button_not_found.png")
                raise Exception("Create account button not found with any selector")
            
            # Click Create Account button
            print("👆 Clicking Create account button...")
            self.actions.tap(create_account_btn)

            time.sleep(random.uniform(1, 2))

            # Click "For my personal use"
            print("👆 Looking for 'For my personal use' option...")
            personal_use_option = self.actions.find_element(By.XPATH, "//span[normalize-space()='For my personal use']")
            
            print("👆 Clicking personal use option...")
            self.actions.tap(personal_use_option)

        except Exception as e:
            print(f"⚠️  Search-based navigation failed: {e}")
            print("🔄 Falling back to direct URL...")
            self.driver.get("https://accounts.google.com/signup")
            
            # Try language selection on direct URL page too
            print("🌍 Trying language selection on direct signup page...")
            self.select_language_on_create_account_page()
        
        # Ensure English US environment is applied after navigation
        self.ensure_indian_environment()
        print("✅ Navigation completed, ready for form filling...")

    def select_english_language_direct(self):
        """Select English language"""
        try:
            print("🌍 Using direct language selection...")
            
            # Step 1: Find language dropdown trigger
            language_trigger_selectors = [
                "//div[@jsname='rfCUpd']",  # Most common selector
                "//div[contains(@class, 'VfPpkd') and contains(@class, 'language')]",
                "//div[@role='button' and contains(., 'हिन्दी')]",  # Hindi text
                "//div[@role='button' and contains(., 'भाषा')]",  # Language text
            ]
            
            language_trigger = None
            for i, selector in enumerate(language_trigger_selectors):
                try:
                    print(f"🔍 Trying language trigger selector {i+1}: {selector}")
                    language_trigger = self.actions.find_element(By.XPATH, selector, timeout=3)
                    print(f"✅ Found language trigger using selector {i+1}")
                    break
                except:
                    print(f"⚠️ Language trigger selector {i+1} failed")
                    continue
            
            if not language_trigger:
                print("⚠️ Language dropdown not found, continuing without language change")
                return False
            
            # Step 2: Click language dropdown
            print("👆 Clicking language dropdown to open...")
            self.actions.tap(language_trigger)
            time.sleep(random.uniform(2, 3))  # Wait for dropdown to open
            
            # Step 3: Select English option
            print("🎯 Selecting English option...")
            english_selectors = [
                "//li[@data-value='en-US']",  # Most reliable
                "//li[@data-value='en-GB']",  # Alternative
                "//li[contains(.,'English (United States)')]",
                "//li[contains(.,'English (United Kingdom)')]",
                "//span[contains(text(), 'English')]/ancestor::li"
            ]
            
            english_option = None
            for selector in english_selectors:
                try:
                    english_option = self.driver.find_element(By.XPATH, selector)
                    print(f"✅ Found English option: {selector}")
                    break
                except:
                    continue
            
            if english_option:
                print("👆 Clicking English option...")
                self.actions.tap(english_option)
                time.sleep(random.uniform(2, 3))
                print("✅ English language selected successfully!")
                return True
            else:
                print("⚠️ English option not found, continuing with current language")
                return False
                
        except Exception as e:
            print(f"⚠️ Language selection failed: {e}, continuing with current language")
            return False

    def select_language_on_create_account_page(self):
        """Select English (United States) from language dropdown using REAL mouse movements"""
        try:
            print("🌍 REAL: Looking for language dropdown on create account page...")
            
            # Language dropdown trigger selectors (from your HTML - most static first)
            language_trigger_selectors = [
                # Most static from your HTML structure
                "//div[@jsname='rfCUpd']", 
                # Fallback with role (what we had before)
                "//div[@jsname='oYxtQd' and @role='combobox']",
                # More specific class-based
                "//div[contains(@class, 'VfPpkd-TkwUic') and @role='combobox']",
                # By current language text (if page is in Hindi)
                "//span[contains(text(), 'हिन्दी')]//ancestor::div[@role='combobox']"
            ]
            
            language_trigger = None
            for i, selector in enumerate(language_trigger_selectors):
                try:
                    print(f"🔍 REAL: Trying language trigger selector {i+1}: {selector}")
                    language_trigger = self.actions.find_element(By.XPATH, selector, timeout=3)
                    print(f"✅ REAL: Found language trigger using selector {i+1}")
                    break
                except:
                    print(f"⚠️  Language trigger selector {i+1} failed")
                    continue
            
            if not language_trigger:
                print("⚠️  Language dropdown not found on this page, continuing without language change")
                return False
            
            # Use REAL dropdown selection approach
            print("🎯 REAL: Using natural language dropdown selection...")
            success = self.natural_dropdown_selection(
                dropdown_element=language_trigger,
                option_text="English (United States)",
                dropdown_name="language"
            )
            
            if not success:
                # Fallback: try generic English
                print("🔄 REAL: Trying fallback: generic English selection...")
                success = self.natural_dropdown_selection(
                    dropdown_element=language_trigger,
                    option_text="English",
                    dropdown_name="language"
                )
            
            return success
            
        except Exception as e:
            print(f"❌ Language selection failed: {e}")
            return False

    def fill_name_and_continue(self, first_name, last_name):
        """Fill first and last name"""
        print(f"📝 Filling name: {first_name} {last_name}")
        
        try:
            # Fill first name
            print(f"👆 STEP 1: Activating first name field...")
            first_name_input = self.actions.find_element(By.NAME, "firstName")
            self.actions.tap(first_name_input)
            time.sleep(random.uniform(0.3, 0.7))
            
            print(f"⌨️ STEP 2: Typing first name...")
            self.actions.typing(first_name_input, first_name)
            time.sleep(random.uniform(0.5, 1.0))

            # Fill last name
            print(f"👆 STEP 3: Activating last name field...")
            last_name_input = self.actions.find_element(By.NAME, "lastName")
            self.actions.tap(last_name_input)
            time.sleep(random.uniform(0.3, 0.7))
            
            print(f"⌨️ STEP 4: Typing last name...")
            self.actions.typing(last_name_input, last_name)
            time.sleep(random.uniform(0.5, 1.0))

            # Find and click Next button
            print("🔍 STEP 5: Looking for Next button...")
            next_button = self.find_button_with_fallbacks(
                button_text_variants=["Next", "आगे", "Continuar", "Siguiente", "Suivant"],
                additional_selectors=["[data-test-id='next-button']"]
            )
            
            if next_button:
                print("🎯 STEP 6: Next button found! Clicking...")
                self.actions.tap(next_button)
                print("✅ Next button clicked, waiting for page transition...")
                time.sleep(random.uniform(1.5, 2.5))
                print("✅ Name filled and submitted")
                
                # Verify we moved to the next page (DOB/Gender page)
                try:
                    wait = WebDriverWait(self.driver, 8)
                    wait.until(EC.presence_of_element_located((By.NAME, "day")))
                    print("✅ Successfully navigated to DOB/Gender page")
                except:
                    print("⚠️  DOB page not detected, taking screenshot...")
                    self.actions.take_screenshot("dob_page_not_loaded.png")
                    time.sleep(random.uniform(2.0, 3.0))
                    
            else:
                self.actions.take_screenshot("next_button_not_found.png")
                print("❌ Could not find Next button with any selector")
                try:
                    fallback_btn = self.actions.find_element(By.XPATH, "//button[@type='button']", timeout=5)
                    print("🔄 Using fallback button...")
                    self.actions.tap(fallback_btn)
                    time.sleep(random.uniform(1.5, 2.5))
                except:
                    raise Exception("No clickable buttons found")

        except Exception as e:
            print(f"❌ Failed to fill name: {e}")
            raise

    def fill_basic_info_and_continue(self, day, month, year, gender):
        """Fill date of birth and gender information"""
        print(f"📅 Filling DOB: {day}/{month}/{year}, Gender: {gender}")
        
        try:
            # Enhanced waiting for DOB page to fully load
            print("⏳ STEP 1: Waiting for DOB/Gender page to load...")
            wait = WebDriverWait(self.driver, 8)
            wait.until(EC.presence_of_element_located((By.NAME, "day")))
            time.sleep(random.uniform(1.0, 1.5))
            print("✅ DOB/Gender page loaded successfully")
            
            # Fill day
            print(f"👆 STEP 2: Activating day field...")
            day_input = self.actions.find_element(By.NAME, "day")
            self.actions.tap(day_input)
            time.sleep(random.uniform(0.3, 0.7))
            
            print(f"⌨️ STEP 3: Typing day...")
            self.actions.typing(day_input, str(day))
            time.sleep(random.uniform(0.8, 1.2))

            # Fill year
            print(f"👆 STEP 4: Activating year field...")
            year_input = self.actions.find_element(By.NAME, "year")
            self.actions.tap(year_input)
            time.sleep(random.uniform(0.3, 0.7))
            
            print(f"⌨️ STEP 5: Typing year...")
            self.actions.typing(year_input, str(year))
            time.sleep(random.uniform(0.8, 1.2))

            # Select month using dropdown approach
            print(f"📅 STEP 6: Selecting month: {month}")
            month_dropdown = self.actions.find_element(By.ID, "month")
            
            # Convert month number to month name
            month_names = ['', 'January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December']
            month_text = month_names[int(month)]
            
            # Use dropdown selection
            month_selected = self.natural_dropdown_selection(
                dropdown_element=month_dropdown,
                option_text=month_text,
                dropdown_name="month"
            )
            
            if not month_selected:
                print(f"❌ Month selection failed")
                raise Exception(f"Could not select month {month} ({month_text})")
            
            # Select gender using dropdown approach
            print(f"👤 STEP 7: Selecting gender: {gender}")
            gender_dropdown_div = self.actions.find_element(By.ID, "gender")
            
            # Convert gender to proper text
            gender_text = "Male" if gender.lower() == "male" else "Female"
            
            # Use dropdown selection
            gender_selected = self.natural_dropdown_selection(
                dropdown_element=gender_dropdown_div,
                option_text=gender_text,
                dropdown_name="gender"
            )
            
            if not gender_selected:
                print(f"❌ Gender selection failed")
                raise Exception(f"Could not select gender {gender_text}")

            # Submit - USING SAME METHOD AS NAME PAGE
            print("🔍 STEP 8: Looking for Next button...")
            next_button = self.find_button_with_fallbacks(
                button_text_variants=["Next", "आगे", "Continuar", "Siguiente", "Suivant"],
                additional_selectors=["[data-test-id='next-button']"]
            )
            
            if next_button:
                print("🎯 STEP 9: Next button found! Clicking...")
                self.actions.tap(next_button)
                print("✅ Next button clicked, waiting for page transition...")
                time.sleep(random.uniform(1.5, 2.5))
                print("✅ Basic info filled and submitted")
                
                # Verify we moved to the next page (Email page)
                try:
                    wait = WebDriverWait(self.driver, 8)
                    wait.until(EC.presence_of_element_located((By.NAME, "Username")))
                    print("✅ Successfully navigated to Email page")
                except:
                    print("⚠️  Email page not detected, taking screenshot...")
                    self.actions.take_screenshot("email_page_not_loaded.png")
                    time.sleep(random.uniform(2.0, 3.0))
                    
            else:
                self.actions.take_screenshot("next_button_not_found.png")
                print("❌ Could not find Next button with any selector")
                try:
                    fallback_btn = self.actions.find_element(By.XPATH, "//button[@type='button']", timeout=5)
                    print("🔄 Using fallback button...")
                    self.actions.tap(fallback_btn)
                    time.sleep(random.uniform(1.5, 2.5))
                except:
                    raise Exception("No clickable buttons found")

        except Exception as e:
            print(f"❌ Failed to fill basic info: {e}")
            self.actions.take_screenshot("basic_info_error.png")
            raise
    
    def choose_email_option(self, email_choice_method, username=None):
        """Choose email creation method"""
        print(f"📧 Email method: {email_choice_method}")
        
        # Quick wait for page transition after DOB/Gender
        print("⏳ Quick wait for email page...")
        time.sleep(random.uniform(0.8, 1.2))
        
        wait = WebDriverWait(self.driver, 8)  # Reduced timeout

        if email_choice_method == "existing":
            try:
                print("👆 Looking for existing email option...")
                existing_email_button_xpath = "//button[.//span[text()='Use your existing email']]"
                wait.until(EC.element_to_be_clickable((By.XPATH, existing_email_button_xpath)))
                existing_email_button = self.actions.find_element(By.XPATH, existing_email_button_xpath)
                
                print("👆 Clicking existing email option...")
                self.actions.tap(existing_email_button)
                print("✅ Selected existing email option")
            except Exception as e:
                print(f"❌ Could not select existing email: {e}")
                raise
        else:
            try:
                print(f"📧 Creating new Gmail: {username}")
                
                # Quick wait for username field
                username_input = None
                for attempt in range(2):  # Reduced attempts
                    try:
                        print(f"🔍 Attempt {attempt + 1} - Looking for username field...")
                        wait.until(EC.visibility_of_element_located((By.NAME, "Username")))
                        username_input = self.actions.find_element(By.NAME, "Username")
                        print("✅ Found username field")
                        break
                    except Exception as e:
                        print(f"⚠️ Attempt {attempt + 1} failed: {e}")
                        if attempt < 1:
                            time.sleep(random.uniform(0.5, 1.0))  # Reduced wait
                        else:
                            raise Exception("Username field not found after 2 attempts")
                
                # Fill username - FAST
                print("👆 Activating username field...")
                self.actions.tap(username_input)
                time.sleep(random.uniform(0.2, 0.4))  # Faster
                
                print("⌨️ Typing username...")
                self.actions.typing(username_input, username)
                time.sleep(random.uniform(0.3, 0.6))  # Faster
                
                # Find and click Next button - USING SAME METHOD AS NAME PAGE
                print("🔍 Looking for Next button...")
                next_button = self.find_button_with_fallbacks(
                    button_text_variants=["Next", "आगे", "Continuar", "Siguiente", "Suivant"],
                    additional_selectors=["[data-test-id='next-button']"]
                )
                
                if next_button:
                    print("🎯 Next button found! Clicking...")
                    self.actions.tap(next_button)
                    print("✅ Next button clicked, waiting for page transition...")
                    time.sleep(random.uniform(1.5, 2.5))
                    print("✅ New username created")
                    
                    # Verify we moved to the next page (Password page)
                    try:
                        wait = WebDriverWait(self.driver, 8)
                        wait.until(EC.presence_of_element_located((By.NAME, "Passwd")))
                        print("✅ Successfully navigated to Password page")
                    except:
                        print("⚠️  Password page not detected, taking screenshot...")
                        self.actions.take_screenshot("password_page_not_loaded.png")
                        time.sleep(random.uniform(2.0, 3.0))
                        
                else:
                    self.actions.take_screenshot("next_button_not_found.png")
                    print("❌ Could not find Next button with any selector")
                    try:
                        fallback_btn = self.actions.find_element(By.XPATH, "//button[@type='button']", timeout=5)
                        print("🔄 Using fallback button...")
                        self.actions.tap(fallback_btn)
                        time.sleep(random.uniform(1.5, 2.5))
                    except:
                        raise Exception("No clickable buttons found")
                    
            except Exception as e:
                print(f"❌ Could not create username: {e}")
                self.actions.take_screenshot("username_creation_error.png")
                raise
    
    def fill_existing_email_and_continue(self, email_address):
        """Fill existing email address for account creation - FAST"""
        print(f"📧 Using existing email: {email_address}")
        
        wait = WebDriverWait(self.driver, 6)  # Faster timeout
        try:
            wait.until(EC.visibility_of_element_located((By.NAME, "Username")))
            email_input = self.actions.find_element(By.NAME, "Username")
            
            # Fill email - FAST
            print("👆 Activating email field...")
            self.actions.tap(email_input)
            time.sleep(random.uniform(0.2, 0.4))  # Faster
            
            print("⌨️ Typing email...")
            self.actions.typing(email_input, email_address)
            time.sleep(random.uniform(0.3, 0.6))  # Faster

            # Find and click Next button - USING SAME METHOD AS NAME PAGE
            print("🔍 Looking for Next button...")
            next_button = self.find_button_with_fallbacks(
                button_text_variants=["Next", "आगे", "Continuar", "Siguiente", "Suivant"],
                additional_selectors=["[data-test-id='next-button']"]
            )
            
            if next_button:
                print("🎯 Next button found! Clicking...")
                self.actions.tap(next_button)
                print("✅ Next button clicked, waiting for page transition...")
                time.sleep(random.uniform(1.5, 2.5))
                print("✅ Existing email submitted")
                
                # Verify we moved to the next page (Email verification page)
                try:
                    wait = WebDriverWait(self.driver, 8)
                    wait.until(EC.presence_of_element_located((By.NAME, "code")))
                    print("✅ Successfully navigated to Email verification page")
                except:
                    print("⚠️  Email verification page not detected, taking screenshot...")
                    self.actions.take_screenshot("email_verification_page_not_loaded.png")
                    time.sleep(random.uniform(2.0, 3.0))
                    
            else:
                self.actions.take_screenshot("next_button_not_found.png")
                print("❌ Could not find Next button with any selector")
                try:
                    fallback_btn = self.actions.find_element(By.XPATH, "//button[@type='button']", timeout=5)
                    print("🔄 Using fallback button...")
                    self.actions.tap(fallback_btn)
                    time.sleep(random.uniform(1.5, 2.5))
                except:
                    raise Exception("No clickable buttons found")

        except Exception as e:
            print(f"❌ Failed to fill existing email: {e}")
            raise
    
    def verify_email_with_code(self, otp_retrieval_method):
        """Handle email verification with OTP code"""
        print("📧 Email verification required")
        
        wait = WebDriverWait(self.driver, 8)  # 8 seconds MAX
        otp_code = None

        try:
            wait.until(EC.visibility_of_element_located((By.NAME, "code")))
            
            if otp_retrieval_method == "manual":
                print("\n" + "="*50)
                print("🔑 MANUAL OTP REQUIRED")
                otp_code = input("Please enter the verification code from your email: ")
                print("="*50 + "\n")
            else:
                raise NotImplementedError("Automatic OTP retrieval not configured")

            code_input = self.actions.find_element(By.NAME, "code")
            self.actions.typing(code_input, otp_code)
            self.actions.human_pause()

            next_button = self.actions.find_element(By.XPATH, "//span[normalize-space()='Next']")
            self.actions.tap(next_button)
            print("✅ Email verification completed")

        except Exception as e:
            print(f"❌ Email verification failed: {e}")
            raise

    def create_password_and_continue(self, password):
        """Create and confirm password for the account"""
        print("🔐 Creating account password...")
        
        # Quick wait for page transition
        print("⏳ Quick wait for password page...")
        time.sleep(random.uniform(0.8, 1.2))
        
        wait = WebDriverWait(self.driver, 8)  # Reduced timeout
        try:
            # Try multiple password field selectors
            password_selectors = [
                (By.NAME, "Passwd"),
                (By.NAME, "password"), 
                (By.XPATH, "//input[@type='password']"),
                (By.XPATH, "//input[contains(@name, 'assw')]"),
                (By.CSS_SELECTOR, "input[type='password']")
            ]
            
            password_input = None
            for by, selector in password_selectors:
                try:
                    print(f"🔍 Trying password selector: {by}={selector}")
                    wait.until(EC.visibility_of_element_located((by, selector)))
                    password_input = self.actions.find_element(by, selector)
                    print(f"✅ Found password field using: {by}={selector}")
                    break
                except:
                    continue
            
            if not password_input:
                # Take screenshot for debugging
                self.actions.take_screenshot("password_field_not_found.png")
                raise Exception("Password field not found with any selector")
            
            # Show password for human-like behavior - FAST
            try:
                show_password_checkbox = self.actions.find_element(By.XPATH, "//input[@type='checkbox']", timeout=2)
                print("👆 Clicking show password checkbox...")
                self.actions.tap(show_password_checkbox)
                print("👁️ Showed password for visibility")
            except:
                print("ℹ️  Show password checkbox not found")

            # Fill password - FAST
            print("👆 Activating password field...")
            self.actions.tap(password_input)
            time.sleep(random.uniform(0.2, 0.4))  # Faster
            
            print("⌨️ Typing password...")
            self.actions.typing(password_input, password)
            time.sleep(random.uniform(0.3, 0.6))  # Faster

            # Confirm password - FAST
            print("🔍 Looking for confirm password field...")
            confirm_selectors = [
                (By.NAME, "PasswdAgain"),
                (By.NAME, "ConfirmPasswd"),
                (By.XPATH, "//input[@type='password'][2]"),
                (By.XPATH, "//input[contains(@name, 'onfirm')]")
            ]
            
            confirm_input = None
            for by, selector in confirm_selectors:
                try:
                    confirm_input = self.actions.find_element(by, selector, timeout=2)  # Faster timeout
                    print(f"✅ Found confirm password field using: {by}={selector}")
                    break
                except:
                    continue
            
            if confirm_input:
                print("👆 Activating confirm password field...")
                self.actions.tap(confirm_input)
                time.sleep(random.uniform(0.2, 0.4))  # Faster
                
                print("⌨️ Typing confirm password...")
                self.actions.typing(confirm_input, password)
                time.sleep(random.uniform(0.3, 0.6))  # Faster
            else:
                print("⚠️  Confirm password field not found, continuing...")

            # Submit with robust button finding - USING SAME METHOD AS NAME PAGE
            print("🔍 Looking for submit button...")
            next_button = self.find_button_with_fallbacks(
                button_text_variants=["Next", "आगे", "Create", "Continue"],
                additional_selectors=["//button[@type='submit']"]
            )
            
            if next_button:
                print("🎯 Submit button found! Clicking...")
                self.actions.tap(next_button)
                print("✅ Submit button clicked, waiting for page transition...")
                time.sleep(random.uniform(1.5, 2.5))
                print("✅ Password created and confirmed")
                
                # Verify we moved to the next page (Mobile verification page)
                try:
                    wait = WebDriverWait(self.driver, 8)
                    wait.until(EC.presence_of_element_located((By.ID, "phoneNumberId")))
                    print("✅ Successfully navigated to Mobile verification page")
                except:
                    print("⚠️  Mobile verification page not detected, taking screenshot...")
                    self.actions.take_screenshot("mobile_verification_page_not_loaded.png")
                    time.sleep(random.uniform(2.0, 3.0))
                    
            else:
                self.actions.take_screenshot("next_button_not_found.png")
                print("❌ Could not find Next button with any selector")
                try:
                    fallback_btn = self.actions.find_element(By.XPATH, "//button[@type='button']", timeout=5)
                    print("🔄 Using fallback button...")
                    self.actions.tap(fallback_btn)
                    time.sleep(random.uniform(1.5, 2.5))
                except:
                    raise Exception("No clickable buttons found")

        except Exception as e:
            print(f"❌ Password creation failed: {e}")
            raise

    def extract_and_save_qr_code(self, save_path="qr_code.png"):
        """Extract QR code from verification page and save as image file"""
        print("📱 Extracting QR code...")
        
        wait = WebDriverWait(self.driver, 8)  # 8 seconds MAX
        
        try:
            qr_img_xpath = "//img[contains(@alt, 'Image of QR code') or contains(@src, 'data:image/png;base64')]"
            wait.until(EC.presence_of_element_located((By.XPATH, qr_img_xpath)))
            
            qr_img_element = self.actions.find_element(By.XPATH, qr_img_xpath)
            img_src = qr_img_element.get_attribute("src")
            
            if img_src.startswith("data:image/png;base64,"):
                base64_data = img_src.split("data:image/png;base64,")[1]
                
                # Fix padding
                missing_padding = len(base64_data) % 4
                if missing_padding:
                    base64_data += '=' * (4 - missing_padding)
                
                # Decode and save
                img_data = base64.b64decode(base64_data)
                
                with open(save_path, "wb") as img_file:
                    img_file.write(img_data)
                
                print(f"✅ QR code saved: {save_path}")
                return save_path, base64_data
            else:
                print("❌ QR code not in expected format")
                return None, None
                
        except Exception as e:
            print(f"❌ QR code extraction failed: {e}")
            return None, None

    def decode_qr_code_and_open_url(self, base64_image_data):
        """Decode QR code and open verification URL in new tab"""
        print("🔍 Decoding QR code...")
        
        try:
            img_data = base64.b64decode(base64_image_data)
            qr_url = None
            
            # Try multiple QR decoders
            try:
                from qreader import QReader
                from PIL import Image
                
                image = Image.open(io.BytesIO(img_data))
                qreader = QReader()
                decoded_text = qreader.detect_and_decode(image=image)
                
                if decoded_text and len(decoded_text) > 0:
                    qr_url = decoded_text[0]
                    print(f"✅ QR decoded with qreader: {qr_url}")
                    
            except ImportError:
                print("⚠️  qreader not available, trying OpenCV...")
                
                try:
                    import cv2
                    import numpy as np
                    from PIL import Image
                    
                    pil_image = Image.open(io.BytesIO(img_data))
                    if pil_image.mode != 'RGB':
                        pil_image = pil_image.convert('RGB')
                    
                    pil_array = np.array(pil_image)
                    cv_image = cv2.cvtColor(pil_array, cv2.COLOR_RGB2BGR)
                    
                    detector = cv2.QRCodeDetector()
                    data, vertices_array, binary_qrcode = detector.detectAndDecode(cv_image)
                    
                    if data:
                        qr_url = data
                        print(f"✅ QR decoded with OpenCV: {qr_url}")
                        
                except ImportError:
                    print("❌ No QR decoder libraries available")
            
            # Open URL in new tab if decoded successfully
            if qr_url and qr_url.strip() and qr_url.startswith(('http://', 'https://')):
                qr_url = qr_url.strip()
                print(f"🌐 Opening verification URL: {qr_url}")
                
                try:
                    original_tab = self.driver.current_window_handle
                    all_tabs = self.driver.window_handles
                    
                    if len(all_tabs) >= 2:
                        verification_tab = all_tabs[1]
                        self.driver.switch_to.window(verification_tab)
                        self.driver.get(qr_url)
                        print("✅ Verification URL opened in second tab")
                        
                        self.actions.human_pause(1.0, 1.5)  # 🚀 FASTER
                        
                        # Monitor network and click Send SMS
                        network_file = self.monitor_and_save_network_calls(
                            save_path=self.data.get("network_save_path", "sms_network_calls.json")
                        )
                        
                        if network_file:
                            print(f"📁 Network data saved: {network_file}")
                        
                        # Return to original tab
                        self.driver.switch_to.window(original_tab)
                        print("🔙 Returned to original tab")
                        
                        return qr_url
                    else:
                        print("⚠️  Creating new tab...")
                        self.driver.execute_script(f"window.open('{qr_url}', '_blank');")
                        self.actions.human_pause(1.0, 1.5)  # 🚀 FASTER
                        return qr_url
                        
                except Exception as nav_error:
                    print(f"❌ Navigation failed: {nav_error}")
                    return qr_url
            else:
                print("❌ Failed to decode QR code URL")
                return None
                
        except Exception as e:
            print(f"❌ QR processing failed: {e}")
            return None

    def monitor_and_save_network_calls(self, save_path="network_calls.json"):
        """Monitor network calls and extract SMS data"""
        print("📡 Setting up network monitoring...")
        
        # Clear previous data
        try:
            if os.path.exists(save_path):
                os.remove(save_path)
                print(f"🗑️  Cleared previous data: {save_path}")
        except Exception as e:
            print(f"⚠️  Could not clear file: {e}")
        
        try:
            # Inject monitoring script
            monitoring_script = """
            window.networkCalls = [];
            window.allResources = [];
            
            const originalFetch = window.fetch;
            const originalOpen = XMLHttpRequest.prototype.open;
            const originalSend = XMLHttpRequest.prototype.send;
            
            // Monitor Fetch API
            window.fetch = function(...args) {
                const startTime = Date.now();
                const url = args[0];
                const options = args[1] || {};
                
                const requestData = {
                    timestamp: new Date().toISOString(),
                    type: 'fetch',
                    url: url,
                    method: options.method || 'GET',
                    headers: options.headers || {},
                    body: options.body || null,
                    startTime: startTime
                };
                
                return originalFetch.apply(this, args).then(response => {
                    const endTime = Date.now();
                    const responseData = {
                        ...requestData,
                        endTime: endTime,
                        duration: endTime - startTime,
                        status: response.status,
                        statusText: response.statusText,
                        responseHeaders: {},
                        responseType: response.type,
                        responseUrl: response.url
                    };
                    
                    response.headers.forEach((value, key) => {
                        responseData.responseHeaders[key] = value;
                    });
                    
                    window.networkCalls.push(responseData);
                    return response;
                }).catch(error => {
                    window.networkCalls.push({...requestData, endTime: Date.now(), error: error.message});
                    throw error;
                });
            };
            
            // Monitor XMLHttpRequest
            XMLHttpRequest.prototype.open = function(method, url, async, user, password) {
                this._requestData = {
                    timestamp: new Date().toISOString(),
                    type: 'xhr',
                    method: method,
                    url: url,
                    startTime: Date.now(),
                    headers: {}
                };
                return originalOpen.apply(this, arguments);
            };
            
            XMLHttpRequest.prototype.send = function(body) {
                if (this._requestData) {
                    this._requestData.body = body;
                }
                
                this.addEventListener('loadend', () => {
                    if (this._requestData) {
                        const responseData = {
                            ...this._requestData,
                            endTime: Date.now(),
                            duration: Date.now() - this._requestData.startTime,
                            status: this.status,
                            statusText: this.statusText,
                            responseHeaders: this.getAllResponseHeaders(),
                            responseBody: this.responseText,
                            responseType: this.responseType,
                            responseURL: this.responseURL
                        };
                        window.networkCalls.push(responseData);
                    }
                });
                
                return originalSend.apply(this, arguments);
            };
            
            console.log('Network monitoring initialized');
            """
            
            # Find and click Send SMS button
            try:
                wait = WebDriverWait(self.driver, 8)  # 8 seconds MAX
                send_sms_xpath = "//span[text()='Send SMS']//ancestor::button"
                wait.until(EC.element_to_be_clickable((By.XPATH, send_sms_xpath)))
                
                # Execute monitoring script first
                self.driver.execute_script(monitoring_script)
                print("📡 Network monitoring active")
                self.actions.human_pause(0.6, 1.0)  # 🚀 FASTER
                
                # Click Send SMS
                send_sms_button = self.actions.find_element(By.XPATH, send_sms_xpath)
                self.actions.tap(send_sms_button)
                print("✅ Send SMS clicked, monitoring network...")
                
                # Wait for network calls
                self.actions.human_pause(2.0, 3.0)  # 🚀 FASTER
                
                # Collect network data
                network_calls = self.driver.execute_script("return window.networkCalls || [];")
                all_resources = self.driver.execute_script("return window.allResources || [];")
                
                # Filter document-type requests
                document_xhr_calls = []
                for call in network_calls:
                    if ('devicephoneverification' in call.get('url', '') or
                        'accounts.google.com' in call.get('url', '') or
                        'Send%20this%20message' in call.get('url', '')):
                        document_xhr_calls.append(call)
                
                # Save network data
                network_data = {
                    "session_info": {
                        "timestamp": datetime.now().isoformat(),
                        "url": self.driver.current_url,
                        "user_agent": self.driver.execute_script("return navigator.userAgent;"),
                        "total_calls": len(network_calls),
                        "document_calls": len(document_xhr_calls)
                    },
                    "document_xhr_calls": document_xhr_calls,
                    "all_captured_calls": network_calls,
                    "all_resources": all_resources
                }
                
                with open(save_path, 'w', encoding='utf-8') as f:
                    json.dump(network_data, f, indent=2, ensure_ascii=False)
                
                print(f"📁 Network data saved: {save_path}")
                print(f"📊 Captured {len(network_calls)} total calls, {len(document_xhr_calls)} document calls")
                
                # Extract and send SMS
                sms_data = self.extract_and_display_sms_data(network_calls)
                if sms_data:
                    mobile = sms_data.get("mobile")
                    message = sms_data.get("text_message")
                    
                    if mobile and message:
                        sms_sent = self.send_qr_verification_sms(mobile, message)
                        if sms_sent:
                            print("🎉 QR verification SMS sent!")
                        else:
                            print("⚠️  SMS sending failed")
                
                return save_path
                    
            except Exception as sms_error:
                print(f"❌ Send SMS failed: {sms_error}")
                return None
                
        except Exception as e:
            print(f"❌ Network monitoring failed: {e}")
            return None

    def extract_and_display_sms_data(self, network_calls):
        """Extract SMS data from network calls"""
        print("🔍 Extracting SMS data from network calls...")
        
        sms_data = {
            "mobile": None,
            "text_message": None,
            "found": False
        }
        
        try:
            for call in network_calls:
                response_body = call.get('responseBody', '')
                
                if ('Send this message' in response_body and '+91' in response_body):
                    print("🎯 Found SMS data in response!")
                    
                    # Extract using regex
                    pattern = r'\[\\*"(\+91\d+)\\*",\\*"(Send this message[^"\\]+)'
                    match = re.search(pattern, response_body)
                    
                    if match:
                        sms_data["mobile"] = match.group(1)
                        raw_message = match.group(2)
                        clean_message = raw_message.replace('\\"', '').replace('\\\\', '').strip()
                        sms_data["text_message"] = clean_message
                        sms_data["found"] = True
                        break
                    else:
                        # Fallback pattern
                        phone_pattern = r'(\+91\d{10})'
                        message_pattern = r'(Send this message without editing\. \([^)]+\))'
                        
                        phone_match = re.search(phone_pattern, response_body)
                        message_match = re.search(message_pattern, response_body)
                        
                        if phone_match and message_match:
                            sms_data["mobile"] = phone_match.group(1)
                            clean_message = message_match.group(1).replace('\\"', '').replace('\\\\', '').strip()
                            sms_data["text_message"] = clean_message
                            sms_data["found"] = True
                            break
            
            if sms_data["found"]:
                print("\n" + "="*60)
                print("📱 EXTRACTED SMS DATA")
                print("="*60)
                
                clean_sms_data = {
                    "mobile": sms_data["mobile"],
                    "text_message": sms_data["text_message"]
                }
                
                print(json.dumps(clean_sms_data, indent=2, ensure_ascii=False))
                print("="*60 + "\n")
                
                # Save SMS data
                sms_file = "extracted_sms_data.json"
                with open(sms_file, 'w', encoding='utf-8') as f:
                    json.dump(clean_sms_data, f, indent=2, ensure_ascii=False)
                
                print(f"💾 SMS data saved: {sms_file}")
                return clean_sms_data
            else:
                print("❌ SMS data not found")
                return None
                
        except Exception as e:
            print(f"❌ SMS extraction failed: {e}")
            return None

    def send_qr_verification_sms(self, mobile_number, text_message):
        """Send QR verification SMS using D7 API"""
        print(f"📤 Sending QR verification SMS to {mobile_number}...")
        
        try:
            result = self.sms_client.send_sms(mobile_number, text_message)
            
            if result["success"]:
                print("✅ QR verification SMS sent successfully!")
                return True
            else:
                print(f"❌ SMS sending failed: {result.get('error', 'Unknown error')}")
                return False
                
        except Exception as e:
            print(f"❌ SMS sending error: {e}")
            return False

    def handle_phone_verification(self):
        """Handle mobile number verification instead of QR code"""
        print("📱 Starting mobile number verification...")
        
        try:
            # 🔧 SESSION CONTEXT MANAGEMENT: Reset session context before mobile verification
            print("🔧 Managing session context for mobile verification...")
            self.driver.execute_script("""
                // Reset session context to appear more human-like
                let context = JSON.parse(sessionStorage.getItem('session_context') || '{}');
                context.isHuman = true;
                context.interactionCount = Math.floor(Math.random() * 10) + 5; // Random realistic count
                context.lastInteraction = Date.now();
                context.sessionStart = Date.now() - (Math.random() * 300000 + 60000); // Random session start
                context.mobileVerificationAttempt = 1;
                sessionStorage.setItem('session_context', JSON.stringify(context));
                
                // Simulate natural page interaction
                setTimeout(() => {
                    window.dispatchEvent(new Event('focus'));
                    document.dispatchEvent(new Event('click'));
                }, Math.random() * 2000 + 1000);
            """)
            
            wait = WebDriverWait(self.driver, 8)  # 8 seconds MAX
            
            # Step 1: Select India (+91) from country code dropdown
            print("🇮🇳 Selecting India (+91) from country dropdown...")
            
            # Try multiple selectors to find the country dropdown
            country_selectors = [
                (By.ID, "countryList"),
                (By.XPATH, "//div[@jscontroller='lcGjA']"),
                (By.XPATH, "//div[@class='mWroFe']"),
                (By.XPATH, "//div[contains(@class, 'VfPpkd-O1htCb')]//span[contains(text(), '+91') or contains(text(), 'India')]"),
                (By.XPATH, "//div[@role='combobox']")
            ]
            
            country_dropdown = None
            for by, selector in country_selectors:
                try:
                    country_dropdown = self.actions.find_element(by, selector, timeout=3)
                    print(f"✅ Found country dropdown using: {by}={selector}")
                    break
                except:
                    continue
            
            if country_dropdown:
                # Click to open dropdown
                self.actions.tap(country_dropdown)
                self.actions.human_pause(0.6, 1.0)  # 🚀 FASTER
                
                # Find and select India (+91) option
                india_selectors = [
                    (By.XPATH, "//span[contains(text(), 'India (+91)')]"),
                    (By.XPATH, "//li[@data-value='in']"),
                    (By.XPATH, "//span[contains(@class, 'VfPpkd-rymPhb-fpDzbe-fmcmS') and contains(text(), 'India (+91)')]"),
                    (By.XPATH, "//li[contains(., 'India (+91)')]")
                ]
                
                india_option = None
                for by, selector in india_selectors:
                    try:
                        wait.until(EC.element_to_be_clickable((by, selector)))
                        india_option = self.actions.find_element(by, selector)
                        print(f"✅ Found India option using: {by}={selector}")
                        break
                    except:
                        continue
                
                if india_option:
                    self.actions.tap(india_option)
                    print("✅ India (+91) selected")
                    self.actions.human_pause(0.6, 1.0)  # 🚀 FASTER
                else:
                    print("⚠️  India option not found, continuing with default")
            else:
                print("⚠️  Country dropdown not found, continuing...")
            
            # Step 2: Fill phone number from console input
            print("📞 Looking for phone number input field...")
            
            # Try multiple selectors for phone number field
            phone_selectors = [
                (By.ID, "phoneNumberId"),
                (By.XPATH, "//input[@type='tel']"),
                (By.XPATH, "//input[@jsname='YPqjbf']"),
                (By.XPATH, "//input[contains(@class, 'VfPpkd-fmcmS-wGMbrd')]"),
                (By.NAME, "phoneNumber"),
                (By.XPATH, "//input[contains(@placeholder, 'phone') or contains(@placeholder, 'mobile')]")
            ]
            
            phone_input = None
            for by, selector in phone_selectors:
                try:
                    wait.until(EC.presence_of_element_located((by, selector)))
                    phone_input = self.actions.find_element(by, selector)
                    print(f"✅ Found phone input field using: {by}={selector}")
                    break
                except:
                    continue
            
            if phone_input:
                # Use mobile number from configuration or prompt user
                mobile_number = self.data.get("mobile_number")
                if mobile_number:
                    # Remove +91 if present, since country code is already selected
                    clean_mobile = mobile_number.replace("+91", "").strip()
                    print(f"📱 Using configured mobile number: {clean_mobile}")
                else:
                    # Fallback to manual input
                    print("\n" + "="*60)
                    print("📱 MOBILE NUMBER REQUIRED")
                    print("="*60)
                    clean_mobile = input("Please enter your mobile number (without +91): ")
                    print("="*60 + "\n")
                
                # 🔧 SESSION CONTEXT: Update before phone input
                self.update_session_context("phone_input")
                
                # Clear any existing value and type the number
                phone_input.clear()
                self.actions.typing(phone_input, clean_mobile)
                print(f"✅ Mobile number entered: {clean_mobile}")
                
                # 🔧 SESSION CONTEXT: Update after phone input
                self.driver.execute_script("""
                    // Update session context after phone input
                    let context = JSON.parse(sessionStorage.getItem('session_context') || '{}');
                    context.phoneNumberEntered = true;
                    context.lastPhoneInput = Date.now();
                    context.isHuman = true;
                    sessionStorage.setItem('session_context', JSON.stringify(context));
                """)
                
                # Random pause as requested (2-4 seconds)
                pause_duration = random.uniform(2, 4)
                print(f"⏳ Waiting {pause_duration:.1f} seconds...")
                time.sleep(pause_duration)
                
                # Step 3: Tap Next button
                print("👆 Tapping Next button...")
                next_button = self.find_button_with_fallbacks(
                    button_text_variants=["Next", "आगे", "Continue", "Continuar"],
                    additional_selectors=["//button[@type='submit']", "//div[@role='button']"]
                )
                
                if next_button:
                    # 🔧 SESSION CONTEXT: Update before Next button click
                    self.driver.execute_script("""
                        // Update session context before Next button click
                        let context = JSON.parse(sessionStorage.getItem('session_context') || '{}');
                        context.nextButtonClick = true;
                        context.lastNextClick = Date.now();
                        context.isHuman = true;
                        context.mobileVerificationStep = 'next_click';
                        sessionStorage.setItem('session_context', JSON.stringify(context));
                        
                        // Simulate natural button click behavior
                        setTimeout(() => {
                            window.dispatchEvent(new Event('beforeunload'));
                            window.dispatchEvent(new Event('focus'));
                        }, 100);
                    """)
                    
                    self.actions.tap(next_button)
                    print("✅ Next button tapped successfully")
                    
                    # 🔧 SESSION CONTEXT: Update after Next button click
                    self.driver.execute_script("""
                        // Update session context after Next button click
                        let context = JSON.parse(sessionStorage.getItem('session_context') || '{}');
                        context.nextButtonClicked = true;
                        context.lastNextClickTime = Date.now();
                        context.isHuman = true;
                        context.mobileVerificationStep = 'waiting_for_otp';
                        sessionStorage.setItem('session_context', JSON.stringify(context));
                    """)
                    
                    self.actions.human_pause(0.8, 1.2)  # 🚀 FASTER
                    
                    # Step 4: Handle OTP verification
                    print("🔐 Waiting for OTP verification page...")
                    self.actions.human_pause(1.0, 1.5)  # 🚀 FASTER
                    
                    # Find OTP input field
                    print("🔢 Looking for OTP input field...")
                    otp_selectors = [
                        (By.ID, "code"),
                        (By.NAME, "code"),
                        (By.XPATH, "//input[@type='tel' and contains(@pattern, '[0-9')]"),
                        (By.XPATH, "//input[@aria-label='Enter code']"),
                        (By.XPATH, "//input[@jsname='YPqjbf']"),
                        (By.XPATH, "//input[contains(@class, 'whsOnd zHQkBf')]")
                    ]
                    
                    otp_input = None
                    for by, selector in otp_selectors:
                        try:
                            wait.until(EC.presence_of_element_located((by, selector)))
                            otp_input = self.actions.find_element(by, selector)
                            print(f"✅ Found OTP input field using: {by}={selector}")
                            break
                        except:
                            continue
                    
                    if otp_input:
                        # Prompt user for OTP
                        print("\n" + "="*60)
                        print("🔐 OTP VERIFICATION REQUIRED")
                        print("="*60)
                        otp_code = input("Please enter the 6-digit verification code from SMS: ")
                        print("="*60 + "\n")
                        
                        # Clear any existing value and type the OTP
                        otp_input.clear()
                        self.actions.typing(otp_input, otp_code)
                        print(f"✅ OTP entered: {otp_code}")
                        
                        # Random pause as requested (1-2 seconds max)
                        pause_duration = random.uniform(1, 2)
                        print(f"⏳ Waiting {pause_duration:.1f} seconds...")
                        time.sleep(pause_duration)
                        
                        # Step 5: Tap Next button after OTP
                        print("👆 Tapping Next button to submit OTP...")
                        next_button_otp = self.find_button_with_fallbacks(
                            button_text_variants=["Next", "आगे", "Continue", "Continuar", "Submit"],
                            additional_selectors=["//button[@type='submit']", "//div[@role='button']"]
                        )
                        
                        if next_button_otp:
                            self.actions.tap(next_button_otp)
                            print("✅ Next button tapped successfully after OTP")
                            self.actions.human_pause(0.8, 1.2)  # 🚀 FASTER
                        else:
                            print("❌ Next button not found after OTP entry")
                            self.actions.take_screenshot("next_button_after_otp.png")
                            
                    else:
                        print("❌ OTP input field not found")
                        self.actions.take_screenshot("otp_input_not_found.png")
                        
                else:
                    print("❌ Next button not found")
                    self.actions.take_screenshot("next_button_after_phone.png")
                    
            else:
                print("❌ Phone number input field not found")
                self.actions.take_screenshot("phone_input_not_found.png")
                
            print("✅ Mobile verification step completed")
            
        except Exception as e:
            print(f"❌ Mobile verification failed: {e}")
            self.actions.take_screenshot("mobile_verification_error.png")
            traceback.print_exc()

    def signup_until_mobile_verification(self):
        """Run signup process including mobile verification but stop before QR code (Android optimized)"""
        try:
            print("🚀 Starting Android-optimized signup including mobile verification...")
            
            # 🔧 Use existing tabs (created in gologin-selenium.py)
            first_tab = self.driver.window_handles[0]
            
            if len(self.driver.window_handles) >= 2:
                print(f"✅ Using existing tabs! Total: {len(self.driver.window_handles)}")
            
            # Step 1: Navigate using search-based approach (integrated from clean code)
            self.go_to_google()
            self.actions.human_pause(0.5, 0.8)  # Faster
            
            # Step 2: Fill name with tap interactions
            self.fill_name_and_continue(
                first_name=self.data.get("first_name", "John"),
                last_name=self.data.get("last_name", "Doe")
            )
            self.actions.human_pause(0.5, 0.8)  # Faster

            # Step 3: Fill basic info (DOB/Gender) with enhanced tap logic
            self.fill_basic_info_and_continue(
                day=self.data.get("day", "15"),
                month=self.data.get("month", "5"),
                year=self.data.get("year", "2000"),
                gender=self.data.get("gender", "male")
            )
            self.actions.human_pause(0.5, 0.8)  # Faster

            # Step 4: Choose email method
            email_creation_method = self.data.get("email_method", "new")
            if email_creation_method == "new":
                self.choose_email_option(
                    email_choice_method="new",
                    username=self.data.get("username", "john.doe.12345chd")
                )
            else:
                self.choose_email_option(
                    email_choice_method="existing"
                )
                self.actions.human_pause(0.5, 0.8)  # Faster
                self.fill_existing_email_and_continue(
                    email_address=self.data.get("existing_email", "user@example.com")
                )
                self.actions.human_pause(0.5, 0.8)  # Faster
                self.verify_email_with_code(
                    otp_retrieval_method=self.data.get("otp_method", "manual")
                )
            
            self.actions.human_pause(0.5, 0.8)  # Faster

            # Step 5: Create password and tap Next - FAST
            try:
                print("🔐 REAL: Attempting password creation...")
                self.create_password_and_continue(
                    password=self.data.get("password", "DefaultPassword@123")
                )
                self.actions.human_pause(0.8, 1.2)  # Faster
            except Exception as e:
                print(f"⚠️ Password creation failed: {e}")
                print("🔄 Checking if we're on a different page...")
                
                # Take screenshot to see what page we're on
                self.actions.take_screenshot("after_email_creation.png")
                
                # Quick wait and try to detect the current page
                time.sleep(1.5)  # Faster
                current_url = self.driver.current_url
                print(f"📍 Current URL: {current_url}")
                
                # Check if we need to handle additional verification
                if "challenge" in current_url.lower() or "verification" in current_url.lower():
                    print("🔍 Detected verification page, attempting to handle...")
                    # Try to find and handle verification elements
                    try:
                        # Look for common verification elements
                        verification_selectors = [
                            "//input[@type='text']",
                            "//input[@type='tel']", 
                            "//input[contains(@name, 'code')]",
                            "//input[contains(@name, 'otp')]"
                        ]
                        
                        for selector in verification_selectors:
                            try:
                                element = self.driver.find_element(By.XPATH, selector)
                                print(f"✅ Found verification element: {selector}")
                                break
                            except:
                                continue
                        
                        print("⚠️ Manual intervention may be required for verification")
                        
                    except Exception as verify_e:
                        print(f"❌ Verification handling failed: {verify_e}")
                
                # Continue with mobile verification even if password failed
                print("🔄 Continuing with mobile verification...")
            
            # Step 6: Handle mobile number verification - FAST
            print("📱 Starting mobile number verification...")
            self.handle_phone_verification()
            self.actions.human_pause(0.8, 1.2)  # Faster
            
            print("🎉 Signup completed including mobile verification!")
            print("✅ All interactions used TAP method for Android compatibility")
            print("🔍 Used search-based navigation for better reliability")
            print("📱 Mobile verification completed")
            print("🛑 Stopping here - no QR code or further verification steps")
            
        except Exception as e:
            print(f"❌ Signup process failed: {e}")
            self.actions.take_screenshot("signup_mobile_verification_error.png")
            traceback.print_exc()

    def run_complete_signup(self):
        """Run the complete Google signup automation process"""
        try:
            print("🚀 Starting complete Google signup automation...")
            
            # 🔧 Use existing tabs (created in gologin-selenium.py)
            first_tab = self.driver.window_handles[0]
            second_tab = None
            
            if len(self.driver.window_handles) >= 2:
                second_tab = self.driver.window_handles[1]
                print(f"✅ Using existing tabs! Total: {len(self.driver.window_handles)}")
                
                # Step 1: Do IP checking in second tab
                print("🔄 Switching to second tab for IP verification...")
                self.driver.switch_to.window(second_tab)
                self.actions.comprehensive_location_check("- BEFORE SIGNUP")
                
                # Step 2: Switch back to main tab for signup process
                print("🔄 Switching back to main tab for signup...")
                self.driver.switch_to.window(first_tab)
            else:
                print("⚠️  Only one tab available, doing IP check in main tab")
                self.actions.comprehensive_location_check("- BEFORE SIGNUP")
            
            # Step 3: Navigate to English signup 
            self.go_to_google()
            self.actions.human_pause(1.0, 1.5)  # 🚀 FASTER
            
            # Step 2: Fill name
            self.fill_name_and_continue(
                first_name=self.data.get("first_name", "John"),
                last_name=self.data.get("last_name", "Doe")
            )
            self.actions.human_pause(1.0, 1.5)  # 🚀 FASTER

            # Step 3: Fill basic info
            self.fill_basic_info_and_continue(
                day=self.data.get("day", "15"),
                month=self.data.get("month", "5"),
                year=self.data.get("year", "2000"),
                gender=self.data.get("gender", "male")
            )
            self.actions.human_pause(1.0, 1.5)  # 🚀 FASTER

            # Step 4: Choose email method
            email_creation_method = self.data.get("email_method", "new")
            if email_creation_method == "new":
                self.choose_email_option(
                    email_choice_method="new",
                    username=self.data.get("username", "john.doe.12345chd")
                )
            else:
                self.choose_email_option(
                    email_choice_method="existing"
                )
                self.actions.human_pause(1.0, 1.5)  # 🚀 FASTER
                self.fill_existing_email_and_continue(
                    email_address=self.data.get("existing_email", "user@example.com")
                )
                self.actions.human_pause(1.0, 1.5)  # 🚀 FASTER
                self.verify_email_with_code(
                    otp_retrieval_method=self.data.get("otp_method", "manual")
                )
            
            self.actions.human_pause(1.0, 1.5)  # 🚀 FASTER

            # Step 5: Create password
            self.create_password_and_continue(
                password=self.data.get("password", "DefaultPassword@123")
            )
            self.actions.human_pause(1.5, 2.0)  # 🚀 FASTER
            
            # Step 6: Handle mobile number verification
            print("📱 Waiting for mobile verification page...")
            self.actions.human_pause(1.5, 2.0)  # 🚀 FASTER
            
            # Handle phone verification
            self.handle_phone_verification()
            
            # Step 8.5: Final location check
            self.actions.comprehensive_location_check("- AFTER SIGNUP COMPLETION")
            
            # Step 9: Keep browser open for manual control
            print("🎉 Automation completed!")
            print("🌐 Browser stays open for manual verification")
            print("💻 Console commands available in DevTools")
            
            # Add console controls
            self.driver.execute_script("""
                console.log('%c🎉 GOOGLE SIGNUP AUTOMATION COMPLETED!', 'color: green; font-size: 18px; font-weight: bold;');
                console.log('%c📝 Type "quit" to close browser', 'color: blue; font-size: 14px;');
                console.log('%c⏸️  Browser will stay open for manual verification', 'color: orange; font-size: 12px;');
                
                window.automationComplete = true;
                window.checkForQuit = function() {
                    if (window.shouldQuit) {
                        window.close();
                    } else {
                        setTimeout(window.checkForQuit, 1000);
                    }
                };
                window.checkForQuit();
            """)
            
            # Infinite loop to keep browser open
            print("♾️  Keeping browser open indefinitely...")
            while True:
                try:
                    should_quit = self.driver.execute_script("return window.shouldQuit || false;")
                    if should_quit:
                        print("👋 User requested quit")
                        break
                    time.sleep(5)
                except:
                    print("🔚 Browser closed externally")
                    break
            
        except Exception as e:
            print(f"❌ Signup automation failed: {e}")
            traceback.print_exc()
            self.actions.take_screenshot("error_screenshot.png")

    def natural_dropdown_selection(self, dropdown_element, option_text, dropdown_name="dropdown"):
        """
        Simple dropdown selection without mouse movements
        """
        try:
            print(f"🎯 {dropdown_name} selection: {option_text}")
            
            # Step 1: Click to open dropdown
            print(f"👆 Clicking {dropdown_name} to show the list...")
            self.actions.tap(dropdown_element)
            time.sleep(random.uniform(1.0, 1.5))
            print(f"✅ {dropdown_name} clicked - dropdown list should be visible")
            
            # Step 2: Random pause while looking at the list
            print(f"⏳ Pausing while looking at {dropdown_name} options...")
            pause_time = random.uniform(1.0, 1.5)
            time.sleep(pause_time)
            print(f"⏱️  Paused for {pause_time:.1f} seconds")
            
            # Step 3: Find and select the option
            print(f"🔍 Looking for '{option_text}' in dropdown...")
            
            simple_selectors = [
                f"//span[text()='{option_text}']",
                f"//li[contains(text(), '{option_text}')]",
                f"//div[contains(text(), '{option_text}')]"
            ]
            
            option_found = False
            for i, selector in enumerate(simple_selectors):
                try:
                    print(f"🔍 Trying selector {i+1}: {selector}")
                    option_element = self.driver.find_element(By.XPATH, selector)
                    print(f"✅ Found option using selector {i+1}")
                    
                    # Step 4: Click the option
                    print(f"👆 Clicking '{option_text}' option...")
                    self.actions.tap(option_element)
                    print(f"✅ {dropdown_name} option selected!")
                    
                    option_found = True
                    break
                except Exception as e:
                    print(f"⚠️ Selector {i+1} failed: {e}")
                    continue
            
            if not option_found:
                print(f"❌ Could not find {dropdown_name} option: {option_text}")
                return False
            
            # Step 5: Wait for dropdown to close
            print(f"⏳ Waiting for dropdown to close...")
            time.sleep(1)
            
            return True
            
        except Exception as e:
            print(f"❌ {dropdown_name} selection failed: {e}")
            return False


