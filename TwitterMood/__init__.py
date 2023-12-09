import datetime
import logging

import azure.functions as func

import os

from . import Functions

def main(mytimer: func.TimerRequest) -> None:
    utc_timestamp = datetime.datetime.utcnow().replace(tzinfo=datetime.timezone.utc).isoformat()
    logging.info('Python timer trigger function execution started: %s', utc_timestamp)

    ConnectionStringInfo = str(os.environ["string_sqldb_information"])
    
    Tweets = Functions.GetTweets(ConnectionStringInfo)

    if Tweets.shape[0] > 0:

        Tweets = Functions.MakeAnalysis(Tweets)

        Functions.WriteTweets(ConnectionStringInfo,Tweets)

    utc_timestamp = datetime.datetime.utcnow().replace(tzinfo=datetime.timezone.utc).isoformat()
    logging.info('Python timer trigger function execution concluded: %s', utc_timestamp)