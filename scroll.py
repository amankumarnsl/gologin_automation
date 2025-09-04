import time
import random
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import pyautogui


# =============================================================================
# PURE SCROLL LOGIC - MODULAR FUNCTIONS
# =============================================================================

class ScrollController:
    """
    Pure scroll logic controller with directional functions - can be imported and used from other files
    """
    
    def __init__(self, driver):
        self.driver = driver
        self.body = None
        self._focus_page()
    
    def _focus_page(self):
        """Focus on page body for keyboard input"""
        self.body = self.driver.find_element(By.TAG_NAME, "body")
        self.body.click()
    
    def _get_speed_timing(self, progress):
        """Get human-like speed timing based on progress (0.0 to 1.0)"""
        if progress < 0.3:
            return random.uniform(0.8, 1.2)  # Fast start
        elif progress < 0.7:
            return random.uniform(1.5, 2.2)  # Medium speed
        else:
            return random.uniform(2.5, 3.5)  # Slow end
    
    # =============================================================================
    # KEYBOARD SCROLL FUNCTIONS - FOUR DIRECTIONS
    # =============================================================================
    
    def keyboard_scroll_down(self, amount=3, show_progress=True):
        """Keyboard scroll down using ARROW_DOWN"""
        if show_progress:
            print(f"⌨️ Keyboard scrolling DOWN x{amount}")
        
        for i in range(amount):
            self.body.send_keys(Keys.ARROW_DOWN)
            
            # Human-like speed variation
            progress = i / (amount - 1) if amount > 1 else 0
            timing = self._get_speed_timing(progress)
            
            if show_progress:
                speed_type = "Fast" if progress < 0.3 else "Medium" if progress < 0.7 else "Slow"
                print(f"🚀 {speed_type} scroll down {i+1} - {timing:.1f}s")
            
            # Apply timing (don't pause after last scroll)
            if i < amount - 1:
                time.sleep(timing)
        
        # Reading pause
        reading_pause = random.uniform(2.0, 3.5)
        if show_progress:
            print(f"👁️ Reading pause: {reading_pause:.1f}s")
        time.sleep(reading_pause)
    
    def keyboard_scroll_up(self, amount=3, show_progress=True):
        """Keyboard scroll up using ARROW_UP"""
        if show_progress:
            print(f"⌨️ Keyboard scrolling UP x{amount}")
        
        for i in range(amount):
            self.body.send_keys(Keys.ARROW_UP)
            
            # Human-like speed variation
            progress = i / (amount - 1) if amount > 1 else 0
            timing = self._get_speed_timing(progress)
            
            if show_progress:
                speed_type = "Fast" if progress < 0.3 else "Medium" if progress < 0.7 else "Slow"
                print(f"🚀 {speed_type} scroll up {i+1} - {timing:.1f}s")
            
            # Apply timing (don't pause after last scroll)
            if i < amount - 1:
                time.sleep(timing)
        
        # Reading pause
        reading_pause = random.uniform(2.0, 3.5)
        if show_progress:
            print(f"👁️ Reading pause: {reading_pause:.1f}s")
        time.sleep(reading_pause)
    
    def keyboard_scroll_left(self, amount=3, show_progress=True):
        """Keyboard scroll left using ARROW_LEFT"""
        if show_progress:
            print(f"⌨️ Keyboard scrolling LEFT x{amount}")
        
        for i in range(amount):
            self.body.send_keys(Keys.ARROW_LEFT)
            
            # Human-like speed variation
            progress = i / (amount - 1) if amount > 1 else 0
            timing = self._get_speed_timing(progress)
            
            if show_progress:
                speed_type = "Fast" if progress < 0.3 else "Medium" if progress < 0.7 else "Slow"
                print(f"🚀 {speed_type} scroll left {i+1} - {timing:.1f}s")
            
            # Apply timing (don't pause after last scroll)
            if i < amount - 1:
                time.sleep(timing)
        
        # Reading pause
        reading_pause = random.uniform(2.0, 3.5)
        if show_progress:
            print(f"👁️ Reading pause: {reading_pause:.1f}s")
        time.sleep(reading_pause)
    
    def keyboard_scroll_right(self, amount=3, show_progress=True):
        """Keyboard scroll right using ARROW_RIGHT"""
        if show_progress:
            print(f"⌨️ Keyboard scrolling RIGHT x{amount}")
        
        for i in range(amount):
            self.body.send_keys(Keys.ARROW_RIGHT)
            
            # Human-like speed variation
            progress = i / (amount - 1) if amount > 1 else 0
            timing = self._get_speed_timing(progress)
            
            if show_progress:
                speed_type = "Fast" if progress < 0.3 else "Medium" if progress < 0.7 else "Slow"
                print(f"🚀 {speed_type} scroll right {i+1} - {timing:.1f}s")
            
            # Apply timing (don't pause after last scroll)
            if i < amount - 1:
                time.sleep(timing)
        
        # Reading pause
        reading_pause = random.uniform(2.0, 3.5)
        if show_progress:
            print(f"👁️ Reading pause: {reading_pause:.1f}s")
        time.sleep(reading_pause)
    
    # =============================================================================
    # MOUSE WHEEL SCROLL FUNCTIONS - TWO DIRECTIONS
    # =============================================================================
    
    def mouse_scroll_down(self, amount=3, show_progress=True):
        """Mouse wheel scroll down"""
        if show_progress:
            print(f"🖱️ Mouse wheel scrolling DOWN x{amount}")
        
        for i in range(amount):
            pyautogui.scroll(1)  # Scroll down
            
            # Human-like speed variation
            progress = i / (amount - 1) if amount > 1 else 0
            
            if progress < 0.3:
                timing = random.uniform(0.1, 0.3)
            elif progress < 0.7:
                timing = random.uniform(0.4, 0.8)
            else:
                timing = random.uniform(1.0, 1.8)
            
            if show_progress:
                speed_type = "Fast" if progress < 0.3 else "Medium" if progress < 0.7 else "Slow"
                print(f"🚀 {speed_type} wheel down {i+1} - {timing:.1f}s")
            
            # Apply timing (don't pause after last scroll)
            if i < amount - 1:
                time.sleep(timing)
        
        # Reading pause
        reading_pause = random.uniform(2.0, 3.5)
        if show_progress:
            print(f"👁️ Reading pause: {reading_pause:.1f}s")
        time.sleep(reading_pause)
    
    def mouse_scroll_up(self, amount=3, show_progress=True):
        """Mouse wheel scroll up"""
        if show_progress:
            print(f"🖱️ Mouse wheel scrolling UP x{amount}")
        
        for i in range(amount):
            pyautogui.scroll(-1)  # Scroll up
            
            # Human-like speed variation
            progress = i / (amount - 1) if amount > 1 else 0
            
            if progress < 0.3:
                timing = random.uniform(0.1, 0.3)
            elif progress < 0.7:
                timing = random.uniform(0.4, 0.8)
            else:
                timing = random.uniform(1.0, 1.8)
            
            if show_progress:
                speed_type = "Fast" if progress < 0.3 else "Medium" if progress < 0.7 else "Slow"
                print(f"🚀 {speed_type} wheel up {i+1} - {timing:.1f}s")
            
            # Apply timing (don't pause after last scroll)
            if i < amount - 1:
                time.sleep(timing)
        
        # Reading pause
        reading_pause = random.uniform(2.0, 3.5)
        if show_progress:
            print(f"👁️ Reading pause: {reading_pause:.1f}s")
        time.sleep(reading_pause)
    


