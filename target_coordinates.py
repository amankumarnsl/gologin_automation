from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import random


def get_random_coordinates_within_element(coordinates):
    """
    Get random coordinates within an element (not centered)
    
    Args:
        coordinates: dict with x, y, width, height
    
    Returns:
        tuple: (random_x, random_y) within the element bounds
    """
    # Get random position within the element bounds
    random_x = coordinates['x'] + random.randint(5, coordinates['width'] - 5)
    random_y = coordinates['y'] + random.randint(5, coordinates['height'] - 5)
    
    print(f"Random coordinates within element: ({random_x}, {random_y})")
    return random_x, random_y


def get_element_coordinates(driver, element_selector, selector_type="css"):
    """
    Get the real coordinates of any element in the browser
    
    Args:
        driver: Selenium WebDriver instance
        element_selector: The selector to find the element (CSS selector, XPath, ID, etc.)
        selector_type: Type of selector ("css", "xpath", "id", "name", "class_name", "tag_name")
    
    Returns:
        dict: Contains 'x', 'y', 'width', 'height', 'center_x', 'center_y'
    """
    try:
        # Wait for element to be present
        wait = WebDriverWait(driver, 10)
        
        # Find element based on selector type
        if selector_type == "css":
            element = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, element_selector)))
        elif selector_type == "xpath":
            element = wait.until(EC.presence_of_element_located((By.XPATH, element_selector)))
        elif selector_type == "id":
            element = wait.until(EC.presence_of_element_located((By.ID, element_selector)))
        elif selector_type == "name":
            element = wait.until(EC.presence_of_element_located((By.NAME, element_selector)))
        elif selector_type == "class_name":
            element = wait.until(EC.presence_of_element_located((By.CLASS_NAME, element_selector)))
        elif selector_type == "tag_name":
            element = wait.until(EC.presence_of_element_located((By.TAG_NAME, element_selector)))
        else:
            raise ValueError(f"Invalid selector_type: {selector_type}")
        
        # Get element coordinates and dimensions
        rect = driver.execute_script("""
            let el = arguments[0];
            let r = el.getBoundingClientRect();
            return {
                abs_x: r.left + window.screenX + (window.outerWidth - window.innerWidth),
                abs_y: r.top + window.screenY + (window.outerHeight - window.innerHeight),
                width: r.width,
                height: r.height
            };
        """, element)
        
        # Calculate center coordinates
        center_x = int(rect["abs_x"] + rect["width"] / 2)
        center_y = int(rect["abs_y"] + rect["height"] / 2)
        
        coordinates = {
            'x': int(rect["abs_x"]),
            'y': int(rect["abs_y"]),
            'width': int(rect["width"]),
            'height': int(rect["height"]),
            'center_x': center_x,
            'center_y': center_y
        }
        
        print(f"✅ Element found: {element_selector}")
        print(f"Coordinates: ({coordinates['x']}, {coordinates['y']})")
        print(f"Size: {coordinates['width']} x {coordinates['height']}")
        print(f"Center: ({coordinates['center_x']}, {coordinates['center_y']})")
        
        return coordinates
        
    except Exception as e:
        print(f"❌ Error getting coordinates for {element_selector}: {str(e)}")
        return None

def get_element_by_text(driver, text, tag_name="*"):
    """
    Get coordinates of element containing specific text
    
    Args:
        driver: Selenium WebDriver instance
        text: Text to search for
        tag_name: HTML tag name (default: any tag)
    
    Returns:
        dict: Element coordinates or None if not found
    """
    try:
        # XPath to find element containing text
        xpath = f"//{tag_name}[contains(text(), '{text}')]"
        return get_element_coordinates(driver, xpath, "xpath")
    except Exception as e:
        print(f"❌ Error finding element with text '{text}': {str(e)}")
        return None

def get_button_coordinates(driver, button_text=None, button_id=None, button_class=None):
    """
    Get coordinates of a button element
    
    Args:
        driver: Selenium WebDriver instance
        button_text: Button text content
        button_id: Button ID attribute
        button_class: Button class attribute
    
    Returns:
        dict: Button coordinates or None if not found
    """
    try:
        if button_id:
            return get_element_coordinates(driver, button_id, "id")
        elif button_class:
            return get_element_coordinates(driver, button_class, "class_name")
        elif button_text:
            return get_element_by_text(driver, button_text, "button")
        else:
            print("❌ Please provide button_text, button_id, or button_class")
            return None
    except Exception as e:
        print(f"❌ Error finding button: {str(e)}")
        return None

def get_form_field_coordinates(driver, field_name=None, field_id=None, field_placeholder=None):
    """
    Get coordinates of a form field element
    
    Args:
        driver: Selenium WebDriver instance
        field_name: Field name attribute
        field_id: Field ID attribute
        field_placeholder: Field placeholder text
    
    Returns:
        dict: Form field coordinates or None if not found
    """
    try:
        if field_id:
            return get_element_coordinates(driver, field_id, "id")
        elif field_name:
            return get_element_coordinates(driver, field_name, "name")
        elif field_placeholder:
            xpath = f"//input[@placeholder='{field_placeholder}']"
            return get_element_coordinates(driver, xpath, "xpath")
        else:
            print("❌ Please provide field_name, field_id, or field_placeholder")
            return None
    except Exception as e:
        print(f"❌ Error finding form field: {str(e)}")
        return None

# Example usage functions
def get_google_search_coordinates(driver):
    """Get Google search box coordinates"""
    return get_element_coordinates(driver, "input[name='q']", "css")

def get_google_search_button_coordinates(driver):
    """Get Google search button coordinates"""
    return get_element_coordinates(driver, "input[name='btnK']", "css")

# Test function
if __name__ == "__main__":
    # Example usage
    print("This module provides functions to get element coordinates.")
    print("Import and use these functions in your automation scripts:")
    print("- get_element_coordinates()")
    print("- get_element_by_text()")
    print("- get_button_coordinates()")
    print("- get_form_field_coordinates()")
    print("- get_google_search_coordinates()")
    print("- get_google_search_button_coordinates()")
