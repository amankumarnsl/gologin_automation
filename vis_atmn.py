import time
import random
import math
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import pyautogui

def generate_human_like_path(start_x, start_y, end_x, end_y, steps=20):
    """Generate a human-like path with dynamic zigzag and variable curves"""
    # Calculate distance and direction
    distance = math.sqrt((end_x - start_x)**2 + (end_y - start_y)**2)
    
    # Calculate the straight line direction
    direction_x = (end_x - start_x) / distance
    direction_y = (end_y - start_y) / distance
    
    # Perpendicular direction for natural curves
    perp_x = -direction_y
    perp_y = direction_x
    
    # Create control points with more dynamic variations
    control_points = []
    num_control_points = random.randint(5, 8)
    
    for i in range(num_control_points):
        progress = (i + 1) / (num_control_points + 1)
        
        # Base point along the straight line
        base_x = start_x + (end_x - start_x) * progress
        base_y = start_y + (end_y - start_y) * progress
        
        # Dynamic curve intensity - varies along the path
        if progress < 0.3:
            # Start with gentle curve
            curve_intensity = math.sin(progress * math.pi / 0.3) * random.uniform(0.1, 0.6)
        elif progress > 0.7:
            # End with gentle curve
            curve_intensity = math.sin((1 - progress) * math.pi / 0.3) * random.uniform(0.1, 0.6)
        else:
            # Middle section - dramatic curve variations (sometimes very high, sometimes very low)
            if random.random() < 0.4:  # 40% chance of very high curve
                curve_intensity = random.uniform(0.8, 1.5)
            elif random.random() < 0.3:  # 30% chance of very low curve
                curve_intensity = random.uniform(0.05, 0.3)
            else:  # 30% chance of medium curve
                curve_intensity = random.uniform(0.4, 0.8)
        
        curve_offset = distance * 0.25 * curve_intensity
        
        # Add some random variation
        random_variation = random.uniform(-0.3, 0.3)
        curve_offset += distance * 0.08 * random_variation
        
        # Calculate base curved position
        final_x = base_x + perp_x * curve_offset
        final_y = base_y + perp_y * curve_offset
        
        # Enhanced zigzag pattern - varies in intensity
        zigzag_freq = random.randint(2, 5)  # Different zigzag frequencies
        zigzag_intensity = math.sin(progress * math.pi * zigzag_freq) * distance * 0.12
        
        # Zigzag perpendicular to the main direction (more natural)
        zigzag_x = perp_x * zigzag_intensity * random.uniform(-1, 1)
        zigzag_y = perp_y * zigzag_intensity * random.uniform(-1, 1)
        
        # Add zigzag along the path direction too
        path_zigzag = math.sin(progress * math.pi * 4) * distance * 0.06
        zigzag_x += direction_x * path_zigzag * random.uniform(-1, 1)
        zigzag_y += direction_y * path_zigzag * random.uniform(-1, 1)
        
        final_x += zigzag_x
        final_y += zigzag_y
        
        control_points.append((int(final_x), int(final_y)))
    
    # Generate smooth path along the curve
    points = []
    for i in range(steps + 1):
        t = i / steps
        x, y = bezier_curve([(start_x, start_y)] + control_points + [(end_x, end_y)], t)
        points.append((int(x), int(y)))
    
    return points

def bezier_curve(control_points, t):
    """Calculate point on Bezier curve"""
    n = len(control_points) - 1
    x = y = 0
    
    for i, point in enumerate(control_points):
        coef = math.comb(n, i) * (1 - t)**(n - i) * t**i
        x += coef * point[0]
        y += coef * point[1]
    
    return x, y

def human_like_mouse_move(start_x, start_y, end_x, end_y, duration=0.5):
    """Move mouse with dynamic speed variations and natural pauses"""
    # Generate path with enhanced zigzag
    path_points = generate_human_like_path(start_x, start_y, end_x, end_y)
    
    print(f"Generated {len(path_points)} points for dynamic curved movement")
    print(f"Start: ({start_x}, {start_y}) -> End: ({end_x}, {end_y})")
    print("Watch the mouse move with varying speeds and zigzag patterns!")
    
    # Calculate dynamic timing with speed variations
    total_points = len(path_points)
    
    for i, (x, y) in enumerate(path_points):
        progress = i / (total_points - 1)
        
        # Dynamic timing based on path complexity
        if progress < 0.2:
            # Very slow, careful start
            timing_factor = 0.2 + 0.8 * (progress / 0.2) ** 1.5
        elif progress < 0.4:
            # Accelerating section
            timing_factor = 0.8 + 0.2 * ((progress - 0.2) / 0.2)
        elif progress < 0.6:
            # Fast middle section (but with variations)
            timing_factor = 1.0 + random.uniform(-0.3, 0.3)
        elif progress < 0.8:
            # Decelerating section
            timing_factor = 0.8 + 0.2 * ((0.8 - progress) / 0.2)
        else:
            # Very slow, careful end
            timing_factor = 0.2 + 0.8 * ((1 - progress) / 0.2) ** 1.5
        
        # Removed pauses for maximum speed
        # Add random human pauses at certain points
        if random.random() < 0.12:  # 12% chance of pause
            pause_time = random.uniform(0.001, 0.005)  # Much shorter pauses
            print(f"Human pause: {pause_time:.3f}s at point {i}")
            time.sleep(pause_time)
        
        # Add micro-pauses for more natural movement
        if random.random() < 0.25:  # 25% chance of micro-pause
            micro_pause = random.uniform(0.001, 0.003)  # Much shorter micro-pauses
            time.sleep(micro_pause)
        
        # Maximum speed - no delays blocking movement
        # Move to point immediately
        pyautogui.moveTo(x, y)
        
        # Print key points and show the dynamic movement
        if i % 8 == 0 or i == total_points - 1:
            print(f"Point {i}: ({x}, {y}) - Maximum speed!")
        
        # No time.sleep() - maximum speed!
    
    print("✅ Dynamic mouse movement completed!")
    print("Movement had varying speeds, zigzag patterns, and natural pauses!")

options = webdriver.ChromeOptions()
# On macOS, Chrome is usually here:
options.binary_location = "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"

# Keep browser open - don't close automatically
options.add_experimental_option("detach", True)
options.add_experimental_option("excludeSwitches", ["enable-automation"])
options.add_experimental_option('useAutomationExtension', False)

driver = webdriver.Chrome(options=options)
driver.get("https://www.google.com")

time.sleep(3)  # Wait longer for page to fully load

# ---- Step 1: Find and prepare search field ----
search = driver.find_element(By.NAME, "q")

# Clear the search field first using Selenium
search.clear()
time.sleep(0.5)

# Focus the search field using Selenium first
search.click()
time.sleep(0.5)

# Get coordinates for visual feedback
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

print(f"Moving mouse to coordinates: ({target_x}, {target_y})")

# Get current mouse position for natural movement
current_x, current_y = pyautogui.position()

# Move mouse to search field using human-like curved path
print("Moving mouse in human-like pattern...")
human_like_mouse_move(current_x, current_y, target_x, target_y, duration=2.5)
time.sleep(0.5)

# ---- Step 2: Type text using Selenium (more reliable) ----
print("Typing 'OpenAI Pricing'...")
search.send_keys("OpenAI Pricing")
time.sleep(1)

# ---- Step 3: Hit Enter using Selenium ----
print("Pressing Enter...")
search.send_keys(Keys.RETURN)

print("✅ Search executed with Enter, browser stays open")
print("Search query: OpenAI Pricing")
print("⚠️  Browser will remain open - you can manually close it when done")