# =============================================================================
# CONVENIENCE FUNCTIONS FOR EASY IMPORT
# =============================================================================

def create_scroll_controller(driver):
    """Create a ScrollController instance"""
    return ScrollController(driver)

# Keyboard convenience functions
def quick_keyboard_scroll_down(driver, amount=3):
    """Quick keyboard scroll down without progress messages"""
    controller = ScrollController(driver)
    controller.keyboard_scroll_down(amount, show_progress=False)

def quick_keyboard_scroll_up(driver, amount=3):
    """Quick keyboard scroll up without progress messages"""
    controller = ScrollController(driver)
    controller.keyboard_scroll_up(amount, show_progress=False)

def quick_keyboard_scroll_left(driver, amount=3):
    """Quick keyboard scroll left without progress messages"""
    controller = ScrollController(driver)
    controller.keyboard_scroll_left(amount, show_progress=False)

def quick_keyboard_scroll_right(driver, amount=3):
    """Quick keyboard scroll right without progress messages"""
    controller = ScrollController(driver)
    controller.keyboard_scroll_right(amount, show_progress=False)

# Mouse convenience functions
def quick_mouse_scroll_down(driver, amount=3):
    """Quick mouse scroll down without progress messages"""
    controller = ScrollController(driver)
    controller.mouse_scroll_down(amount, show_progress=False)

