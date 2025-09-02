import time
from selenium import webdriver
from selenium.webdriver.common.by import By
import pyautogui

options = webdriver.ChromeOptions()
# On macOS, Chrome is usually here:
options.binary_location = "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"

driver = webdriver.Chrome(options=options)
driver.get("https://www.google.com")

time.sleep(2)

# ---- Step 1: Move to Search Bar ----
search = driver.find_element(By.NAME, "q")
rect = driver.execute_script("""
    let el = arguments[0];
    let r = el.getBoundingClientRect();
    return {
        abs_x: r.left + window.screenX + (window.outerWidth - window.innerWidth),
        abs_y: r.top + window.screenY + (window.outerHeight - window.innerHeight),
        width: r.width,
        height: r.height
    };
""", search)

target_x = int(rect["abs_x"] + rect["width"] / 2)
target_y = int(rect["abs_y"] + rect["height"] / 2)
pyautogui.moveTo(target_x, target_y, duration=2.5)
pyautogui.click()
time.sleep(1)

# ---- Step 2: Type text ----
pyautogui.typewrite("Selenium tutorial", interval=0.1)
time.sleep(2)

# ---- Step 3: Find the *visible* search button ----
btns = driver.find_elements(By.NAME, "btnK")
btn = None
for b in btns:
    if b.is_displayed():
        btn = b
        break

if btn:
    rect_btn = driver.execute_script("""
        let el = arguments[0];
        let r = el.getBoundingClientRect();
        return {
            abs_x: r.left + window.screenX + (window.outerWidth - window.innerHeight),
            abs_y: r.top + window.screenY + (window.outerHeight - window.innerHeight),
            width: r.width,
            height: r.height
        };
    """, btn)

    target_x_btn = int(rect_btn["abs_x"] + rect_btn["width"] / 2)
    target_y_btn = int(rect_btn["abs_y"] + rect_btn["height"] / 2)
    pyautogui.moveTo(target_x_btn, target_y_btn, duration=2.5)
    pyautogui.click()
    print("✅ Search executed, browser stays open")
else:
    print("⚠️ Could not find visible search button")
