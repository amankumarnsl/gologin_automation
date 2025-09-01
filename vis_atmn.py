import pyautogui
import time
import webbrowser

# --- Helper: smooth visible mouse movement ---
def smooth_move(x, y, duration=5.0, steps=150):
    """Slow visible mouse move from current pos to (x,y)."""
    start_x, start_y = pyautogui.position()
    dx = (x - start_x) / steps
    dy = (y - start_y) / steps
    delay = duration / steps
    for i in range(steps + 1):
        pyautogui.moveTo(start_x + dx * i, start_y + dy * i)
        time.sleep(delay)

# --- Step 1: Open Google in default browser ---
print("Opening Google in default browser...")
webbrowser.open("https://www.google.com")
time.sleep(6)  # wait for Google to load

# --- Step 2: Move mouse to search box & click ---
screen_width, screen_height = pyautogui.size()
search_x, search_y = screen_width // 2, screen_height // 3  # approximate position
smooth_move(search_x, search_y, duration=5.0, steps=200)
pyautogui.click()
time.sleep(1)

# --- Step 3: Type query and press Enter ---
query = "OpenAI ChatGPT visual automation demo"
pyautogui.typewrite(query, interval=0.12)
pyautogui.press("enter")
print("Searching...")
time.sleep(6)

# --- Step 4: Scroll down slowly using PageDown ---
print("Scrolling results slowly...")
for i in range(8):  # scroll 8 times
    pyautogui.press("pagedown")
    time.sleep(2.5)  # pause to simulate human reading
