import time
import random
import requests
import json
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException


class HumanActions:
    """Human-like automation actions for more natural browser interaction"""
    
    def __init__(self, driver, wait_timeout=10):
        self.driver = driver
        self.wait_timeout = wait_timeout  # Max 10 seconds for element waits
        self.wait = WebDriverWait(driver, wait_timeout)
    
    def human_pause(self, min_seconds=1, max_seconds=3):
        """Add human-like random pause between actions"""
        pause_time = random.uniform(min_seconds, max_seconds)
        print(f"⏳ Human pause: {pause_time:.2f}s")
        time.sleep(pause_time)
    
    def find_element(self, by, value, timeout=None):
        """Find element with explicit wait and error handling"""
        timeout = timeout or self.wait_timeout
        try:
            wait = WebDriverWait(self.driver, timeout)
            element = wait.until(EC.presence_of_element_located((by, value)))
            print(f"✅ Found element: {by}='{value}'")
            return element
        except TimeoutException:
            print(f"❌ Element not found: {by}='{value}' (timeout: {timeout}s)")
            raise
    
    def find_clickable_element(self, by, value, timeout=None):
        """Find element that is clickable"""
        timeout = timeout or self.wait_timeout
        try:
            wait = WebDriverWait(self.driver, timeout)
            element = wait.until(EC.element_to_be_clickable((by, value)))
            print(f"✅ Found clickable element: {by}='{value}'")
            return element
        except TimeoutException:
            print(f"❌ Clickable element not found: {by}='{value}' (timeout: {timeout}s)")
            raise
    
    def tap(self, element, add_pause=True):
        """Android-optimized tap with timeout protection and multiple fallback methods"""
        
        try:
            # Scroll element into view first
            self.driver.execute_script("arguments[0].scrollIntoView({block: 'center', behavior: 'smooth'});", element)
            self.human_pause(0.3, 0.8) if add_pause else None
            
            # Method 1: Fast JavaScript tap (skip problematic direct tap)
            print(f"📱 Trying JavaScript tap first...")
            self.driver.set_script_timeout(5)  # 5 second script timeout MAX
            self.driver.execute_script("arguments[0].click();", element)
            print(f"📱 JavaScript tap successful")
            if add_pause:
                self.human_pause(0.8, 1.5)
            return
            
        except Exception as js_error:
            print(f"⚠️  JavaScript tap failed: {js_error}")
            try:
                # Method 2: Force click with DOM event
                print(f"📱 Trying DOM event dispatch...")
                self.driver.execute_script("""
                    const element = arguments[0];
                    const event = new MouseEvent('click', {
                        view: window,
                        bubbles: true,
                        cancelable: true
                    });
                    element.dispatchEvent(event);
                """, element)
                print(f"📱 DOM event click successful")
                if add_pause:
                    self.human_pause(0.8, 1.5)
                return
            except Exception as dom_error:
                print(f"⚠️  DOM click failed: {dom_error}")
                try:
                    # Method 3: Try direct tap as last resort with short implicit wait
                    print(f"📱 Trying direct tap with short timeout...")
                    original_timeout = self.driver.implicitly_wait(0)
                    self.driver.implicitly_wait(3)  # 3 second implicit wait MAX
                    
                    element.click()
                    print(f"📱 Direct tap successful")
                    
                    self.driver.implicitly_wait(original_timeout)  # Restore
                    if add_pause:
                        self.human_pause(0.8, 1.5)
                    return
                except Exception as direct_error:
                    print(f"⚠️  Direct tap failed: {direct_error}")
                    try:
                        # Method 4: Form submit as absolute last resort
                        print(f"📱 Trying form submit fallback...")
                        self.driver.execute_script("arguments[0].closest('form').submit();", element)
                        print(f"📱 Form submit successful")
                        if add_pause:
                            self.human_pause(0.8, 1.5)
                        return
                    except Exception as submit_error:
                        print(f"❌ All tap methods failed: {submit_error}")
                        # Take screenshot for debugging
                        import time
                        screenshot_name = f"tap_failed_{int(time.time())}.png"
                        try:
                            self.driver.save_screenshot(screenshot_name)
                            print(f"📸 Debug screenshot saved: {screenshot_name}")
                        except:
                            pass
                        raise Exception("All tap methods failed - check screenshot for debugging")
    
    def click(self, element, add_pause=True):
        """Legacy click method - redirects to tap for Android compatibility"""
        return self.tap(element, add_pause)
    
    def typing(self, element, text, typing_speed="normal"):
        """Type text with human-like speed and behavior - Android optimized"""
        try:
            # Step 1: Activate/focus the field first (important for Google forms)
            print(f"📱 Activating field for typing...")
            try:
                # Scroll into view and TAP to activate (Android optimized)
                self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", element)
                self.human_pause(0.2, 0.4)
                
                # Use our tap method instead of click
                self.tap(element, add_pause=False)  # Activate the field
                print(f"✅ Field activated via tap")
                self.human_pause(0.3, 0.6)
            except Exception as activate_error:
                print(f"⚠️  Field tap activation failed: {activate_error}")
                # Try JavaScript focus as fallback
                try:
                    self.driver.execute_script("arguments[0].focus();", element)
                    print(f"✅ Field focused via JavaScript")
                except:
                    print(f"⚠️  JavaScript focus also failed")
            
            # Step 2: Clear field first
            try:
                element.clear()
                print(f"✅ Field cleared")
            except Exception as clear_error:
                print(f"⚠️  Clear failed, trying JavaScript: {clear_error}")
                try:
                    self.driver.execute_script("arguments[0].value = '';", element)
                    print(f"✅ Field cleared via JavaScript")
                except:
                    print(f"⚠️  JavaScript clear also failed")
            
            self.human_pause(0.2, 0.5)
            
            # Step 3: Set typing speed
            if typing_speed == "fast":
                min_delay, max_delay = 0.01, 0.05
            elif typing_speed == "slow":
                min_delay, max_delay = 0.1, 0.3
            else:  # normal
                min_delay, max_delay = 0.05, 0.15
            
            # Step 4: Type character by character
            for char in text:
                element.send_keys(char)
                if char != " ":  # Don't pause on spaces
                    time.sleep(random.uniform(min_delay, max_delay))
            
            print(f"⌨️  Typed text: '{text}' ({typing_speed} speed)")
            
        except Exception as e:
            print(f"❌ Typing failed: {e}")
            # Fallback to JavaScript input
            try:
                print(f"📱 Trying JavaScript input fallback...")
                self.driver.execute_script("arguments[0].value = arguments[1];", element, text)
                # Trigger input event to make sure the form recognizes the value
                self.driver.execute_script("""
                    const element = arguments[0];
                    const event = new Event('input', { bubbles: true });
                    element.dispatchEvent(event);
                """, element)
                print(f"⌨️  JavaScript input successful (fallback): '{text}'")
            except Exception as js_error:
                print(f"❌ JavaScript input also failed: {js_error}")
                # Final fallback - direct send_keys without clear
                try:
                    element.send_keys(text)
                    print(f"⌨️  Direct send_keys successful (final fallback): '{text}'")
                except Exception as final_error:
                    print(f"❌ All typing methods failed: {final_error}")
                    raise
    
    def scroll_to_element(self, element):
        """Scroll to element smoothly"""
        try:
            self.driver.execute_script("""
                arguments[0].scrollIntoView({
                    behavior: 'smooth',
                    block: 'center',
                    inline: 'center'
                });
            """, element)
            self.human_pause(1, 2)
            print(f"📜 Scrolled to element")
        except Exception as e:
            print(f"❌ Scroll failed: {e}")
    
    def wait_for_page_load(self, timeout=20):
        """Wait for page to fully load - MAX 20 seconds"""
        try:
            print(f"⏳ Waiting for page to load (max {timeout}s)...")
            # Wait for document ready state
            WebDriverWait(self.driver, timeout).until(
                lambda driver: driver.execute_script("return document.readyState") == "complete"
            )
            
            # Additional wait for dynamic content
            self.human_pause(1, 2)  # Reduced from 2-4 to 1-2
            print(f"📄 Page loaded successfully")
            
        except TimeoutException:
            print(f"⚠️  Page load timeout after {timeout}s")
            print(f"🔍 Current URL: {self.driver.current_url}")
            print(f"🔍 Page title: {self.driver.title}")
    
    def wait_and_tap(self, by, value, timeout=None):
        """Wait for element and tap it - Android optimized"""
        element = self.find_clickable_element(by, value, timeout)
        self.tap(element)
        return element
    
    def wait_and_click(self, by, value, timeout=None):
        """Legacy method - redirects to tap for Android compatibility"""
        return self.wait_and_tap(by, value, timeout)
    
    def wait_and_type(self, by, value, text, timeout=None, typing_speed="normal"):
        """Wait for element and type text"""
        element = self.find_element(by, value, timeout)
        self.typing(element, text, typing_speed)
        return element
    
    def take_screenshot(self, filename=None):
        """Take screenshot for debugging"""
        if not filename:
            timestamp = int(time.time())
            filename = f"screenshot_{timestamp}.png"
        
        try:
            self.driver.save_screenshot(filename)
            print(f"📸 Screenshot saved: {filename}")
            return filename
        except Exception as e:
            print(f"❌ Screenshot failed: {e}")
            return None
    
    def get_current_url(self):
        """Get current page URL"""
        try:
            url = self.driver.current_url
            print(f"🌐 Current URL: {url}")
            return url
        except Exception as e:
            print(f"❌ Failed to get URL: {e}")
            return None
    
    def wait_for_url_change(self, current_url, timeout=30):
        """Wait for URL to change from current URL"""
        try:
            WebDriverWait(self.driver, timeout).until(
                lambda driver: driver.current_url != current_url
            )
            new_url = self.driver.current_url
            print(f"🔄 URL changed to: {new_url}")
            return new_url
        except TimeoutException:
            print(f"⚠️  URL did not change within {timeout}s")
            return self.driver.current_url
    
    def check_ip_location(self, method="selenium"):
        """Check current IP and location using different methods"""
        print("🌍 Checking current IP and location...")
        
        if method == "selenium":
            # Method 1: Use Selenium to check IP via browser
            try:
                current_url = self.driver.current_url
                self.driver.get("https://ipinfo.io/json")
                self.human_pause(2, 3)
                
                # Get the JSON response from the page
                response_text = self.driver.find_element(By.TAG_NAME, "body").text
                ip_info = json.loads(response_text)
                
                print(f"📍 IP Location Info (via Selenium):")
                print(f"   🌐 IP: {ip_info.get('ip', 'Unknown')}")
                print(f"   🏙️  City: {ip_info.get('city', 'Unknown')}")
                print(f"   🗺️  Region: {ip_info.get('region', 'Unknown')}")
                print(f"   🇮🇳 Country: {ip_info.get('country', 'Unknown')}")
                print(f"   🕐 Timezone: {ip_info.get('timezone', 'Unknown')}")
                print(f"   🏢 Org: {ip_info.get('org', 'Unknown')}")
                
                # Navigate back to original URL
                if current_url and current_url != "data:,":
                    self.driver.get(current_url)
                    self.human_pause(1, 2)
                
                return ip_info
                
            except Exception as e:
                print(f"❌ Selenium IP check failed: {e}")
                return None
                
        elif method == "requests":
            # Method 2: Use direct requests (this will use your real IP, not browser proxy)
            try:
                response = requests.get("https://ipinfo.io/json", timeout=10)
                ip_info = response.json()
                
                print(f"📍 IP Location Info (via Direct Request - Real IP):")
                print(f"   🌐 IP: {ip_info.get('ip', 'Unknown')}")
                print(f"   🏙️  City: {ip_info.get('city', 'Unknown')}")
                print(f"   🗺️  Region: {ip_info.get('region', 'Unknown')}")
                print(f"   🇮🇳 Country: {ip_info.get('country', 'Unknown')}")
                print(f"   🕐 Timezone: {ip_info.get('timezone', 'Unknown')}")
                
                return ip_info
                
            except Exception as e:
                print(f"❌ Direct request IP check failed: {e}")
                return None
    
    def check_google_location(self):
        """Check what location Google thinks we're in"""
        print("🗺️  Checking Google's location detection...")
        
        try:
            current_url = self.driver.current_url
            self.driver.get("https://www.google.com/search?q=my+location")
            self.human_pause(3, 5)
            
            # Look for location information in the search results
            try:
                location_elements = self.driver.find_elements(By.XPATH, "//*[contains(text(), 'Based on your IP address') or contains(text(), 'Your location') or contains(text(), 'From your IP address')]")
                
                for element in location_elements:
                    print(f"🏷️  Google location info: {element.text}")
                    
            except:
                print("ℹ️  Could not find specific Google location text")
            
            # Check if there are any location-based results
            page_text = self.driver.find_element(By.TAG_NAME, "body").text
            if "Jaipur" in page_text:
                print("✅ Jaipur detected in Google results!")
            elif "India" in page_text:
                print("🇮🇳 India detected in Google results")
            else:
                print("⚠️  No India/Jaipur location detected in Google results")
            
            # Navigate back
            if current_url and current_url != "data:,":
                self.driver.get(current_url)
                self.human_pause(1, 2)
                
        except Exception as e:
            print(f"❌ Google location check failed: {e}")
    
    def comprehensive_location_check(self, stage=""):
        """Run comprehensive location checking"""
        print(f"\n{'='*60}")
        print(f"🔍 COMPREHENSIVE LOCATION CHECK {stage}")
        print(f"{'='*60}")
        
        # Check 1: Browser IP (what websites see)
        print("\n1️⃣  Browser IP Check (What websites see):")
        browser_ip = self.check_ip_location("selenium")
        
        # Check 2: Real IP (bypass proxy)
        print("\n2️⃣  Direct Request IP Check (Your real IP):")
        real_ip = self.check_ip_location("requests")
        
        # Check 3: Google's location detection
        print("\n3️⃣  Google Location Detection:")
        self.check_google_location()
        
        print(f"{'='*60}\n")
        
        return {
            "browser_ip": browser_ip,
            "real_ip": real_ip,
            "stage": stage
        }
