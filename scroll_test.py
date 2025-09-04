import time
import random
import math
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from target_coordinates import get_element_coordinates, get_random_coordinates_within_element
from vis_atmn import human_like_mouse_move
import pyautogui


def smooth_human_scroll(driver, total_amount, steps=10):
    """
    Perform smooth human-like scrolling with natural acceleration/deceleration
    """
    print(f"🔄 Smooth scrolling {total_amount}px in {steps} steps...")
    
    # Create a natural scroll curve (slow start, fast middle, slow end)
    scroll_steps = []
    for i in range(steps):
        progress = i / (steps - 1)
        
        # Natural scroll curve: ease-in-out with some randomness
        if progress < 0.3:
            # Slow start
            curve_factor = 0.3 + 0.7 * (progress / 0.3) ** 2
        elif progress > 0.7:
            # Slow end
            curve_factor = 0.3 + 0.7 * ((1 - progress) / 0.3) ** 2
        else:
            # Fast middle with some variation
            curve_factor = 1.0 + random.uniform(-0.2, 0.2)
        
        # Calculate step amount with natural variation
        base_step = total_amount / steps
        step_amount = base_step * curve_factor * random.uniform(0.8, 1.2)
        
        scroll_steps.append(int(step_amount))
    
    # Execute smooth scrolling
    for i, step_amount in enumerate(scroll_steps):
        # Add natural timing variation
        if i == 0:
            # First step - slightly longer pause
            time.sleep(random.uniform(0.1, 0.2))
        elif i == len(scroll_steps) - 1:
            # Last step - longer pause
            time.sleep(random.uniform(0.15, 0.25))
        else:
            # Middle steps - variable timing
            time.sleep(random.uniform(0.05, 0.15))
        
        # Perform the scroll step
        driver.execute_script(f"window.scrollBy(0, {step_amount});")
        
        # Add micro-pauses for natural reading behavior
        if random.random() < 0.3:  # 30% chance of micro-pause
            micro_pause = random.uniform(0.1, 0.3)
            time.sleep(micro_pause)


def smooth_human_scroll_to_top(driver):
    """Smooth scroll back to top with human-like behavior"""
    current_scroll = driver.execute_script("return window.pageYOffset")
    if current_scroll > 0:
        print(f"🔄 Smooth scrolling back to top from {current_scroll}px...")
        smooth_human_scroll(driver, -current_scroll, steps=12)
    else:
        print("📍 Already at top of page")


def smooth_mouse_wheel_scroll(driver, scroll_clicks, direction="down"):
    """
    Perform smooth mouse wheel scrolling with human-like timing
    """
    print(f"🖱️ Smooth mouse wheel scrolling {scroll_clicks} clicks {direction}...")
    
    # Move mouse to a natural position first
    current_x, current_y = pyautogui.position()
    target_x = random.randint(600, 1000)
    target_y = random.randint(400, 600)
    
    # Human-like mouse movement
    human_like_mouse_move(current_x, current_y, target_x, target_y, duration=0.8)
    
    # Perform smooth wheel scrolling
    for i in range(scroll_clicks):
        # Natural timing between wheel clicks
        if i == 0:
            time.sleep(random.uniform(0.2, 0.4))
        else:
            time.sleep(random.uniform(0.1, 0.3))
        
        # Perform wheel scroll
        if direction == "down":
            pyautogui.scroll(1)
        else:
            pyautogui.scroll(-1)
        
        # Add occasional longer pauses (like reading)
        if random.random() < 0.2:  # 20% chance
            reading_pause = random.uniform(0.5, 1.2)
            time.sleep(reading_pause)


def natural_reading_behavior(driver, duration=2.0):
    """
    Simulate natural reading behavior with micro-movements
    """
    print(f"👁️ Simulating reading behavior for {duration:.1f}s...")
    
    start_time = time.time()
    while time.time() - start_time < duration:
        # Occasional small mouse movements (like following text)
        if random.random() < 0.3:  # 30% chance
            current_x, current_y = pyautogui.position()
            # Small random movement
            new_x = current_x + random.randint(-20, 20)
            new_y = current_y + random.randint(-10, 10)
            
            # Ensure we stay within reasonable bounds
            new_x = max(100, min(1800, new_x))
            new_y = max(100, min(1000, new_y))
            
            pyautogui.moveTo(new_x, new_y, duration=random.uniform(0.3, 0.8))
        
        # Random pause
        time.sleep(random.uniform(0.2, 0.6))


