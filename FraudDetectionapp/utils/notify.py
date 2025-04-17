from twilio.rest import Client
from dotenv import load_dotenv
import os

# Load environment variables from .env file
load_dotenv()

def send_sms(message):
    # Get the Twilio SID, Auth Token, Twilio numbers, and recipient number from environment variables
    account_sid = os.getenv("TWILIO_SID")
    auth_token = os.getenv("TWILIO_AUTH")
    twilio_numbers = os.getenv("TWILIO_NUMS").split(",")  # Split the numbers into a list
    recipient_number = os.getenv("RECIPIENT_NUM")  # Get the recipient number from the environment

    # Ensure you are using a valid Twilio number to send the message
    if not twilio_numbers:
        print("No Twilio numbers found.")
        return

    twilio_number = twilio_numbers[0]  # Use the first Twilio number from your list

    client = Client(account_sid, auth_token)

    try:
        # Send SMS
        msg = client.messages.create(
            body=message,
            from_=twilio_number,
            to=recipient_number  # Send to the recipient number
        )
        print(f"SMS sent successfully: {msg.sid}")
    except Exception as e:
        print(f"Error sending SMS: {str(e)}")

# Example usage
send_sms("This is a test fraud alert!")