def quick_mouse_scroll_up(driver, amount=3):
    """Quick mouse scroll up without progress messages"""
    controller = ScrollController(driver)
    controller.mouse_scroll_up(amount, show_progress=False)



# =============================================================================
# INTERACTIVE MENU SYSTEM
# =============================================================================

def show_scroll_menu():
    """Display the interactive scroll menu"""
    print("\n" + "="*60)
    print("🖱️ INTERACTIVE SCROLL MENU")
    print("="*60)
    print("⌨️ KEYBOARD SCROLLING:")
    print("  1. Scroll Down (Arrow Down)")
    print("  2. Scroll Up (Arrow Up)")
    print("  3. Scroll Left (Arrow Left)")
    print("  4. Scroll Right (Arrow Right)")
    print("")
    print("🖱️ MOUSE WHEEL SCROLLING:")
    print("  5. Mouse Scroll Down")
    print("  6. Mouse Scroll Up")
    print("")
    print("  0. Exit")
    print("="*60)

def get_user_choice():
    """Get user's scroll choice"""
    while True:
        try:
            choice = int(input("Enter your choice (0-6): ").strip())
            if 0 <= choice <= 6:
                return choice
            else:
                print("❌ Invalid choice. Please enter a number between 0-6.")
        except ValueError:
            print("❌ Invalid input. Please enter a number.")

def get_scroll_amount():
    """Get scroll amount from user"""
    while True:
        try:
            amount = int(input("Enter scroll amount (1-50): ").strip())
            if 1 <= amount <= 50:
                return amount
            else:
                print("❌ Invalid amount. Please enter a number between 1-50.")
        except ValueError:
            print("❌ Invalid input. Please enter a number.")

def interactive_scroll_menu(scroll_controller):
    """Interactive scroll menu system"""
    while True:
        show_scroll_menu()
        choice = get_user_choice()
        
        if choice == 0:
            print("👋 Goodbye!")
            break
        
        # Get scroll amount for all scroll actions
        amount = get_scroll_amount()
        
        # Execute the chosen action
        if choice == 1:
            scroll_controller.keyboard_scroll_down(amount)
        elif choice == 2:
            scroll_controller.keyboard_scroll_up(amount)
        elif choice == 3:
            scroll_controller.keyboard_scroll_left(amount)
        elif choice == 4:
            scroll_controller.keyboard_scroll_right(amount)
        elif choice == 5:
            scroll_controller.mouse_scroll_down(amount)
        elif choice == 6:
            scroll_controller.mouse_scroll_up(amount)
        
        print("\n✅ Action completed!")
        input("Press Enter to continue...")


# =============================================================================
# TEST FUNCTIONS (for demonstration purposes)
# =============================================================================


def scroll_test_automation():
    """Comprehensive scroll testing using modular ScrollController"""
    
    # Ask user to choose scroll method
    print("🖱️ Choose Scroll Method:")
    print("1. Keyboard (Arrow keys only)")
    print("2. Mouse Wheel (pyautogui.scroll)")
    print("=" * 50)
    
    while True:
        choice = input("Enter your choice (1 or 2): ").strip()
        if choice == "1":
            scroll_method = "keyboard"
            break
        elif choice == "2":
            scroll_method = "mouse"
            break
        else:
            print("❌ Invalid choice. Please enter 1 or 2.")
    
    print(f"\n✅ Selected scroll method: {scroll_method}")
    
    # Setup Chrome driver
    options = webdriver.ChromeOptions()
    options.binary_location = "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"
    options.add_experimental_option("detach", True)
    options.add_experimental_option("excludeSwitches", ["enable-automation"])
    options.add_experimental_option('useAutomationExtension', False)
    
    driver = webdriver.Chrome(options=options)
    
    try:
        print("🚀 Starting Comprehensive Scroll Testing")
        print("=" * 50)
        
        # Create scroll controller
        scroll_controller = ScrollController(driver)
        
        # Test different websites with different scroll behaviors
        test_scenarios = [
            {
                "name": "Wikipedia Long Article",
                "url": "https://en.wikipedia.org/wiki/List_of_countries_and_dependencies_by_population",
                "description": "Testing page scroll on a long Wikipedia article"
            },
            {
                "name": "Reddit Front Page",
                "url": "https://www.reddit.com/",
                "description": "Testing infinite scroll behavior on Reddit"
            },
            {
                "name": "GitHub Trending",
                "url": "https://github.com/trending",
                "description": "Testing scroll within specific elements"
            },
            {
                "name": "News Website",
                "url": "https://www.bbc.com/news",
                "description": "Testing smooth scroll behavior"
            }
        ]
        
        for i, scenario in enumerate(test_scenarios, 1):
            print(f"\n📋 Test Scenario {i}: {scenario['name']}")
            print(f"🌐 URL: {scenario['url']}")
            print(f"📝 Description: {scenario['description']}")
            print(f"🖱️ Scroll Method: {scroll_method}")
            print("-" * 40)
            
            # Navigate to the test page
            print(f"🌐 Navigating to {scenario['url']}...")
            driver.get(scenario['url'])
            time.sleep(3)  # Wait for page to load
            
            # Perform scroll tests using modular controller
            test_scroll_patterns(scroll_controller, scroll_method)
            
            # Wait between tests
            if i < len(test_scenarios):
                print(f"\n⏳ Waiting 3 seconds before next test...")
                time.sleep(3)
        
        print("\n✅ All scroll tests completed!")
        print("🌐 Browser will remain open - you can manually close it when done")
        
    except Exception as e:
        print(f"❌ Error during scroll testing: {str(e)}")
        driver.quit()


