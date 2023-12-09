import logging

import pandas as pd
import pyodbc

import re

from afinn import Afinn

def GetTweets(ConnectionString):

    Tweets = pd.DataFrame()

    SqlInput = "SELECT TOP 1000 [Tweets].[Index], [Tweets].[TweetId], [Tweets].[TweetCreatedAt], [Tweets].[Text] \
                FROM\
                (\
                SELECT 'Dax' AS [Index],[TweetId],[TweetCreatedAt],[Text]\
                FROM [Twitter].[Dax]\
                WHERE [TweetCreatedAt] >= DATEADD(month,-1,SYSUTCDATETIME())\
                UNION\
                SELECT 'Dow' AS [Index],[TweetId],[TweetCreatedAt],[Text]\
                FROM [Twitter].[Dow]\
                WHERE [TweetCreatedAt] >= DATEADD(month,-1,SYSUTCDATETIME())\
                UNION\
                SELECT 'Ftse' AS [Index],[TweetId],[TweetCreatedAt],[Text]\
                FROM [Twitter].[Ftse]\
                WHERE [TweetCreatedAt] >= DATEADD(month,-1,SYSUTCDATETIME())\
                UNION\
                SELECT 'Nasdaq' AS [Index],[TweetId],[TweetCreatedAt],[Text]\
                FROM [Twitter].[Nasdaq]\
                WHERE [TweetCreatedAt] >= DATEADD(month,-1,SYSUTCDATETIME())\
                ) AS [Tweets]\
                LEFT JOIN [Twitter].[Mood] AS [Mood] ON [Tweets].[TweetId] = [Mood].[TweetId]\
                WHERE [Mood].[TweetId] IS NULL"

    try:
        cnxn = pyodbc.connect(ConnectionString)
        Tweets = pd.read_sql(SqlInput,cnxn)
        cnxn.close()
    except Exception as e:
        logging.info(e)
        logging.info(SqlInput)

    return Tweets

def WriteTweets(ConnectionString, Tweets):

    SqlInput = "INSERT INTO [Twitter].[Mood] ([Index],[TweetId],[TweetCreatedAt],[Score]) VALUES (?,?,?,?)"

    try:
        cnxn = pyodbc.connect(ConnectionString)
        cursor = cnxn.cursor()

        for it, row in Tweets.iterrows():
            cursor.execute(SqlInput, row["Index"], row["TweetId"], row["TweetCreatedAt"], row["Score"])

        cnxn.commit()
        cursor.close()
    except Exception as e:
        logging.info(e)
        logging.info(SqlInput)

def MakeAnalysis(Tweets):

    afinn = Afinn(language = "en")

    Score = []

    for it,row in Tweets.iterrows():

        coreWords = NoUserAlpha(row["Text"])

        score = afinn.score(" ".join(coreWords))

        Score.append(score)

    Tweets["Score"] = Score

    return Tweets

def NoUserAlpha(tweet):
    tweet_list = [ele for ele in tweet.split() if ele != 'user']
    clean_tokens = [t for t in tweet_list if re.match(r'[^\W\d]*$', t)]
    return clean_tokens
