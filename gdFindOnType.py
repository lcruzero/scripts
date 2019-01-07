import json
import boto3
import ast
import re

def lambda_handler(event, context):
    t=str(event)
    json_data = ast.literal_eval(t)
    json_stdout = (json.dumps(json_data))
    json_stdout=json.loads(json_stdout)

    accountName=["accountName1=000000000000","accountName2=000000000000"]


    accountJson=json_stdout['detail']['accountId']
    account="notFound"
    for i in accountName:
        if accountJson in i:
            temp=i.split("=")
            account=temp[0].replace("dev","-dev")
            account=account.replace("stage","-stage")
            account=account.replace("prod","-prod")

    if account == "notFound":
        account=accountJson

#    account = 'adi-aws-core-secops'

    temp=json_stdout['detail']['service']['eventFirstSeen'].split("T")
    date=temp[0]
    time=temp[1]


    detail_type=json_stdout['detail']['type']
    Description=json_stdout['detail']['description']
    eventSource=json_stdout['source']
    account=json_stdout['detail']['accountId']
    userName=json_stdout['detail']['resource']['accessKeyDetails']['userName']
    region=json_stdout['detail']['region']


    msg="date:\t\t\t\t      " + date
    msg=msg + "\ntime:\t\t\t\t      " + time.replace("Z"," UTC")
    msg=msg + "\ndetail_type:\t\t\t " + detail_type
    msg=msg + "\neventSource:\t\t\t" + eventSource
    msg=msg + "\naccount:\t\t\t   "+ account
    msg=msg + "\nDescription:\t\t\t" + Description
    msg=msg + "\nuserName:\t\t\t   "+ userName
    msg=msg + "\nregion:\t\t\t\t     "+ region

   # header = json_stdout['detail']['description']

    threshold = 4
    severity = json_stdout['detail']['severity']

    if severity > threshold:
        msg=msg + "\n\n\nPayLoad:\n" + json.dumps(event)
        client = boto3.client('sns')
        response = client.publish(
            TopicArn= 'arn:aws:sns:us-east-1:xxxxxxxxxxx:secops-gd',
            Message=msg,
            #Subject= "test" + Description
            Subject= "GuardDuty event finding Severity > 4 " + account
)
