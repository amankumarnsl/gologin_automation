import time
import random
from gologin import GoLogin
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager

# Use the actual profile ID
profile_id = "68b84865b16815cb4309701a"  # Primary profile

# Initialize GoLogin
gl = GoLogin({
   "token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiI2OGI4NDZiMjYxMzcwMzY0NzU3YWU3N2EiLCJ0eXBlIjoiZGV2Iiwiand0aWQiOiI2OGI4NDg3YzYxMzcwMzY0NzU3ZDU1MTQifQ.lEN5_aPKqIjZGvGvcN7gBl5eFITp9L3AHuE4oVEDlbs",
   "profile_id": profile_id
   })

# 🔧 CLEANUP: Stop any running instances and clear proxy
try:
   print("🛑 Stopping any running profile instances...")
   gl.stop()
   time.sleep(2)
   print("✅ Profile stopped successfully")
except Exception as e:
   print(f"⚠️  Stop failed: {e}")

try:
   print("🔧 Clearing proxy settings...")
   gl.deleteGologinProxyFromProfile(profile_id)
   print("✅ Proxy cleared successfully")
except Exception as e:
   print(f"⚠️  Proxy clear failed: {e}")

# 🚀 START BROWSER with robust retry logic
max_retries = 3
debugger_address = None

for attempt in range(max_retries):
   try:
       print(f"🚀 Starting GoLogin (attempt {attempt + 1}/{max_retries})...")
       debugger_address = gl.start()
       print(f"✅ GoLogin started successfully! Debugger: {debugger_address}")
       break
   except Exception as e:
       print(f"❌ Attempt {attempt + 1} failed: {e}")
       if attempt < max_retries - 1:
           wait_time = (attempt + 1) * 10  # Shorter waits: 10, 20, 30 seconds
           print(f"⏳ Waiting {wait_time} seconds before retry...")
           time.sleep(wait_time)
       else:
           print("💥 All attempts failed. Please check:")
           print("   • GoLogin dashboard for profile status")
           print("   • Token validity")
           print("   • Network connection")
           raise e

if not debugger_address:
   raise Exception("Failed to get debugger address")

# 🔧 ENHANCED ANTI-DETECTION CHROME OPTIONS
chrome_options = webdriver.ChromeOptions()
chrome_options.add_experimental_option("debuggerAddress", debugger_address)

# 🎯 COMPREHENSIVE ANTI-DETECTION ARGUMENTS
chrome_options.add_argument("--no-sandbox")
chrome_options.add_argument("--disable-dev-shm-usage")
chrome_options.add_argument("--disable-blink-features=AutomationControlled")
chrome_options.add_argument("--disable-extensions")
chrome_options.add_argument("--disable-translate")
chrome_options.add_argument("--no-first-run")
chrome_options.add_argument("--disable-default-apps")
chrome_options.add_argument("--disable-web-security")
chrome_options.add_argument("--allow-running-insecure-content")
chrome_options.add_argument("--disable-features=VizDisplayCompositor")
chrome_options.add_argument("--disable-background-timer-throttling")
chrome_options.add_argument("--disable-backgrounding-occluded-windows")
chrome_options.add_argument("--disable-renderer-backgrounding")
chrome_options.add_argument("--disable-field-trial-config")
chrome_options.add_argument("--disable-ipc-flooding-protection")
chrome_options.add_argument("--disable-hang-monitor")
chrome_options.add_argument("--disable-prompt-on-repost")
chrome_options.add_argument("--disable-client-side-phishing-detection")
chrome_options.add_argument("--disable-component-update")
chrome_options.add_argument("--disable-domain-reliability")
chrome_options.add_argument("--disable-background-networking")
chrome_options.add_argument("--disable-sync")
chrome_options.add_argument("--metrics-recording-only")
chrome_options.add_argument("--no-default-browser-check")
chrome_options.add_argument("--disable-popup-blocking")
chrome_options.add_argument("--disable-password-generation")
chrome_options.add_argument("--disable-single-click-autofill")
chrome_options.add_argument("--disable-autofill-keyboard-accessory-view")
chrome_options.add_argument("--disable-credit-card-autofill")
chrome_options.add_argument("--disable-address-and-more-form-autofill")
chrome_options.add_argument("--disable-features=TranslateUI")
chrome_options.add_argument("--disable-features=BlinkGenPropertyTrees")

