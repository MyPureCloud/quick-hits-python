# >> START user-lastlogin
"""
Genesys Cloud User Login Report Generator
=======================================

This script generates a CSV report of all Genesys Cloud users and their last login dates.
It uses the Genesys Cloud Platform API to fetch user data and creates a report showing:
- User ID
- Email address  
- Last login date/time
- Number of days since last login (or "Never Logged In")

Prerequisites:
-------------
1. Python 3.6+
2. PureCloudPlatformClientV2 SDK installed (pip install PureCloudPlatformClientV2)

Required Environment Variables:
----------------------------
- GENESYSCLOUD_OAUTHCLIENT_ID: Your OAuth client ID
- GENESYSCLOUD_OAUTHCLIENT_SECRET: Your OAuth client secret
- GENESYSCLOUD_API_REGION: Your Genesys Cloud region (e.g., "mypurecloud.com")

To run:
-------
1. Set up the required environment variables
2. Run: python script_name.py

Output:
-------
Creates a CSV file named 'genesys_users.csv' in the current directory
Prints summary statistics about user login status
"""

import os
import csv
from datetime import datetime, timezone
import PureCloudPlatformClientV2

# Read environment variables
CLIENT_ID = os.getenv("GENESYSCLOUD_OAUTHCLIENT_ID")
CLIENT_SECRET = os.getenv("GENESYSCLOUD_OAUTHCLIENT_SECRET")
API_REGION = os.getenv("GENESYSCLOUD_API_REGION")  # Example: "mypurecloud.com"

if not all([CLIENT_ID, CLIENT_SECRET, API_REGION]):
    raise ValueError("Missing one or more required environment variables.")

# Set up Genesys Cloud SDK
PureCloudPlatformClientV2.configuration.host = API_REGION
api_client = PureCloudPlatformClientV2.api_client.ApiClient().get_client_credentials_token(CLIENT_ID, CLIENT_SECRET)
users_api = PureCloudPlatformClientV2.UsersApi(api_client)

# Function to get all users using correct pagination
def get_all_users():
    users = []
    page_number = 1
    page_size = 100  # Max page size
    total_pages = 1  # Placeholder; will be updated dynamically

    while page_number <= total_pages:
        response = users_api.get_users(
            page_size=page_size,
            page_number=page_number,
            expand=["dateLastLogin"]  # Explicitly request dateLastLogin
        )
        users.extend(response.entities)

        total_pages = response.page_count  # Update total pages
        page_number += 1  # Move to the next page

    return users

# Retrieve users
users = get_all_users()

# Get current UTC time
current_time = datetime.now(timezone.utc)

# Process users: Extract data and calculate days since last login
never_logged_in_users = []
logged_in_users = []

for user in users:
    last_login = user.date_last_login
    
    if last_login is not None:
        # User has logged in before
        days_since_last_login = (current_time - last_login).days
        logged_in_users.append((
            user.id,
            user.email,
            last_login.isoformat(),
            days_since_last_login
        ))
    else:
        # User has never logged in
        never_logged_in_users.append((
            user.id,
            user.email,
            "",
            "Never Logged In"
        ))

# Sort logged in users by days since last login (descending)
logged_in_users.sort(key=lambda x: x[3], reverse=True)

# Combine the lists: never logged in users first, then sorted logged in users
user_data = never_logged_in_users + logged_in_users

# Write to CSV
csv_filename = "genesys_users.csv"
with open(csv_filename, mode="w", newline="") as file:
    writer = csv.writer(file)
    writer.writerow(["User ID", "Email", "Last Login", "Days Since Last Login"])
    writer.writerows(user_data)

print(f"CSV file '{csv_filename}' created successfully with {len(user_data)} users.")
print(f"Total users who have never logged in: {len(never_logged_in_users)}")
print(f"Total users who have logged in: {len(logged_in_users)}")
# >> END user-lastlogin