# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.http import Http404
from django.views.generic import TemplateView


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