# 🔧 ENHANCED PREFERENCES - Anti-detection focused
chrome_options.add_experimental_option("prefs", {
   # Translation and language
   "translate.enabled": False,
   "translate_whitelists": {},
   "translate_blocked_languages": ["*"],
   
   # Location and permissions
   "profile.default_content_setting_values.geolocation": 2,
   "profile.managed_default_content_settings.geolocation": 2,
   "profile.default_content_setting_values.notifications": 2,
   "profile.default_content_setting_values.media_stream_mic": 2,
   "profile.default_content_setting_values.media_stream_camera": 2,
   "profile.default_content_setting_values.protocol_handlers": 2,
   
   # Autofill and forms
   "autofill.profile_enabled": False,
   "autofill.credit_card_enabled": False,
   "profile.password_manager_enabled": False,
   "credentials_enable_service": False,
   "credentials_enable_autosignin": False,
   
   # Download and security
   "download.prompt_for_download": False,
   "download.directory_upgrade": True,
   "safebrowsing.enabled": False,
   "safebrowsing.disable_download_protection": True,
   
   # Browser behavior
   "browser.enable_spellchecking": True,
   "webkit.webprefs.default_encoding": "UTF-8",
   "intl.accept_languages": "en-US,en-IN,en",
   
   # Privacy and tracking
   "search.suggest.enabled": False,
   "alternate_error_pages.enabled": False,
   "profile.block_third_party_cookies": False,
   "profile.default_content_setting_values.cookies": 1,
   
   # Network and performance
   "net.network_prediction_options": 2,
   "dns_prefetching.enabled": False,
   "predictors.enabled": False,
   
   # Automation detection prevention
   "profile.managed_default_content_settings.images": 1,
   "profile.default_content_setting_values.plugins": 1,
   "profile.content_settings.plugin_whitelist": {},
   
   # Mobile-specific settings
   "profile.default_content_setting_values.mixed_script": 1,
   "profile.default_content_setting_values.media_stream": 2,
   "profile.default_content_setting_values.media_stream_mic": 2,
   "profile.default_content_setting_values.media_stream_camera": 2,
   "profile.default_content_setting_values.protocol_handlers": 2,
   "profile.default_content_setting_values.ppapi_broker": 2,
   "profile.default_content_setting_values.automatic_downloads": 1,
   "profile.default_content_setting_values.midi_sysex": 2,
   "profile.default_content_setting_values.push_messaging": 2,
   "profile.default_content_setting_values.ssl_cert_decisions": 2,
   "profile.default_content_setting_values.metro_switch_to_desktop": 2,
   "profile.default_content_setting_values.protected_media_identifier": 2,
   "profile.default_content_setting_values.app_banner": 2,
   "profile.default_content_setting_values.site_engagement": 2,
   "profile.default_content_setting_values.durable_storage": 2
})

# 🎯 MOBILE USER AGENT
chrome_options.add_argument('--user-agent=Mozilla/5.0 (Linux; Android 11; SM-G991B) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/138.0.0.0 Mobile Safari/537.36')

# 🔧 ADDITIONAL ANTI-DETECTION EXPERIMENTAL OPTIONS
# Note: Some experimental options are not compatible with this ChromeDriver version

# 🔧 GET CHROMIUM VERSION and install webdriver
try:
   chromium_version = gl.get_chromium_version()
   print(f"🔧 Chromium version: {chromium_version}")
   service = Service(ChromeDriverManager(driver_version=chromium_version).install())
except Exception as e:
   print(f"⚠️  Could not get Chromium version: {e}")
   print("🔄 Using default ChromeDriver...")
   service = Service(ChromeDriverManager().install())

