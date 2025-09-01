

import time
from gologin import GoLogin
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
# Use the actual profile ID
profile_id = "68aff3c19446e61259e7c087"  # Primary profile
# profile_id = "BACKUP_PROFILE_ID"  # If you have another profile to test

# Initialize GoLogin
gl = GoLogin({
	"token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiI2OGFmZTQ1YjljZWJhOWU1ODUxYjRkY2QiLCJ0eXBlIjoiZGV2Iiwiand0aWQiOiI2OGFmZTU4YTI0MjYyYTZhNWRkNGRmNzUifQ.o9KzAg9lmh0MxPOimC-dv9_hqtYpHUtEhGhMth9JK-o",
	"profile_id": profile_id
	})

# Try to clear any existing proxy before starting
try:
    print("🔧 Attempting to clear proxy settings for testing...")
    gl.deleteGologinProxyFromProfile(profile_id)
    print("✅ Proxy cleared successfully")
except:
    print("⚠️  Could not clear proxy (may not exist)")
    pass

# 🔧 FORCE STOP any running instance of this profile
try:
    print("🛑 Force stopping any running instance of profile...")
    gl.stop()
    time.sleep(3)  # Wait for cleanup
    print("✅ Profile stopped successfully")
except:
    print("⚠️  Profile was not running (or stop failed)")
    pass

# Start Browser and get websocket url with retry logic
max_retries = 3
for attempt in range(max_retries):
    try:
        print(f"🚀 Starting GoLogin (attempt {attempt + 1}/{max_retries})...")
        debugger_address = gl.start()
        print("✅ GoLogin started successfully!")
        break
    except Exception as e:
        print(f"❌ Attempt {attempt + 1} failed: {e}")
        if attempt < max_retries - 1:
            wait_time = (attempt + 1) * 30  # Wait 30, 60, 90 seconds
            print(f"⏳ Waiting {wait_time} seconds before retry...")
            time.sleep(wait_time)
        else:
            print("💥 All attempts failed. This suggests:")
            print("   1. 🕐 API rate limiting (wait 5-10 minutes)")
            print("   2. 🔒 Profile locked/running elsewhere") 
            print("   3. 🌐 GoLogin server issues")
            print("   4. 🔑 Token/authentication problems")
            print("\n🛠️  Try:")
            print("   • Close profile in GoLogin dashboard")
            print("   • Wait 10 minutes and try again")
            print("   • Check if profile is running manually")
            raise e

# Get Chromium version for webdriver
chromium_version = gl.get_chromium_version()

# Add proxy to profile
# gl.addGologinProxyToProfile(profile_id, "us")  # Commented out to use iRoyal Jaipur proxy instead

# Install webdriver
service = Service(ChromeDriverManager(driver_version=chromium_version).install())

chrome_options = webdriver.ChromeOptions()
chrome_options.add_experimental_option("debuggerAddress", debugger_address)

# 🌍 MINIMAL BROWSER SETUP - Let natural language detection work
print("🌍 Setting up browser with minimal language interference...")

# 🔧 BASIC CHROME PREFERENCES (no language forcing)
chrome_options.add_argument("--disable-translate")  # Keep translation disabled for automation

# 🔧 MINIMAL PREFERENCES - Just essentials
chrome_options.add_experimental_option("prefs", {
    # Translation disabled for automation stability
    "translate.enabled": False,
    
    # Location settings (keep blocked for privacy)
    "profile.default_content_setting_values.geolocation": 2,
    "profile.managed_default_content_settings.geolocation": 2,
    
    # Basic browser settings
    "browser.enable_spellchecking": True,
    "webkit.webprefs.default_encoding": "UTF-8"
})

driver = webdriver.Chrome(service=service, options=chrome_options)

print("🚀 Browser launched successfully!")

# 🔧 FIRST STEP: Open TWO TABS immediately (as requested)
print("📱 Opening second tab FIRST...")
try:
    driver.execute_script("window.open('about:blank', '_blank');")
    time.sleep(2)
    
    # Verify two tabs exist
    if len(driver.window_handles) >= 2:
        print(f"✅ TWO TABS created successfully! Total: {len(driver.window_handles)}")
        # Switch back to first tab for setup
        driver.switch_to.window(driver.window_handles[0])
        print("🔄 Switched back to main tab for setup")
    else:
        print("⚠️  Second tab creation failed, continuing with single tab")
        
except Exception as e:
    print(f"⚠️  Tab creation failed: {e}, continuing with single tab")

# 🔧 SIMPLIFIED: Environment setup ONLY (no IP checks - that's for second tab)
print("🔧 Setting up basic environment...")

def setup_basic_environment(driver):
    """Set up basic environment (timezone only, no language forcing)"""
    try:
        print("🇮🇳 Setting basic Indian environment (timezone only)...")
        
        # Clear cache and cookies to remove any conflicting data
        print("🧹 Clearing browser cache and cookies...")
        driver.delete_all_cookies()
        driver.execute_script("window.localStorage.clear();")
        driver.execute_script("window.sessionStorage.clear();")
        
        # Apply basic environment setup (timezone only, no language forcing)
        basic_script = """
        // ===== TIMEZONE SETUP ONLY =====
        Date.prototype.getTimezoneOffset = function() {
            return -330; // IST is UTC+5:30 = -330 minutes
        };
        
        // Set basic preferences in localStorage (no language forcing)
        try {
            localStorage.setItem('country', 'IN');
            localStorage.setItem('region', 'IN');
            localStorage.setItem('timezone', 'Asia/Kolkata');
        } catch(e) {}
        
        console.log('🇮🇳 Basic Indian environment applied (timezone only)');
        """
        
        driver.execute_script(basic_script)
        print("✅ Basic Indian environment applied for Android profile")
                
    except Exception as e:
        print(f"⚠️  Environment setup failed: {e}, continuing anyway")

# Apply basic environment setup (no language forcing)
setup_basic_environment(driver)

print("🔗 GoLogin profile connected with consistent environment")

# Import and initialize Enhanced Google Signup Automation (with integrated improvements)
try:
    from app.google_signup_automation import GoogleSignupAutomation
    
    # Create automation instance
    automation = GoogleSignupAutomation(driver)
    
    # Configure automation data (using search-based navigation + tap optimization + mobile verification)
    automation.set_data(
        first_name="love",
        last_name="Sharma",  
        day="2",
        month="5",
        year="1999",
        gender="male",
        email_method="new",  # "new" for Gmail or "existing" for existing email
        username="loyurn123mujdelh",  # For new Gmail
        # existing_email="user@example.com",  # For existing email method
        # otp_method="manual",  # For existing email verification
        password="@mayank123",
        mobile_number="+919842901727",  # Mobile number for verification
        qr_save_path="google_signup_qr.png",
        network_save_path="sms_network_calls.json"
    )
    
    print("✅ Enhanced Android-Optimized Google Signup configured")
    print("🔍 Using search-based navigation + tap interactions")
    print("📱 Starting automated signup process with mobile verification...")
    
    # Run the signup including mobile verification (as requested)
    automation.signup_until_mobile_verification()
    
except ImportError as e:
    print(f"❌ Failed to import automation: {e}")
    print("📄 Running basic browser test instead...")
    driver.get("http://www.python.org")
    time.sleep(30)
    
except Exception as e:
    print(f"❌ Automation failed: {e}")
    print("📄 Browser will remain open for manual use...")
    time.sleep(300)  # Keep open for 5 minutes

# Cleanup will be handled by the automation
# Browser stays open until manual quit or automation completion
