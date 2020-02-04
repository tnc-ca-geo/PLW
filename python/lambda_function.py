import json
import rasterio


def lambda_handler(event, context):
    print(event)
    return {
        "statusCode": 200,
        "body": json.dumps(event)
    }