def scroll_test_automation():
    """Comprehensive scroll testing automation with human-like mouse movement"""
    
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
        
        # Test different websites with different scroll behaviors
        test_scenarios = [
            {
                "name": "Wikipedia Long Article",
                "url": "https://en.wikipedia.org/wiki/List_of_countries_and_dependencies_by_population",
                "scroll_type": "page_scroll",
                "description": "Testing page scroll on a long Wikipedia article"
            },
            {
                "name": "Reddit Front Page",
                "url": "https://www.reddit.com/",
                "scroll_type": "infinite_scroll",
                "description": "Testing infinite scroll behavior on Reddit"
            },
            {
                "name": "GitHub Trending",
                "url": "https://github.com/trending",
                "scroll_type": "element_scroll",
                "description": "Testing scroll within specific elements"
            },
            {
                "name": "News Website",
                "url": "https://www.bbc.com/news",
                "scroll_type": "smooth_scroll",
                "description": "Testing smooth scroll behavior"
            }
        ]
        
        for i, scenario in enumerate(test_scenarios, 1):
            print(f"\n📋 Test Scenario {i}: {scenario['name']}")
            print(f"🌐 URL: {scenario['url']}")
            print(f"📝 Description: {scenario['description']}")
            print(f"🔄 Scroll Type: {scenario['scroll_type']}")
            print("-" * 40)
            
            # Navigate to the test page
            print(f"🌐 Navigating to {scenario['url']}...")
            driver.get(scenario['url'])
            time.sleep(3)  # Wait for page to load
            
            # Perform scroll test based on type
            if scenario['scroll_type'] == "page_scroll":
                test_page_scroll(driver, scenario['name'])
            elif scenario['scroll_type'] == "infinite_scroll":
                test_infinite_scroll(driver, scenario['name'])
            elif scenario['scroll_type'] == "element_scroll":
                test_element_scroll(driver, scenario['name'])
            elif scenario['scroll_type'] == "smooth_scroll":
                test_smooth_scroll(driver, scenario['name'])
            
            # Wait between tests
            if i < len(test_scenarios):
                print(f"\n⏳ Waiting 3 seconds before next test...")
                time.sleep(3)
        
        print("\n✅ All scroll tests completed!")
        print("🌐 Browser will remain open - you can manually close it when done")
        
    except Exception as e:
        print(f"❌ Error during scroll testing: {str(e)}")
        driver.quit()


def test_page_scroll(driver, test_name):
    """Test basic page scrolling with human-like smooth movement"""
    print(f"\n🔄 Testing Human-like Smooth Page Scroll for {test_name}")
    
    # Get initial page height
    initial_height = driver.execute_script("return document.body.scrollHeight")
    print(f"📏 Initial page height: {initial_height}px")
    
    # Test different scroll amounts with human-like behavior
    scroll_amounts = [200, 400, 600, 800, 1000]
    
    for i, amount in enumerate(scroll_amounts, 1):
        print(f"\n📜 Smooth Scroll Test {i}: Scrolling down {amount}px")
        
        # Move mouse to a random position on screen for natural behavior
        current_x, current_y = pyautogui.position()
        target_x = random.randint(400, 1200)
        target_y = random.randint(300, 700)
        
        # Human-like mouse movement
        human_like_mouse_move(current_x, current_y, target_x, target_y, duration=1.0)
        
        # Perform smooth human-like scroll with gradual steps
        smooth_human_scroll(driver, amount, steps=8)
        
        # Human-like pause to "read" content
        reading_pause = random.uniform(1.5, 3.0)
        print(f"👁️ Reading pause: {reading_pause:.1f}s")
        time.sleep(reading_pause)
        
        # Get current scroll position
        current_scroll = driver.execute_script("return window.pageYOffset")
        print(f"📍 Current scroll position: {current_scroll}px")
    
    # Smooth scroll back to top
    print(f"\n⬆️ Smooth scrolling back to top...")
    smooth_human_scroll_to_top(driver)
    time.sleep(2)


