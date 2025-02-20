# >> START find_onqueue_agents_by_skill.py
"""
This script queries the Genesys Cloud API to find agents who meet the following criteria:
- Are currently on-queue (available to take interactions)
- Have a specific skill assigned to them
- Are members of any queue in the organization

The script will:
1. Connect to Genesys Cloud using OAuth credentials
2. Look up the ID of the specified skill
3. Iterate through all queues in the organization
4. For each queue, check all queue members
5. Filter for members who are on-queue and have the specified skill
6. Display results in a table showing:
   - Queue ID and name
   - Skill ID and name  
   - User ID and name

Installation:
1. Install required dependencies:
   pip install PureCloudPlatformClientV2 prettytable

2. Set up environment variables:
   GENESYSCLOUD_OAUTHCLIENT_ID - Your Genesys Cloud OAuth client ID
   GENESYSCLOUD_OAUTHCLIENT_SECRET - Your Genesys Cloud OAuth client secret  
   GENESYSCLOUD_API_REGION - Your Genesys Cloud API region URL (e.g. https://api.mypurecloud.com)

Usage:
   python script.py <skill_name>

   Example: python script.py "Customer Service"
"""

import os
import argparse
import PureCloudPlatformClientV2
from PureCloudPlatformClientV2.rest import ApiException
from prettytable import PrettyTable


def main():
    # Set up command-line argument parsing
    parser = argparse.ArgumentParser(description="Find agents on-queue with a specific skill across all queues.")
    parser.add_argument('skill_name', type=str, help='The name of the skill to search for.')
    args = parser.parse_args()

    # Retrieve environment variables
    client_id = os.getenv('GENESYSCLOUD_OAUTHCLIENT_ID')
    client_secret = os.getenv('GENESYSCLOUD_OAUTHCLIENT_SECRET')
    environment = os.getenv('GENESYSCLOUD_API_REGION')

    # Validate environment variables
    if not all([client_id, client_secret, environment]):
        print("Error: Missing one or more environment variables: "
              "GENESYSCLOUD_OAUTHCLIENT_ID, GENESYSCLOUD_OAUTHCLIENT_SECRET, GENESYSCLOUD_API_REGION")
        return

    # Configure the SDK
    PureCloudPlatformClientV2.configuration.host = environment
    api_client = PureCloudPlatformClientV2.api_client.ApiClient().get_client_credentials_token(client_id, client_secret) 

    # Create instances of the necessary APIs
    routing_api = PureCloudPlatformClientV2.RoutingApi(api_client)
    users_api = PureCloudPlatformClientV2.UsersApi(api_client)

    try:
        # Retrieve all routing skills to map skill names to IDs
        skills = routing_api.get_routing_skills()
        skill_map = {skill.name: skill.id for skill in skills.entities}

        # Check if the specified skill exists
        if args.skill_name not in skill_map:
            print(f"Skill '{args.skill_name}' not found.")
            return

        required_skill_id = skill_map[args.skill_name]

        # Initialize the table
        table = PrettyTable()
        table.field_names = ["Queue ID", "Queue Name", "Skill ID", "Skill Name", "User ID", "User Name"]

        # Initialize pagination variables for queues
        page_number = 1
        page_size = 100  # Maximum page size
        more_pages = True

        while more_pages:
            # Fetch a page of queues
            queues = routing_api.get_routing_queues(page_size=page_size, page_number=page_number)
            queue_list = queues.entities

            # Iterate through each queue
            for queue in queue_list:
                queue_id = queue.id
                queue_name = queue.name

                # Initialize pagination variables for queue members
                member_page_number = 1
                more_member_pages = True

                while more_member_pages:
                    # Fetch a page of queue members with expanded skills and presence information
                    members = routing_api.get_routing_queue_members(
                        queue_id=queue_id,
                        page_size=page_size,
                        page_number=member_page_number,
                        expand=['skills', 'routingStatus','presence'],
                        joined=True
                    )

                    # Filter members who are on-queue and have the exact required skill
                    for member in members.entities:
                        if any(skill.id == required_skill_id for skill in member.user.skills) and member.user.presence.presence_definition.system_presence=="On Queue":
                            # Fetch user details
                            user = users_api.get_user(member.id)
                            # Add row to the table
                            table.add_row([queue_id, queue_name, required_skill_id, args.skill_name, user.id, user.name])

                    # Check if there are more pages of members
                    member_page_number += 1
                    more_member_pages = (members.next_uri!=None)

            # Check if there are more pages of queues
        
            page_number += 1
            more_pages = page_number <= queues.page_count

        # Print the table
        print(table)

    except ApiException as e:
        print(f"Exception when calling API: {e}")

if __name__ == '__main__':
    main()
# >> END find_onqueue_agents_by_skill.py  
