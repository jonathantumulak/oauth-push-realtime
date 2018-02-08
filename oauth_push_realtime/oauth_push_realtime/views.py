# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import json

from django.http import Http404
from django.views.generic import TemplateView
from django.http import HttpResponse


from tweepy.streaming import StreamListener
from tweepy import OAuthHandler
from tweepy import Stream

from tweet.models import Tweet

from django.http import HttpResponse
from django.views.generic import View
from django.template import loader, Context

from oauth_push_realtime.models import UserToken


class LoginRequiredMixin(object):
    """ Mixin for Resources that are only accessible for logged in users """

    def dispatch(self, method, *args, **kwargs):
        if (not hasattr(self.request, 'user') or
                not self.request.user.is_authenticated()):
            raise Http404
        return super(LoginRequiredMixin, self).dispatch(
            method, *args, **kwargs)


class HomeView(TemplateView):
    template_name = 'oauth_push_realtime/home.html'


class FeedView(LoginRequiredMixin, TemplateView):
    template_name = 'oauth_push_realtime/feed.html'

    def get_context_data(self, **kwargs):
        ctx = super(FeedView, self).get_context_data(**kwargs)
        ctx['user'] = self.request.user
        return ctx

    def post(self, request, *args, **kwargs):
        pass

class StdOutListener(StreamListener):

    def on_data(self, data):
        loaded = json.loads(data)
        # for item in loaded:
        #     print item
            # Tweet.objects.create(text=item.get('text'))
        return True

    def on_error(self, status):
        print status
        return False


def post(request):
    l = StdOutListener()
    auth = OAuthHandler('S0Mk4LKsTKEhikMHC0UStwon2', 'THCs5s2VCF6dq3nFmKgpJMXnyPULMcJknii8oYZTPT9CjOvkf7')
    auth.set_access_token('761121725283115009-ty24nOmtLgYx1cwl3TfGQ9ImoVkgARu', 'AjQPqW0Lw26m8wHMTTGCxSj9kAi9NoaZZfrSBWXXDTQBC')
    stream = Stream(auth, l)

    #This line filter Twitter Streams to capture data by the keywords: 'python', 'javascript', 'ruby'
    stream.filter(track=['python', 'javascript', 'ruby'])
    return HttpResponse(status=201)


class ServiceWorkerView(View):
    """View to serve service worker js"""

    def get(self, request, *args, **kwargs):
        javascript = loader.get_template('oauth_push_realtime/firebase-messaging-sw.js')
        response = HttpResponse(javascript.render({}))
        response['Content-Type'] = 'application/javascript'
        return response


class SaveTokenView(View):

    def post(self, request, *args, **kwargs):
        token = self.request.POST.get('token', None)
        if token:
            UserToken.objects.create(owner=self.request.user, token=token)
        return HttpResponse()
