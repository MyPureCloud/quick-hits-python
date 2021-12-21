# >> START analytics-conversation-aggregate-query
import base64, sys, requests, os
from datetime import datetime, timedelta
import PureCloudPlatformClientV2
from pprint import pprint
from PureCloudPlatformClientV2.rest import ApiException

# >> START analytics-conversation-aggregate-query-step-2
def get_interval_string():
    """ Gets an ISO-8601 interval from now for the last 7 days """
    now = datetime.now().replace(microsecond=0)
    week_ago = (now - timedelta(days=7)).replace(microsecond=0)
    return f"{ week_ago.isoformat() }/{ now.isoformat() }"
# >> END analytics-conversation-aggregate-query-step-2

print("-------------------------------------------------------------")
print("- Querying Queue Historical Statistics -")
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

# Genesys Cloud Objects
routing_api = PureCloudPlatformClientV2.RoutingApi(api_client)
analytics_api = PureCloudPlatformClientV2.AnalyticsApi(api_client)

# Get "Support" queue by name
try:
    queue_data = routing_api.get_routing_queues(name='Support')
except ApiException as e:
    print("Exception when calling RoutingApi->get_routing_queues: {e}")
    sys.exit()

print(f"queueData: {queue_data}")

# Store queue ID
queue_id = queue_data.entities[0].id

# >> START analytics-conversation-aggregate-query-step-1
# Build analytics query
query = PureCloudPlatformClientV2.ConversationAggregationQuery()
query.interval = get_interval_string()
# >> START analytics-conversation-aggregate-query-step-3
query.group_by = ['queueId']
# >> END analytics-conversation-aggregate-query-step-3
# >> START analytics-conversation-aggregate-query-step-4
query.metrics = ['nOffered', 'tAnswered', 'tTalk']
# >> END analytics-conversation-aggregate-query-step-4
# >> START analytics-conversation-aggregate-query-step-5
query.filter = PureCloudPlatformClientV2.ConversationAggregateQueryFilter()
query.filter.type = 'and'
query.filter.clauses = [PureCloudPlatformClientV2.ConversationAggregateQueryClause()]
query.filter.clauses[0].type = 'or'
query.filter.clauses[0].predicates = [PureCloudPlatformClientV2.ConversationAggregateQueryPredicate()]
query.filter.clauses[0].predicates[0].dimension = 'queueId'
query.filter.clauses[0].predicates[0].value = queue_id
# >> END analytics-conversation-aggregate-query-step-5
# >> END analytics-conversation-aggregate-query-step-1

print(f"query: {query}")

# >> START analytics-conversation-aggregate-query-step-6
# Execute analytics query
query_result = analytics_api.post_analytics_conversations_aggregates_query(query)

pprint(f"queryResult: {query_result}")
# >> END analytics-conversation-aggregate-query-step-6
# >> END analytics-conversation-aggregate-query
