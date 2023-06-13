import requests
import random
import string
import os
from datetime import datetime, timedelta

# Directory to store emails
directory = 'emails'

# Create the directory if it doesn't exist
if not os.path.exists(directory):
    os.makedirs(directory)

def generate_random_string(length):
    letters_and_digits = string.ascii_letters + string.digits
    return ''.join(random.choice(letters_and_digits) for _ in range(length))

def get_temp_email():
    response = requests.get('https://www.1secmail.com/api/v1/?action=genRandomMailbox&count=1')
    if response.status_code == 200:
        data = response.json()
        if data:
            return data[0]
    return None

def save_email_address(email_address):
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    filename = os.path.join(directory, f'{email_address}.txt')
    random_string = generate_random_string(8)
    with open(filename, 'w') as file:
        file.write(f'Email: {email_address}\n')
        file.write(f'Random String: {random_string}\n')
        file.write(f'Timestamp: {timestamp}\n')

def check_expired_emails():
    expired_emails_directory = 'expiredemails'
    if not os.path.exists(expired_emails_directory):
        os.makedirs(expired_emails_directory)

    for filename in os.listdir(directory):
        filepath = os.path.join(directory, filename)
        if os.path.isfile(filepath):
            with open(filepath, 'r') as file:
                lines = file.readlines()
                if len(lines) >= 3:
                    timestamp_str = lines[2].strip().split(': ')[1]
                    timestamp = datetime.strptime(timestamp_str, '%Y-%m-%d %H:%M:%S')
                    if datetime.now() - timestamp >= timedelta(hours=24):
                        expired_filepath = os.path.join(expired_emails_directory, filename)
                        os.rename(filepath, expired_filepath)

# Generate a random email address
temp_email = get_temp_email()
if temp_email:
    email_address = temp_email

    # Save the email address, random string, and timestamp to a file
    save_email_address(email_address)

    # Check for expired emails and move them to the "expiredemails" directory
    check_expired_emails()

    print(f'Temporary email address: {email_address}')
else:
    print('Failed to generate a temporary email address.')