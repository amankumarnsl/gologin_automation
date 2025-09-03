import time
import random
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from target_coordinates import get_element_coordinates, get_random_coordinates_within_element
from vis_atmn import human_like_mouse_move
import pyautogui


def wikipedia_search_automation():
    """Automate Wikipedia search with human-like mouse movement"""
    
    # Setup Chrome driver
    options = webdriver.ChromeOptions()
    options.binary_location = "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"
    options.add_experimental_option("detach", True)
    options.add_experimental_option("excludeSwitches", ["enable-automation"])
    options.add_experimental_option('useAutomationExtension', False)
    
    driver = webdriver.Chrome(options=options)
    
    try:
        # Visit Wikipedia
        print("🌐 Visiting Wikipedia...")
        driver.get("https://www.wikipedia.org/")
        time.sleep(3)  # Wait for page to load
        
        # ---- Step 1: Find search input element and get random coordinates ----
        print("\n🔍 Finding search input element...")
        search_input_coords = get_element_coordinates(driver, "input#searchInput", "css")
        
        if not search_input_coords:
            print("❌ Could not find search input element")
            return
        
        # Get random coordinates within the search input (not centered)
        search_x, search_y = get_random_coordinates_within_element(search_input_coords)
        
        # ---- Step 2: Move mouse to search input with human-like movement ----
        print(f"\n🖱️ Moving mouse to search input at ({search_x}, {search_y})...")
        current_x, current_y = pyautogui.position()
        
        # Use vis_atmn.py for human-like movement
        human_like_mouse_move(current_x, current_y, search_x, search_y, duration=1.5)
        
        # Click on the search input
        print("👆 Clicking on search input...")
        pyautogui.click()
        time.sleep(0.5)
        
        # ---- Step 3: Type "albert einstein" ----
        print("⌨️ Typing 'albert einstein'...")
        pyautogui.typewrite("albert einstein", interval=0.1)
        time.sleep(1)
        
        # ---- Step 4: Find search button and get random coordinates ----
        print("\n🔍 Finding search button...")
        search_button_coords = get_element_coordinates(driver, "button.pure-button.pure-button-primary-progressive", "css")
        
        if not search_button_coords:
            print("❌ Could not find search button")
            return
        
        # Get random coordinates within the search button (not centered)
        button_x, button_y = get_random_coordinates_within_element(search_button_coords)
        
        # ---- Step 5: Move mouse to search button with human-like movement ----
        print(f"\n🖱️ Moving mouse to search button at ({button_x}, {button_y})...")
        
        # Use vis_atmn.py for human-like movement
        human_like_mouse_move(search_x, search_y, button_x, button_y, duration=1.5)
        
        # Click on the search button
        print("👆 Clicking search button...")
        pyautogui.click()
        
        print("\n✅ Search completed! Wikipedia should now show results for 'Albert Einstein'")
        print("🌐 Browser will remain open - you can manually close it when done")
        
    except Exception as e:
        print(f"❌ Error during automation: {str(e)}")
        driver.quit()

if __name__ == "__main__":
    print("🚀 Starting Wikipedia Search Automation")
    print("This script will:")
    print("1. Visit Wikipedia")
    print("2. Find search input and move mouse there (human-like)")
    print("3. Type 'albert einstein'")
    print("4. Find search button and move mouse there (human-like)")
    print("5. Click to search\n")
    
    wikipedia_search_automation()
