# >> START upload-prompts Guide on creating a prompt and uploading the media wav file
import base64, sys, requests, os
import PureCloudPlatformClientV2
from pprint import pprint
from PureCloudPlatformClientV2.rest import ApiException

print('-------------------------------------------------------------')
print('- Uploading Architect Prompts -')
print('-------------------------------------------------------------')

# >> START upload-prompts-step-1
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
# >> END upload-prompts-step-1

# Genesys Cloud Objects
architect_api = PureCloudPlatformClientV2.ArchitectApi(api_client)
# >> START upload-prompts-step-2
# Create new prompt
print("Creating new prompt...")
prompt_req = PureCloudPlatformClientV2.Prompt()
prompt_req.name = "uploaded_prompt"
prompt_req.description = "Prompt uploaded by upload-prompts example app"

try:
    prompt = architect_api.post_architect_prompts(prompt_req)
except ApiException as e:
    print(f"Exception when calling ArchitectApi->post_architect_prompts: {e}")
    sys.exit()
# >> END upload-prompts-step-2

# >> START upload-prompts-step-3
# Create prompt resource for english
print("Creating prompt resource...")

prompt_asset_req = PureCloudPlatformClientV2.PromptAssetCreate()
prompt_asset_req.language = "en-us"

try:
    prompt_resource = architect_api.post_architect_prompt_resources(prompt.id, prompt_asset_req)
except ApiException as e:
    print(f"Exception when calling ArchitectApi->post_architect_prompts_resources: {e}")
    sys.exit()
# >> END upload-prompts-step-3

# >> START request-presigned-url-step-4
# Request presigned URL for upload
print("Requesting presigned URL...")
try:
    presigned_url_response = architect_api.post_architect_prompt_resources_uploads(prompt_resource.promptId, prompt_resource.language)
except ApiException as e:
    print(f"Exception when calling ArchitectApi->post_architect_prompt_resources_uploads: {e}")
    sys.exit()
# >> END request-presigned-url-step-4

# >> START upload-prompts-step-5
# Upload WAV file to prompt
print("Uploading prompt...")

wav_form_data = {
    'file': ('prompt-example.wav', open('../prompt-example.wav', 'rb'))
}

upload_response = requests.post(presigned_url_response.url, files=wav_form_data,
                                headers={"Authorization": f"bearer {api_client.access_token}", **presigned_url_response.headers})

print("Upload complete. Review your prompt in architect.")
print("https://apps.mypurecloud.com/architect/#/call/userprompts")
pprint(upload_response)
# >> END upload-prompts-step-5
# >> END upload-prompts
