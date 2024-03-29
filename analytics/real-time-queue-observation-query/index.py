# >> START real-time-queue-observation-query
import sys
import asyncio
import time
import os
import json
import websockets
import PureCloudPlatformClientV2
from pprint import pprint
from datetime import date
from PureCloudPlatformClientV2.rest import ApiException
from PureCloudPlatformClientV2.models import response

print("-------------------------------------------------------------")
print("- Realtime Queues Member Analytics -")
print("-------------------------------------------------------------")

# >> START real-time-queue-observation-query-step-1
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
# >> END real-time-queue-observation-query-step-1

# Create an instance of the API class
api_instance = PureCloudPlatformClientV2.AnalyticsApi(api_client)
notifications_api = PureCloudPlatformClientV2.NotificationsApi(api_client)

QUEUE_ID = "QUEUE_ID"

# >> START real-time-queue-observation-query-step-2
try:
    # Create a new channel
    new_channel = notifications_api.post_notifications_channels()
    print("Created a channel")
except ApiException as e:
    print(f"Exception when calling NotificationsApi->post_notifications_channels: { e }")
    sys.exit(response.status_code)

conversations_topic_id = f"v2.routing.queues.{ QUEUE_ID }.conversations"
channel_topic = PureCloudPlatformClientV2.ChannelTopic()
channel_topic.id = conversations_topic_id

try:
    # Subscribe to conversation notifications for the queue
    notification_subscription = notifications_api.\
        put_notifications_channel_subscriptions(new_channel.id, [channel_topic])
    pprint(notification_subscription)
except ApiException as e:
    print(f"Exception when calling NotificationsApi->put_notifications_channel_subscriptions: { e }")
    sys.exit(response.status_code)

async def listen_to_Websocket():
    """ Open a new web socket using the connect Uri of the channel """
    async with websockets.connect(new_channel.connect_uri) as websocket:
        print("Listening to websocket")
        """ Message received """
        async for message in websocket:
            message = json.loads(message)
            if message['topicName'].lower() == "channel.metadata":
                print(f"Heartbeat: { date.today() }")
            elif message['topicName'].lower() != conversations_topic_id:
                print("Unexpected notification:")
                pprint(message)
            else:
                # filter each incoming interactions 
                purpose = ([x for x in message['eventBody']['participants'] if x['purpose'] == 'customer'])[0]['purpose']
                if purpose == 'customer':
                    display_queue_observation()
# >> END real-time-queue-observation-query-step-2

# >> START real-time-queue-observation-query-step-3
def display_queue_observation():
    query = PureCloudPlatformClientV2.QueueObservationQuery() # QueueObservationQuery | query
    query = {
        "filter": {
            "type": "AND",
            "clauses": [
                {
                    "type": "or",
                            "predicates":[
                                {
                                    "dimension" : "queueId",
                                    "value": QUEUE_ID
                                }
                            ]
                }
            ]
            },
        "detailMetrics": ["oInteracting"],
        "metrics":["oUserRoutingStatuses"]
        }
    try:
        # Query for queue observations
        api_response = api_instance.post_analytics_queues_observations_query(query)
        print("Display analytics observation query.")
        pprint(api_response)
    except ApiException as e:
        print ("Exception when calling AnalyticsApi->post_analytics_queues_observations_query: %s\n" % e)
# >> END real-time-queue-observation-query-step-3

grouped_async = asyncio.gather(listen_to_Websocket())
asyncio.get_event_loop().run_until_complete(grouped_async)
# >> END real-time-queue-observation-query