# 🚀 INITIALIZE DRIVER with error handling
try:
   print("🚀 Initializing Chrome driver...")
   driver = webdriver.Chrome(service=service, options=chrome_options)
   print("✅ Chrome driver initialized successfully!")
except Exception as e:
   print(f"❌ Driver initialization failed: {e}")
   raise e

# 🔧 COMPREHENSIVE STEALTH - Anti-detection focused
try:
   print("🔧 Applying comprehensive stealth enhancements...")
   driver.execute_script("""
       // ===== COMPREHENSIVE ANTI-DETECTION SCRIPT =====
       
       // Remove webdriver property
       Object.defineProperty(navigator, 'webdriver', {
           get: () => undefined,
       });
       
       // Mock chrome runtime
       window.chrome = {
           runtime: {},
           loadTimes: function() {},
           csi: function() {},
           app: {}
       };
       
       // Mock plugins
       Object.defineProperty(navigator, 'plugins', {
           get: () => [1, 2, 3, 4, 5],
       });
       
       // Mock languages
       Object.defineProperty(navigator, 'languages', {
           get: () => ['en-US', 'en', 'en-IN'],
       });
       
       // Mock permissions
       const originalQuery = window.navigator.permissions.query;
       window.navigator.permissions.query = (parameters) => (
           parameters.name === 'notifications' ?
               Promise.resolve({ state: Notification.permission }) :
               originalQuery(parameters)
       );
       
       // Mock webdriver
       Object.defineProperty(navigator, 'webdriver', {
           get: () => undefined,
       });
       
       // Mock automation
       Object.defineProperty(navigator, 'automation', {
           get: () => undefined,
       });
       
       // Mock connection
       Object.defineProperty(navigator, 'connection', {
           get: () => ({
               effectiveType: '4g',
               type: 'cellular',
               downlink: 10,
               rtt: 50,
               saveData: false
           }),
       });
       
       // Mock hardware concurrency
       Object.defineProperty(navigator, 'hardwareConcurrency', {
           get: () => 8,
       });
       
       // Mock device memory
       Object.defineProperty(navigator, 'deviceMemory', {
           get: () => 4,
       });
       
       // Mock platform
       Object.defineProperty(navigator, 'platform', {
           get: () => 'Linux armv8l',
       });
       
       // Mock user agent data
       if (navigator.userAgentData) {
           Object.defineProperty(navigator, 'userAgentData', {
               get: () => ({
                   brands: [
                       { brand: 'Chromium', version: '138' },
                       { brand: 'Google Chrome', version: '138' },
                       { brand: 'Not=A?Brand', version: '8' }
                   ],
                   mobile: true,
                   platform: 'Android'
               }),
           });
       }
       
       // Mock battery API
       navigator.getBattery = () => Promise.resolve({
           charging: Math.random() > 0.5,
           chargingTime: Infinity,
           dischargingTime: Math.random() * 28800 + 7200,
           level: Math.random() * 0.5 + 0.5
       });
       
       // Mock screen properties
       Object.defineProperty(screen, 'availWidth', { value: 412 });
       Object.defineProperty(screen, 'availHeight', { value: 869 });
       Object.defineProperty(screen, 'width', { value: 412 });
       Object.defineProperty(screen, 'height', { value: 915 });
       Object.defineProperty(screen, 'colorDepth', { value: 24 });
       Object.defineProperty(screen, 'pixelDepth', { value: 24 });
       
       // Mock touch support
       Object.defineProperty(navigator, 'maxTouchPoints', { value: 10 });
       
       // Mock permissions
       const originalGetUserMedia = navigator.mediaDevices.getUserMedia;
       navigator.mediaDevices.getUserMedia = function(constraints) {
           return Promise.reject(new Error('Permission denied'));
       };
       
       // Mock geolocation
       navigator.geolocation.getCurrentPosition = function(success, error, options) {
           setTimeout(() => {
               if (success) {
                   success({
                       coords: {
                           latitude: 30.7333,
                           longitude: 76.7794,
                           accuracy: 20,
                           altitude: null,
                           altitudeAccuracy: null,
                           heading: null,
                           speed: null
                       },
                       timestamp: Date.now()
                   });
               }
           }, Math.random() * 1000 + 100);
       };
       
       // Mock canvas fingerprinting
       const originalGetContext = HTMLCanvasElement.prototype.getContext;
       HTMLCanvasElement.prototype.getContext = function(type, ...args) {
           const context = originalGetContext.call(this, type, ...args);
           if (type === '2d') {
               const originalFillText = context.fillText;
               context.fillText = function(...args) {
                   return originalFillText.apply(this, args);
               };
           }
           return context;
       };
       
       // Mock webGL fingerprinting
       const getParameter = WebGLRenderingContext.prototype.getParameter;
       WebGLRenderingContext.prototype.getParameter = function(parameter) {
           if (parameter === 37445) {
               return 'Intel Inc.';
           }
           if (parameter === 37446) {
               return 'Intel(R) Iris(TM) Graphics 6100';
           }
           return getParameter.call(this, parameter);
       };
       
       // Mock audio fingerprinting
       const originalGetChannelData = AudioBuffer.prototype.getChannelData;
       AudioBuffer.prototype.getChannelData = function(channel) {
           const data = originalGetChannelData.call(this, channel);
           const noise = new Float32Array(data.length);
           for (let i = 0; i < data.length; i++) {
               noise[i] = data[i] + (Math.random() - 0.5) * 0.0001;
           }
           return noise;
       };
       
       // Mock timezone
       Date.prototype.getTimezoneOffset = function() {
           return -330; // IST
       };
       
       // Mock time
       const originalNow = Date.now;
       Date.now = function() {
           return originalNow() + (Math.random() - 0.5) * 100;
       };
       
       // Mock localStorage
       try {
           localStorage.setItem('country', 'IN');
           localStorage.setItem('timezone', 'Asia/Kolkata');
           localStorage.setItem('locale', 'en-IN');
           localStorage.setItem('currency', 'INR');
       } catch(e) {}
       
       console.log('Comprehensive stealth applied successfully');
   """)
   print("✅ Comprehensive stealth applied!")
