from __future__ import absolute_import

import os
import json

from celery import Celery
from celery.task import periodic_task

from django.utils.timezone import timedelta
from tweepy.streaming import StreamListener
from tweepy import OAuthHandler
from tweepy import Stream

# from tweet.models import Tweet

# set the default Django settings module for the 'celery' program.
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'oauth_push_realtime.settings')

from django.conf import settings

app = Celery('oauth_push_realtime')

# Using a string here means the worker will not have to
# pickle the object when using Windows.
app.config_from_object('django.conf:settings')

app.autodiscover_tasks(lambda: settings.INSTALLED_APPS)


class StdOutListener(StreamListener):

    def on_data(self, data):
        loaded = json.loads(data.text)
        # for item in loaded:
            # Tweet.objects.create(text=item.get('text'))
        return True

    def on_error(self, status):
        print status
        return False


@app.task(bind=True)
def debug_task(self):
    print('Request: {0!r}'.format(self.request))


@periodic_task(run_every=timedelta(seconds=60 * 3))
def debug_tasker():
    # api = twitter.Api(consumer_key='S0Mk4LKsTKEhikMHC0UStwon2',
    #                   consumer_secret='THCs5s2VCF6dq3nFmKgpJMXnyPULMcJknii8oYZTPT9CjOvkf7',
    #                   access_token_key='761121725283115009-ty24nOmtLgYx1cwl3TfGQ9ImoVkgARu',
    #                   access_token_secret='AjQPqW0Lw26m8wHMTTGCxSj9kAi9NoaZZfrSBWXXDTQBC')
    # print(api.GetUserStream)

    l = StdOutListener()
    auth = OAuthHandler('S0Mk4LKsTKEhikMHC0UStwon2', 'THCs5s2VCF6dq3nFmKgpJMXnyPULMcJknii8oYZTPT9CjOvkf7')
    auth.set_access_token('761121725283115009-ty24nOmtLgYx1cwl3TfGQ9ImoVkgARu', 'AjQPqW0Lw26m8wHMTTGCxSj9kAi9NoaZZfrSBWXXDTQBC')
    stream = Stream(auth, l)

    #This line filter Twitter Streams to capture data by the keywords: 'python', 'javascript', 'ruby'
    stream.filter(track=['python', 'javascript', 'ruby'])
