import requests
import time
from datetime import datetime

# IPRoyal credentials
USERNAME = "os4C1BLBSyyABmpd"
PASSWORD = "bTRxKrFpB0YSKUkW"
HOST = "geo.iproyal.com:12321"

def get_ip(session_id: str, city: str = "jaipur", ttl_hours: int = 48, country: str = "in"):
    """
    Returns the IP address assigned for a given session_id.
    Same session_id → same IP, Different session_id → different IP.
    """
    proxy_pass = f"{PASSWORD}_country-{country}_city-{city}_session-{session_id}_lifetime-{ttl_hours}h"

    proxies = {
        "http": f"http://{USERNAME}:{proxy_pass}@{HOST}",
        "https": f"http://{USERNAME}:{proxy_pass}@{HOST}",
    }

    try:
        r = requests.get("https://api.ipify.org?format=json", proxies=proxies, timeout=20)
        return r.json()["ip"]
    except Exception as e:
        return f"Error: {str(e)}"

# --- Check same session ID every 2 minutes for 20 minutes ---
session_id = "stickyW"
total_duration = 20 * 60  # 20 minutes in seconds
check_interval = 2 * 60   # 2 minutes in seconds

print(f"Checking session '{session_id}' every 2 minutes for 20 minutes...")
print("-" * 50)

start_time = time.time()
check_count = 0
max_checks = total_duration // check_interval

while time.time() - start_time < total_duration:
    check_count += 1
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    ip_address = get_ip(session_id)
    
    print(f"Check #{check_count} at {current_time}: {ip_address}")
    
    # Sleep for 2 minutes, but adjust to ensure total duration doesn't exceed 20 minutes
    remaining_time = total_duration - (time.time() - start_time)
    sleep_time = min(check_interval, remaining_time)
    
    if sleep_time > 0:
        time.sleep(sleep_time)

print("-" * 50)
print(f"Completed {check_count} checks over 20 minutes")