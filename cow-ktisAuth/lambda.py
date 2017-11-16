import json
import boto3


class Response(dict):
    def __init__(self, resp, status=200):
        super().__init__()
        self.update({
            'statusCode': status,
            'body': json.dumps(resp),
            'headers': {
                'Content-Type': 'application/json',
                'Access-Control-Allow-Origin': '*'
            },
        })


def lambda_handler(event, context):
    return Response({'debug': event})