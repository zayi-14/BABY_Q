# utils.py
from twilio.rest import Client

def send_otp_via_twilio(phone):
    # Your Twilio credentials
    account_sid = 'your_account_sid'
    auth_token = 'your_auth_token'
    from_number = 'your_twilio_number'

    # Generate a random OTP (you can use a more sophisticated method)
    otp = '123456'  # Replace with actual OTP generation logic

    client = Client(account_sid, auth_token)
    message = client.messages.create(
        body=f'Your OTP is {otp}',
        from_=from_number,
        to=phone
    )
    return otp
