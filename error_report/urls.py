from django.conf.urls import patterns, include, url
from error_report.views import *

urlpatterns = patterns('error_report.views',
	url(r'^$', 'index'),
	url(r'^login/$', 'login'),

	url(r'^app/(?P<app_id>[^/]+)/',include(patterns('',
		url(r'^$',app),
	))),
	url(r'^reports/(?P<report>[^/]+)/',include(patterns('',
		url(r'^messages/add/$',add_message),
		url(r'^messages/$',get_messages),
		url(r'^details/$',report_page),
		url(r'^get/$',get_report),
	))),

	url(r'^(?P<app>[^/]+)/$', 'report'),
)
