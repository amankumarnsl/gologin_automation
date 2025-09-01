import requests
import json
import time


class DaisySMSClient:
    """DaisySMS API client for handling SMS operations"""
    
    def __init__(self, api_token=None):
        self.base_url = "https://api.d7networks.com/messages/v1"
        self.api_token = api_token or "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJhdWQiOiJhdXRoLWJhY2tlbmQ6YXBwIiwic3ViIjoiNzgxMmZkNmYtOGRmZi00ZTljLWFjYjItYmZkZjdmMjVhZGNhIn0.mecDUyeV1wP4dVJlNfgIHg1qI26nmvswAefU7uXwzWc"
        self.headers = {
            'Content-Type': 'application/json',
            'Accept': 'application/json',
            'Authorization': f'Bearer {self.api_token}'
        }
    
    def send_sms(self, mobile_number, message, originator="SignOTP"):
        """
        Send SMS using D7 API
        
        Args:
            mobile_number (str): Mobile number (with or without +)
            message (str): SMS message content
            originator (str): SMS originator/sender ID
            
        Returns:
            dict: API response data
        """
        try:
            # Clean mobile number (remove + if present)
            clean_mobile = mobile_number.replace("+", "") if mobile_number.startswith("+") else mobile_number
            
            payload = {
                "messages": [
                    {
                        "channel": "sms",
                        "recipients": [clean_mobile],
                        "content": message,
                        "msg_type": "text",
                        "data_coding": "text"
                    }
                ],
                "message_globals": {
                    "originator": originator,
                    "report_url": "https://example.com/delivery_report"
                }
            }
            
            print(f"📤 Sending SMS to {mobile_number}...")
            print(f"📱 Clean number: {clean_mobile}")
            print(f"💬 Message: {message}")
            
            response = requests.post(
                f"{self.base_url}/send",
                headers=self.headers,
                data=json.dumps(payload)
            )
            
            print(f"📡 API Response Status: {response.status_code}")
            print(f"📄 API Response: {response.text}")
            
            if response.status_code == 200:
                print("✅ SMS sent successfully!")
                return {
                    "success": True,
                    "data": response.json(),
                    "status_code": response.status_code
                }
            else:
                print(f"❌ SMS sending failed with status: {response.status_code}")
                return {
                    "success": False,
                    "error": response.text,
                    "status_code": response.status_code
                }
                
        except Exception as e:
            print(f"❌ SMS sending error: {e}")
            return {
                "success": False,
                "error": str(e),
                "status_code": None
            }
    
    def get_delivery_status(self, message_id):
        """
        Get delivery status of sent SMS
        
        Args:
            message_id (str): Message ID from send_sms response
            
        Returns:
            dict: Delivery status data
        """
        try:
            response = requests.get(
                f"{self.base_url}/reports/{message_id}",
                headers=self.headers
            )
            
            if response.status_code == 200:
                return {
                    "success": True,
                    "data": response.json()
                }
            else:
                return {
                    "success": False,
                    "error": response.text,
                    "status_code": response.status_code
                }
                
        except Exception as e:
            return {
                "success": False,
                "error": str(e)
            }
    
    def validate_mobile_number(self, mobile_number):
        """
        Validate mobile number format
        
        Args:
            mobile_number (str): Mobile number to validate
            
        Returns:
            bool: True if valid, False otherwise
        """
        import re
        
        # Remove spaces and special characters
        clean_number = re.sub(r'[^\d+]', '', mobile_number)
        
        # Check for valid international format
        patterns = [
            r'^\+\d{10,15}$',  # +country_code + number
            r'^\d{10,15}$'     # just number
        ]
        
        for pattern in patterns:
            if re.match(pattern, clean_number):
                return True
        
        return False
    
    def format_mobile_number(self, mobile_number, country_code="+91"):
        """
        Format mobile number to standard international format
        
        Args:
            mobile_number (str): Raw mobile number
            country_code (str): Default country code if not present
            
        Returns:
            str: Formatted mobile number
        """
        import re
        
        # Remove all non-digit characters except +
        clean_number = re.sub(r'[^\d+]', '', mobile_number)
        
        # If number doesn't start with +, add country code
        if not clean_number.startswith('+'):
            # Remove leading zeros
            clean_number = clean_number.lstrip('0')
            clean_number = f"{country_code}{clean_number}"
        
        return clean_number
    
    def bulk_send_sms(self, recipients, message, originator="SignOTP"):
        """
        Send SMS to multiple recipients
        
        Args:
            recipients (list): List of mobile numbers
            message (str): SMS message content
            originator (str): SMS originator/sender ID
            
        Returns:
            dict: Bulk send results
        """
        results = []
        
        for mobile in recipients:
            result = self.send_sms(mobile, message, originator)
            results.append({
                "mobile": mobile,
                "result": result
            })
            # Small delay between requests
            time.sleep(1)
        
        success_count = sum(1 for r in results if r["result"]["success"])
        
        print(f"📊 Bulk SMS Results: {success_count}/{len(recipients)} successful")
        
        return {
            "total": len(recipients),
            "successful": success_count,
            "failed": len(recipients) - success_count,
            "details": results
        }
