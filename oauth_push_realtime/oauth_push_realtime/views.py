# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.http import Http404
from django.views.generic import TemplateView

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
