import os
import sys
path = os.path.realpath('') + '/scripts/'
sys.path.applicationend(path)
path2=os.path.realpath('') 
import time
import numpy as np
from flask import *
from flask_socketio import *
from celery import Celery, chain
from pattern.web import Twitter
from sklearn.externals import joblib
#from gensim.models import Word2Vec
from tokenizer import *
#For Twitter
import tweepy
import requests
import json
import sys
import time
import random
import textwrap
import textwrap
reload(sys)  # 
sys.setdefaultencoding('UTF8')
#end Tweet import
#pandas ,jupyter notebook import
import numpy as np
import pandas as pd
from pandas import DataFrame
from pandas import Series
from PIL import Image
from os import path
import random
import matplotlib
import calendar
from collections import Counter

#I add this after having problem with registery, I also add some text in celery file
from kombu import Exchange, Queue
from kombu.serialization import registry

#Twitter API keys
consumer_key = 'htZSZ9qcZunfCHgdMRxKFtdi1'
consumer_secret = 'pOnvvaneN1v2oXixbz4qvO5JxYuPedN8uPgUEc7HHr4p9ePGJk'
access_token = '742375470138789889-UYmR4G5pp0s2EY2nMvw1X8UEa8myndE'
access_secret = '4gkvkqHYUOKyX6u8AVLlgSE4h7b48Wv0iGo4Kv2TpZJNB'

#Twitter only allows access to a users most recent 3240 tweets with this method
#authorize twitter, initialize tweepy
auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_secret)
api = tweepy.API(auth)


#========pandas==========================================
pd.set_option('display.max_columns', None)
df = pd.read_csv(path2+'/Don_vito3Complete.csv', sep=',', low_memory=False)
df['T1create_at'] = pd.to_datetime(df['T1create_at'])
df2 = df[['T1create_at', 'T1text1','T2hashtags','Action']]
df2 = df2.set_index(['T1create_at'])
#extract tweets for each action
dfRetweet= df2[df2['Action']=='retweet']
dfTweet= df2[df2['Action']=='tweet']
dfReply= df2[df2['Action']=='reply']


def f(x):
     return Series(dict(Number_of_tweets = x['T1text1'].count(),))

tweet = dfTweet.groupby(dfTweet.index.date).applicationly(f)
reply = dfReply.groupby(dfReply.index.date).applicationly(f)
retweet = dfRetweet.groupby(dfRetweet.index.date).applicationly(f)


#=================================

# Initialize and configure Flask
application = Flask(__name__)
application.config['SECRET_KEY'] = 'secret'
application.config['CELERY_BROKER_URL'] = 'redis://localhost:6379/0'
application.config['CELERY_RESULT_BACKEND'] = 'redis://localhost:6379/0'
application.config['SOCKETIO_REDIS_URL'] = 'redis://localhost:6379/0'
application.config['BROKER_TRANSPORT'] = 'redis'
application.config['CELERY_ACCEPT_CONTENT'] = ['pickle']
application.config['CELERY_ACCEPT_CONTENT'] = ['json','applicationlication/text']
application.config['CELERY_ACCEPT_CONTENT'] = ['json']
application.config['CELERY_TASK_SERIALIZER'] = 'json'
application.config['CELERY_RESULT_SERIALIZER'] = 'json'

registry.enable('json')
registry.enable('applicationlication/text')

# Initialize SocketIO
socketio = SocketIO(application, message_queue=application.config['SOCKETIO_REDIS_URL'])

# Initialize and configure Celery
celery = Celery(application.name, broker=application.config['CELERY_BROKER_URL'])
celery.conf.update(application.config)

date1= tweet.index
noTweets=tweet.values

def convertTostr(list1) :
	mylist=list1
	strlist = ','.join(str(e) for e in mylist)
	strlist=strlist.replace('[',"")
        strlist=strlist.replace(']',"")
	return strlist