except Exception as e:
   print(f"⚠️  Stealth failed: {e}, continuing anyway...")

# 🔧 REALISTIC ENVIRONMENT SETUP - Session context management
def setup_realistic_environment(driver):
   """Set up realistic environment with session context management"""
   try:
       print("🇮🇳 Setting up realistic Indian environment...")
       
       # Don't clear everything - keep some realistic browser state
       # Only clear specific automation-related data
       driver.execute_script("""
           // Clear only automation-related data, keep realistic browser state
           if (sessionStorage.getItem('automation_flag')) {
               sessionStorage.clear();
           }
           if (localStorage.getItem('automation_detected')) {
               localStorage.removeItem('automation_detected');
           }
       """)
       
       # Realistic environment script with session context management
       realistic_script = """
       // ===== REALISTIC ENVIRONMENT SETUP WITH SESSION MANAGEMENT =====
       
       // Enhanced timezone override
       Date.prototype.getTimezoneOffset = function() {
           return -330; // IST
       };
       
       // Override Date constructor for consistent timezone
       const OriginalDate = Date;
       Date = function(...args) {
           if (args.length === 0) {
               const now = new OriginalDate();
               return new OriginalDate(now.getTime() + (330 * 60 * 1000));
           }
           return new OriginalDate(...args);
       };
       Date.prototype = OriginalDate.prototype;
       Date.now = function() {
           return OriginalDate.now() + (330 * 60 * 1000);
       };
       
       // Realistic localStorage setup - only set if not already present
       try {
           if (!localStorage.getItem('country')) localStorage.setItem('country', 'IN');
           if (!localStorage.getItem('timezone')) localStorage.setItem('timezone', 'Asia/Kolkata');
           if (!localStorage.getItem('locale')) localStorage.setItem('locale', 'en-IN');
           if (!localStorage.getItem('language')) localStorage.setItem('language', 'en-US');
       } catch(e) {}
       
       // Session context management
       let sessionContext = {
           isHuman: true,
           interactionCount: 0,
           lastInteraction: Date.now(),
           sessionStart: Date.now()
       };
       
       // Store session context
       sessionStorage.setItem('session_context', JSON.stringify(sessionContext));
       
       // Monitor and update session context
       setInterval(() => {
           try {
               let context = JSON.parse(sessionStorage.getItem('session_context') || '{}');
               context.lastInteraction = Date.now();
               context.isHuman = true;
               sessionStorage.setItem('session_context', JSON.stringify(context));
           } catch(e) {}
       }, 5000);
       
       // Mock Intl API
       const originalResolvedOptions = Intl.DateTimeFormat.prototype.resolvedOptions;
       Intl.DateTimeFormat.prototype.resolvedOptions = function() {
           const options = originalResolvedOptions.call(this);
           options.timeZone = 'Asia/Kolkata';
           return options;
       };
       
       // Mock performance timing
       if (window.performance && window.performance.timing) {
           const timing = window.performance.timing;
           timing.navigationStart = Date.now() - Math.random() * 10000;
           timing.loadEventEnd = timing.navigationStart + Math.random() * 5000;
       }
       
       // Mock performance memory
       if (window.performance && window.performance.memory) {
           Object.defineProperty(window.performance, 'memory', {
               value: {
                   usedJSHeapSize: Math.floor(Math.random() * 50000000) + 10000000,
                   totalJSHeapSize: Math.floor(Math.random() * 100000000) + 50000000,
                   jsHeapSizeLimit: 2147483648
               }
           });
       }
       
       // Mock device pixel ratio
       Object.defineProperty(window, 'devicePixelRatio', {
           get: () => 2.5
       });
       
       // Mock inner dimensions
       Object.defineProperty(window, 'innerWidth', { value: 412 });
       Object.defineProperty(window, 'innerHeight', { value: 869 });
       Object.defineProperty(window, 'outerWidth', { value: 412 });
       Object.defineProperty(window, 'outerHeight', { value: 915 });
       
       // Mock viewport
       Object.defineProperty(window, 'visualViewport', {
           value: {
               width: 412,
               height: 869,
               scale: 1,
               offsetLeft: 0,
               offsetTop: 0
           }
       });
       
       console.log('Realistic Indian environment with session management applied successfully');
       """
       
       driver.execute_script(realistic_script)
       print("✅ Realistic environment with session management applied")
       
       # Add some natural behavior
       driver.execute_script("window.scrollTo(0, Math.random() * 100);")
       time.sleep(0.5)
       
   except Exception as e:
       print(f"⚠️  Environment setup failed: {e}, continuing anyway")