def test_scroll_patterns(scroll_controller, scroll_method):
    """Test different scroll patterns using ScrollController"""
    
    # Test different scroll patterns
    scroll_tests = [
        {"direction": "down", "amount": 8, "name": "Fast Scroll Down"},
        {"direction": "down", "amount": 15, "name": "Medium Scroll Down"},
        {"direction": "down", "amount": 6, "name": "Slow Scroll Down"},
        {"direction": "down", "amount": 20, "name": "Very Fast Scroll Down"},
        {"direction": "up", "amount": 10, "name": "Scroll Back Up"}
    ]
    
    for i, test in enumerate(scroll_tests, 1):
        print(f"\n📜 {test['name']} Test {i}")
        print(f"🔄 Scroll: {test['direction']} x{test['amount']}")
        
        # Use modular scroll controller based on method and direction
        if scroll_method == "keyboard":
            if test['direction'] == "down":
                scroll_controller.keyboard_scroll_down(test['amount'], show_progress=True)
            elif test['direction'] == "up":
                scroll_controller.keyboard_scroll_up(test['amount'], show_progress=True)
        elif scroll_method == "mouse":
            if test['direction'] == "down":
                scroll_controller.mouse_scroll_down(test['amount'], show_progress=True)
            elif test['direction'] == "up":
                scroll_controller.mouse_scroll_up(test['amount'], show_progress=True)
        
        print(f"📍 Scroll test {i} completed")
    
    # Scroll back to top using chosen method
    print(f"\n⬆️ Scrolling back to top using {scroll_method}...")
    if scroll_method == "keyboard":
        scroll_controller.keyboard_scroll_up(20, show_progress=True)
    else:
        scroll_controller.mouse_scroll_up(10, show_progress=True)
    time.sleep(2)


def run_interactive_scroll_test():
    """Interactive scroll test using modular ScrollController with menu"""
    print("🚀 Running Interactive Scroll Test")
    print("=" * 50)
    
    # Setup Chrome driver
    options = webdriver.ChromeOptions()
    options.binary_location = "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"
    options.add_experimental_option("detach", True)
    options.add_experimental_option("excludeSwitches", ["enable-automation"])
    options.add_experimental_option('useAutomationExtension', False)
    
    driver = webdriver.Chrome(options=options)
    
    try:
        # Go to a test page
        print("🌐 Navigating to Wikipedia...")
        driver.get("https://en.wikipedia.org/wiki/List_of_countries_and_dependencies_by_population")
        time.sleep(3)
        
        # Create scroll controller
        scroll_controller = ScrollController(driver)
        
        print("✅ Scroll controller ready!")
        print("🎯 You can now use the interactive menu to test different scroll directions")
        
        # Start interactive menu
        interactive_scroll_menu(scroll_controller)
        
        print("\n✅ Interactive scroll test completed!")
        print("🌐 Browser will remain open - you can manually close it when done")
        
    except Exception as e:
        print(f"❌ Error during interactive scroll test: {str(e)}")
        driver.quit()


if __name__ == "__main__":
    print("🖱️ Scroll Testing Automation")
    print("=" * 40)
    print("🚀 Starting Interactive Scroll Testing...")
    print("📋 Available scroll functions:")
    print("   ⌨️ Keyboard: up, down, left, right (4 directions)")
    print("   🖱️ Mouse: up, down (2 directions)")
    print("=" * 40)
    
    run_interactive_scroll_test()