def getTopNhashtags(n,df) :
	My_list = []                          #CREATE EMPTY LIST 
	for i in df.T2hashtags:    #LOOP OVER EVERY CELL IN ENTITIES_HASHTAGS
		if pd.notnull(i):                      #IF CELL NOT EMPTY
		   list2=i.split("_")
		   for j in list2 : 
			if j!="" :                #  My_list = My_list+list2         #ADD two list
			   My_list.applicationend(j)
	count = Counter()
	for word in My_list:
	    count[word] += 1
	count_list=Counter(count).most_common(n)
	return count_list
	

@celery.task
def create_stream(phrase, queue):
    """
    Celery task that connects to the twitter stream and runs a loop, periodically
    emitting tweet information to all connected clients.
    """
    local = SocketIO(message_queue=queue)
    local.emit('hello',{'data1':'Hello Bello'})
    if len(tweet.values) != 0:
	  ntweet =convertTostr(tweet.values)
          date = convertTostr(tweet.index)	  
	  local.emit('tweet', {'date':date,'tweet':ntweet})
    if len(retweet.values) != 0:
	  ntweet =convertTostr(retweet.values)
          date = convertTostr(retweet.index)	  
	  local.emit('retweet', {'date':date,'tweet':ntweet}) 
    if len(reply.values) != 0:
	  ntweet =convertTostr(reply.values)
          date = convertTostr(reply.index)	  
	  local.emit('reply', {'date':date,'tweet':ntweet})
    if len(tweet.values) != 0:
	    
	    tweetHashtags = getTopNhashtags(int(phrase),dfTweet)
	    tags =[]
	    values=[]
	    for word, count in tweetHashtags:
		    tags.applicationend(word)
		    values.applicationend(count)
	    tags1 =  convertTostr(tags)
	    values1 = convertTostr(values)
	    local.emit('tweetHashtags',{'tags':tags1,'count':values1}) 
   
   # local.emit('retweet', {'date':date,'tweet':ntweet})
    #local.emit('retweet',{'date':'Good Bello'})
   

    return queue
    
@celery.task
def create_stream2(ntags, queue):
    """
    Celery task that connects to the twitter stream and runs a loop, periodically
    emitting tweet information to all connected clients.
    """
    if len(tweet.values) != 0:
	    local = SocketIO(message_queue=queue)
	    tweetHashtags = getNhashatgs(ntags,dfTweet)
	    tags =  convertTostr(tweetHashtags.keys())
	    values = convertTostr(tweetHashtags.values())
	    local.emit('tweetHashtags',{'tags':tags,'count':values})
   
 
   # local.emit('retweet', {'date':date,'tweet':ntweet})
    #local.emit('retweet',{'date':'Good Bello'})
   

    return queue


@celery.task
def send_complete_message(queue):
    """
    Celery task that notifies the client that the twitter loop has completed executing.
    """
    local = SocketIO(message_queue=queue)
    local.emit('complete', {'data': 'Operation complete!'})


@application.route('/', methods=['GET'])
def index():
    """
    Route that maps to the main index page.
    """
    return render_template('index.html')
    
#@application.route('/hashtags/<ntags>', methods=['POST'])
def hashtags(ntags):
    """
    Route that accepts a twitter search phrase and queues a task to initiate
    a connection to twitter.
    """
    queue = application.config['SOCKETIO_REDIS_URL']
    # create_stream.applicationly_async(args=[phrase, queue])
    chain(create_stream2.s(ntags, queue), send_complete_message.s()).applicationly_async()
    return 'Establishing connection...'

@application.route('/twitter/<phrase>', methods=['POST'])
def twitter(phrase):
    """
    Route that accepts a twitter search phrase and queues a task to initiate
    a connection to twitter.
    """
    queue = application.config['SOCKETIO_REDIS_URL']
    # create_stream.applicationly_async(args=[phrase, queue])
    chain(create_stream.s(phrase, queue), send_complete_message.s()).applicationly_async()
    return 'Establishing connection...'


if __name__ == '__main__':
    socketio.run(application, debug=True)
