from __future__ import unicode_literals

from django.conf.urls import patterns, url

from rblike.extension import Rblike


urlpatterns = patterns(
    'rblike.views',

    url(r'^$', 'configure'),
)