def test_infinite_scroll(driver, test_name):
    """Test infinite scroll behavior (like Reddit, Twitter) with smooth scrolling"""
    print(f"\n🔄 Testing Smooth Infinite Scroll for {test_name}")
    
    # Get initial number of elements
    initial_elements = len(driver.find_elements(By.TAG_NAME, "article"))
    print(f"📊 Initial articles/posts: {initial_elements}")
    
    # Perform multiple smooth scrolls to trigger infinite loading
    for i in range(5):
        print(f"\n📜 Smooth Infinite Scroll Test {i + 1}")
        
        # Move mouse to center of screen
        current_x, current_y = pyautogui.position()
        target_x = random.randint(600, 1000)
        target_y = random.randint(400, 600)
        
        # Human-like mouse movement
        human_like_mouse_move(current_x, current_y, target_x, target_y, duration=1.0)
        
        # Get current scroll position
        current_scroll = driver.execute_script("return window.pageYOffset")
        page_height = driver.execute_script("return document.body.scrollHeight")
        
        # Calculate smooth scroll amount (scroll towards bottom but not all the way)
        scroll_amount = min(800, (page_height - current_scroll) // 2)
        
        # Perform smooth scroll
        smooth_human_scroll(driver, scroll_amount, steps=6)
        
        # Natural reading behavior
        natural_reading_behavior(driver, duration=random.uniform(1.5, 2.5))
        
        # Check if new elements were loaded
        new_elements = len(driver.find_elements(By.TAG_NAME, "article"))
        print(f"📊 Articles/posts after scroll: {new_elements}")
        
        if new_elements > initial_elements:
            print(f"✅ New content loaded! (+{new_elements - initial_elements} items)")
            initial_elements = new_elements
        else:
            print("ℹ️ No new content loaded yet")


def test_element_scroll(driver, test_name):
    """Test scrolling within specific elements"""
    print(f"\n🔄 Testing Element Scroll for {test_name}")
    
    # Try to find scrollable elements
    scrollable_selectors = [
        "div[style*='overflow']",
        ".scrollable",
        "[data-testid*='scroll']",
        "div[class*='scroll']",
        "section[class*='list']"
    ]
    
    scrollable_element = None
    for selector in scrollable_selectors:
        try:
            elements = driver.find_elements(By.CSS_SELECTOR, selector)
            if elements:
                scrollable_element = elements[0]
                print(f"✅ Found scrollable element: {selector}")
                break
        except:
            continue
    
    if scrollable_element:
        # Get element coordinates
        element_coords = get_element_coordinates(driver, scrollable_element)
        if element_coords:
            # Move mouse to the scrollable element
            current_x, current_y = pyautogui.position()
            target_x, target_y = get_random_coordinates_within_element(element_coords)
            
            # Human-like mouse movement to element
            human_like_mouse_move(current_x, current_y, target_x, target_y, duration=1.5)
            
            # Perform scroll within the element
            print("🖱️ Scrolling within the element...")
            for i in range(3):
                # Use ActionChains to scroll within the element
                actions = ActionChains(driver)
                actions.move_to_element(scrollable_element)
                actions.scroll_by_amount(0, 200)
                actions.perform()
                time.sleep(1)
    else:
        print("ℹ️ No specific scrollable elements found, testing general page scroll")
        test_page_scroll(driver, test_name)


def test_smooth_scroll(driver, test_name):
    """Test ultra-smooth scrolling behavior with human-like patterns"""
    print(f"\n🔄 Testing Ultra-Smooth Human-like Scroll for {test_name}")
    
    # Test different smooth scrolling patterns
    scroll_patterns = [
        {"amount": 400, "steps": 12, "name": "Gentle Smooth Scroll"},
        {"amount": 600, "steps": 15, "name": "Medium Smooth Scroll"},
        {"amount": 800, "steps": 20, "name": "Slow Smooth Scroll"},
        {"amount": 1000, "steps": 25, "name": "Ultra-Smooth Scroll"}
    ]
    
    for i, pattern in enumerate(scroll_patterns, 1):
        print(f"\n📜 {pattern['name']} Test {i}")
        
        # Move mouse to a natural position
        current_x, current_y = pyautogui.position()
        target_x = random.randint(500, 1100)
        target_y = random.randint(350, 650)
        
        # Human-like mouse movement
        human_like_mouse_move(current_x, current_y, target_x, target_y, duration=1.0)
        
        # Perform ultra-smooth scroll with more steps
        smooth_human_scroll(driver, pattern['amount'], steps=pattern['steps'])
        
        # Natural reading behavior after scroll
        natural_reading_behavior(driver, duration=random.uniform(2.0, 3.5))
        
        # Get current scroll position
        current_scroll = driver.execute_script("return window.pageYOffset")
        print(f"📍 Current scroll position: {current_scroll}px")
    
    # Ultra-smooth scroll back to top
    print(f"\n⬆️ Ultra-smooth scrolling back to top...")
    smooth_human_scroll_to_top(driver)
    time.sleep(2)


def test_mouse_wheel_scroll(driver, test_name):
    """Test smooth mouse wheel scrolling with human-like behavior"""
    print(f"\n🔄 Testing Smooth Mouse Wheel Scroll for {test_name}")
    
    # Test different smooth wheel scroll patterns
    wheel_patterns = [
        {"clicks": 3, "direction": "down", "name": "Gentle Wheel Scroll"},
        {"clicks": 5, "direction": "down", "name": "Medium Wheel Scroll"},
        {"clicks": 8, "direction": "down", "name": "Fast Wheel Scroll"},
        {"clicks": 4, "direction": "up", "name": "Scroll Back Up"}
    ]
    
    for i, pattern in enumerate(wheel_patterns, 1):
        print(f"\n🖱️ {pattern['name']} Test {i}")
        
        # Perform smooth mouse wheel scroll
        smooth_mouse_wheel_scroll(driver, pattern['clicks'], pattern['direction'])
        
        # Natural reading behavior after wheel scroll
        natural_reading_behavior(driver, duration=random.uniform(1.0, 2.0))
        
        # Get current scroll position
        current_scroll = driver.execute_script("return window.pageYOffset")
        print(f"📍 Current scroll position: {current_scroll}px")


def test_keyboard_scroll(driver, test_name):
    """Test keyboard-based scrolling with human-like timing"""
    print(f"\n🔄 Testing Human-like Keyboard Scroll for {test_name}")
    
    # Focus on the page body
    body = driver.find_element(By.TAG_NAME, "body")
    body.click()
    
    # Test different keyboard scroll methods with natural timing
    keyboard_tests = [
        {"key": Keys.PAGE_DOWN, "name": "Page Down", "pause": 2.5},
        {"key": Keys.PAGE_DOWN, "name": "Page Down Again", "pause": 2.0},
        {"key": Keys.PAGE_UP, "name": "Page Up", "pause": 2.0},
        {"key": Keys.END, "name": "End Key", "pause": 3.0},
        {"key": Keys.HOME, "name": "Home Key", "pause": 2.5}
    ]
    
    for i, test in enumerate(keyboard_tests, 1):
        print(f"\n⌨️ Keyboard Test {i}: {test['name']}")
        
        # Move mouse to a natural position before keyboard action
        current_x, current_y = pyautogui.position()
        target_x = random.randint(500, 1100)
        target_y = random.randint(400, 600)
        
        # Human-like mouse movement
        human_like_mouse_move(current_x, current_y, target_x, target_y, duration=0.8)
        
        # Send the key
        body.send_keys(test['key'])
        
        # Natural reading behavior after keyboard scroll
        natural_reading_behavior(driver, duration=test['pause'])
        
        # Get current scroll position
        current_scroll = driver.execute_script("return window.pageYOffset")
        print(f"📍 Current scroll position: {current_scroll}px")


def run_quick_scroll_test():
    """Quick scroll test on a single page"""
    print("🚀 Running Quick Scroll Test")
    print("=" * 30)
    
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
        
        # Run all smooth scroll tests on this page
        test_page_scroll(driver, "Wikipedia Quick Test")
        test_mouse_wheel_scroll(driver, "Wikipedia Quick Test")
        test_keyboard_scroll(driver, "Wikipedia Quick Test")
        
        # Add a final smooth scroll demonstration
        print(f"\n🎯 Final Smooth Scroll Demonstration")
        smooth_human_scroll(driver, 1000, steps=30)
        natural_reading_behavior(driver, duration=3.0)
        smooth_human_scroll_to_top(driver)
        
        print("\n✅ Quick scroll test completed!")
        print("🌐 Browser will remain open - you can manually close it when done")
        
    except Exception as e:
        print(f"❌ Error during quick scroll test: {str(e)}")
        driver.quit()


if __name__ == "__main__":
    print("🖱️ Scroll Testing Automation")
    print("=" * 40)
    print("Choose test mode:")
    print("1. Comprehensive Test (multiple websites)")
    print("2. Quick Test (single page)")
    print("=" * 40)
    
    choice = input("Enter your choice (1 or 2): ").strip()
    
    if choice == "1":
        print("\n🚀 Starting Comprehensive Scroll Testing...")
        scroll_test_automation()
    elif choice == "2":
        print("\n🚀 Starting Quick Scroll Testing...")
        run_quick_scroll_test()
    else:
        print("❌ Invalid choice. Running quick test by default...")
        run_quick_scroll_test()
