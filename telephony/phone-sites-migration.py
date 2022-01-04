#!/usr/bin/env python3
# >> START phone-sites-migration
import os
import PureCloudPlatformClientV2
print("-------------------------------------------------------------")
print("- Phone Sites Migration -")
print("-------------------------------------------------------------")

# Credentials
CLIENT_ID = os.environ['GENESYS_CLOUD_CLIENT_ID']
CLIENT_SECRET = os.environ['GENESYS_CLOUD_CLIENT_SECRET']
ORG_REGION = os.environ['GENESYS_CLOUD_REGION']  # eg. us_east_1

# Set environment
region = PureCloudPlatformClientV2.PureCloudRegionHosts[ORG_REGION]
PureCloudPlatformClientV2.configuration.host = region.get_api_host()

# OAuth when using Client Credentials
api_client = PureCloudPlatformClientV2.api_client.ApiClient() \
            .get_client_credentials_token(CLIENT_ID, CLIENT_SECRET)


# Use your own IDs here
old_site_id = input("Old site id: ")
new_site_id = input("New site id: ")

"""Migrate all phones from old site to new site"""

# Genesys Cloud Objects
tpe_api = PureCloudPlatformClientV2.TelephonyProvidersEdgeApi(api_client)
# Query all Phones
phones = tpe_api.get_telephony_providers_edges_phones(expand=["lines"]).entities
print(phones)
print(f"There are {len(phones)} phones in the old site.")

if len(phones) > 0:
    print('Starting migration of phones...')
    for phone in phones:
        if phone.site.id == old_site_id:
            phone.site.id = new_site_id
            tpe_api.put_telephony_providers_edges_phone(phone.id, phone)

    print('Successfully migrated all phones.')
else:
    print('No phones to migrate.')

# >> END phone-sites-migration