from __future__ import print_function
import json
import boto3
import ast

def lambda_handler(event, context):

    t=str(event)
    json_data = ast.literal_eval(t)
    testz= (json.dumps(json_data))
    testz=json.loads(testz)



    #translate acct no# to friendly name
    accountName=["accountName1=xxxxxxxxxxxxxxx", "accountName2=xxxxxxxxxxxxxx"]

    accountJson=testz['detail']['userIdentity']['accountId']
    account="notFound"
    for i in accountName:
        if accountJson in i:
            temp=i.split("=")
            account=temp[0].replace("dev","-dev")
            account=account.replace("stage","-stage")
            account=account.replace("prod","-prod")

    if account == "notFound":
        account=accountJson


    temp=testz['detail']['eventTime'].split("T")
    date=temp[0]
    time=temp[1]

    region=testz['detail']['awsRegion']
    eventName=testz['detail']['eventName']
    eventSource=testz['source']
    ip=testz['detail']['sourceIPAddress']
    arn=testz['detail']['userIdentity']['arn']


    msg="date:\t\t\t      " + date
    msg=msg + "\ntime:\t\t\t      " + time.replace("Z"," UTC")
    msg=msg + "\nregion:\t\t\t     " + region
    msg=msg + "\naccount:\t\t    " + account
    msg=msg + "\neventSource:\t\t " + eventSource
    msg=msg + "\neventName:\t\t" + eventName
    msg=msg + "\nuser:\t\t\t       " + arn
    msg=msg + "\nip:\t\t\t         " + ip

    msg=msg + "\n\n\nPayLoad:\n" + json.dumps(event)
    client = boto3.client('sns')
    response = client.publish(
        TopicArn= 'arn:aws:sns:us-east-1:xxxxxxxxxxxxxx:OpenVPN_Alarms_Dev',
        Message=msg,
        Subject="CloudTrail Logging Disabled for Acct: " + account

    )
