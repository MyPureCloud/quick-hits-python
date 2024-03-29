# >> START real-time-queue-observation-query-step-4
{
    "results": [
    {
        "group": {
            "queueId": "1d1af111-b11c-11f1-b111-1cf1c11111fc"
        },
        "data": [
        {
            "metric": "oUserRoutingStatuses",
            "qualifier": "INTERACTING",
            "stats": {
                "count": 2
            }
        },
        {
            "metric": "oUserRoutingStatuses",
            "qualifier": "IDLE",
            "stats": {
                "count": 1
            }
        },
        {
            "metric": "oUserRoutingStatuses",
            "qualifier": "OFF_QUEUE",
            "stats": {
                "count": 3
            }
        }
        ]
    },
    {
        "group": {
            "queueId": "1d1af111-b11c-11f1-b111-1cf1c11111fc",
            "mediaType": "voice"
        },
        "data": [
        {
            "metric": "oInteracting",
            "stats": {
                "count": 1
            },
            "truncated": false,
            "observations": [
            {
                "observationDate": "2020-08-03T04:28:15.134Z",
                "conversationId": "111eb1ec-c111-11d1-bbb1-1f1b1c111da1",
                "sessionId": "1df11a1d-1d1c-110e-bd11-1caf1fb111fb",
                "routingPriority": 0,
                "participantName": "Makati, Philippines",
                "userId": "be11a111-1ff1-1a11-111f-11cb1a11da1e",
                "direction": "inbound",
                "ani": "tel:+63299999000",
                "dnis": "tel:+16149999000"
            }
            ]
        }
        ]
    },
    {
        "group": {
            "queueId": "1d1af111-b11c-11f1-b111-1cf1c11111fc",
            "mediaType": "chat"
        },
        "data": [
        {
            "metric": "oInteracting",
            "stats": {
                "count": 1
            },
            "truncated": false,
            "observations": [
            {
                "observationDate": "2020-08-03T04:27:36.780Z",
                "conversationId": "cb111111-1111-11cb-b11c-1f11111b1c1e",
                "sessionId": "1fb111d1-111c-1da1-aa1e-fe1111e11d1e",
                "routingPriority": 2,
                "participantName": "Juan Dela Cruz",
                "userId": "da11acf1-0110-11d1-1111-ddf111111a11",
                "direction": "inbound"
            }
            ]
        }
        ]
    },
    {
        "group": {
            "queueId": "1d1af111-b11c-11f1-b111-1cf1c11111fc",
            "mediaType": "message"
        },
        "data": [
        {
            "metric": "oInteracting",
            "stats": {
                "count": 0
            }
        }
        ]
    },
    {
        "group": {
            "queueId": "1d1af111-b11c-11f1-b111-1cf1c11111fc",
            "mediaType": "email"
        },
        "data": [
        {
            "metric": "oInteracting",
            "stats": {
                "count": 0
            }
        }
        ]
    },
    {
        "group": {
            "queueId": "1d1af111-b11c-11f1-b111-1cf1c11111fc",
            "mediaType": "callback"
        },
        "data": [
        {
            "metric": "oInteracting",
            "stats": {
                "count": 0
            }
        }
        ]
    }
    ]
}
# >> END real-time-queue-observation-query-step-4
