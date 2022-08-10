# Copyright Amazon.com, Inc. or its affiliates. All Rights Reserved.
# SPDX-License-Identifier: MIT-0
import json
import boto3
import os
from datetime import datetime, timezone
from urllib.parse import urlencode
from urllib.request import Request, urlopen, URLError, HTTPError
from botocore.exceptions import ClientError


def send_to_slack(message, webhookurl):
    slack_message = message
    req = Request(webhookurl, data=json.dumps(slack_message).encode("utf-8"),
                  headers={'content-type': 'application/json'})
    try:
        response = urlopen(req)
        response.read()
    except HTTPError as e:
        print("Request failed : ", e.code, e.reason)
    except URLError as e:
        print("Server connection failed: ", e.reason, e.reason)


def get_secrets():
    secret_slack_name = os.environ['SLACK_CHANNEL_ID']
    region_name = os.environ['AWS_REGION']
    get_secret_value_response_slack = ""

    # create a Secrets Manager client
    session = boto3.session.Session()
    client = session.client(
        service_name='secretsmanager',
        region_name=region_name
    )
   
    try:
        get_secret_value_response_slack = client.get_secret_value(
            SecretId=secret_slack_name
        )
    except ClientError as e:
        if e.response['Error']['Code'] == 'AccessDeniedException':
            print("No AWS Secret configured for Slack")
        else:    
            print("There was an error with the Slack secret: ",e.response)
            slack_channel_id = "None"
    finally:
        if 'SecretString' in get_secret_value_response_slack:
            slack_channel_id = get_secret_value_response_slack['SecretString']
        else:
            slack_channel_id = "None"

        secrets ={
            "slack" : slack_channel_id
        }

    return secrets



def convert_time(event_time):
    """
    Converts epoch to datetime
    """
    event_time = datetime.fromtimestamp(int(event_time)/1000, timezone.utc)
    return event_time.strftime("%Y-%m-%d %H:%M:%S")

def get_message_for_slack(event_details):
    message = ""
    summary = ""

    account=event_details['detail']['accountId']
    region=event_details['detail']['region']
    start_time=event_details['detail']['startTime']
    insight_type=event_details['detail']['insightType']
    severity=event_details['detail']['insightSeverity']
    description=event_details['detail']['insightDescription']
    insight_url=event_details['detail']['insightUrl']
    num_of_anomalies=len(event_details['detail']['anomalies'])
    
    summary += (
        f":alert:[NEW] Amazon DevOps Guru reported an issue in the {region.upper()} region."
    )

    message = {
        "text": summary,
        "account": account,
        "region": region,
        "startTime": convert_time(start_time),
        "insightType": insight_type,
        "severity": severity,
        "description": description,
        "insightUrl": insight_url,
        "numOfAnomalies": str(num_of_anomalies)
    }
  
    return message
    

def main(event, context):
    print("Received new event from DevOps Guru")
    slack_url = get_secrets()["slack"]

    try:
        print("Sending the alert to Slack Workflows Channel")
        message = get_message_for_slack(event)
        send_to_slack(message, slack_url)
        print("Message sent to Slack: ", message)
    except HTTPError as e:
        print("Got an error while sending message to Slack: ", e.code, e.reason)
    except URLError as e:
        print("Server connection failed: ", e.reason)
        pass