# Apply realistic environment
setup_realistic_environment(driver)

# 🔧 REALISTIC BROWSER SETUP - Single tab only
print("🌐 Setting up realistic single-tab browser...")

# 🔧 ENHANCED WAIT - More reliable
wait = WebDriverWait(driver, 15)
print("🚀 Browser ready with enhanced stability!")

# Import and run automation
try:
   from app.google_signup_automation import GoogleSignupAutomation
   
   # Create automation instance
   automation = GoogleSignupAutomation(driver)
   
   # Configure data
   automation.set_data(
       first_name="Rahul",
       last_name="Verma",  
       day="12",
       month="3",
       year="2003",
       gender="male",
       email_method="new",
       username="vrmarahul123del",
       password="@verma123",
       mobile_number="+918912983454",
       qr_save_path="google_signup_qr.png",
       network_save_path="sms_network_calls.json"
   )
   
   print("✅ Enhanced Google Signup configured")
   print("🔍 Using robust button detection + tap interactions")
   print("📱 Starting automated signup process...")
   
   # Run signup
   automation.signup_until_mobile_verification()
   
except ImportError as e:
   print(f"❌ Import failed: {e}")
   print("📄 Running basic test...")
   driver.get("https://www.google.com")
   time.sleep(10)
   
except Exception as e:
   print(f"❌ Automation failed: {e}")
   print("📄 Browser will remain open for manual use...")
   time.sleep(300)

print("🏁 Script completed")