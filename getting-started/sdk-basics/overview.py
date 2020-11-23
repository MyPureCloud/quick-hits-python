# >> START sdk-overview This example demonstrates authorizing using a client credentials grant and getting authorization permissions
import PureCloudPlatformClientV2

# Creates an api client
apiclient = PureCloudPlatformClientV2.api_client.ApiClient().get_client_credentials_token("a0bda580-cb41-4ff6-8f06-28ffb4227594", "e4meQ53cXGq53j6uffdULVjRl8It8M3FVsupKei0nSg")

# Create Auth API Instance
authApi = PureCloudPlatformClientV2.AuthorizationApi(apiclient)
print authApi.get_authorization_permissions()
# >> END sdk-overview
