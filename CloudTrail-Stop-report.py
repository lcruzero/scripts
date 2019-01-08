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
    accountName=["bambooprod=950880909537","corebcs=808824028248","corelogs=249475246982","coresecops=188639114030","dustdevildev=636883842329","dustdevilprod=237831351786","dustdevilstage=077594607743","elninodev=729742422785","elninoprod=574526892074","elninostage=315674266177","f5dev=913190200478","f5prod=436751343158","f5stage=368682747592","hazedev=002245141188","hazeprod=507994701454","hazestage=944107818137","infdev=552651952925","infprodvpn=643513054308","infprod=318316747731","infstage=316303769806","monsoondev=704637827957","monsoonprod=140708019862","monsoonstage=500295253484","nimbusdev=836735598406","nimbusprod=087543491196","nimbusstage=203012769823","platformsdevdistribution=790080567225","platformsdev=328926112274","platformsprod=642896844624","platformsstage=360734909313","qadev=754630846216","qaprod=533375140838","qastage=951614904934","sandboxdev=911977357153","servicesdev=421249787774","servicesprod=365852958273","servicesstage=808319953027","summerbreezedev=883042251047","summerbreezeprod=035933670544","summerbreezestage=757507578133","tsunamidev=917206393378","tsunamiprod=570740605148","tsunamistage=717244964802","master=876637047057"]

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
