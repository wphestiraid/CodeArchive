from django.conf.urls import url
from . import views

urlpatterns = [
	url(r'^$', views.post_list, name='post_list'),
	url(r'^post/(?P<pk>[0-9]+)/$', views.post_detail, name='post_detail'),
	url(r'^post/new/$', views.post_new, name='post_new'),
	url(r'^post/(?P<pk>[0-9]+)/edit/$', views.post_edit, name='post_edit'),
	url(r'^drafts/$', views.post_draft_list, name='post_draft_list'),
	url(r'^post/(?P<pk>\d+)/publish/$', views.post_publish, name='post_publish'),
	url(r'^post/(?P<pk>\d+)/remove/$', views.post_remove, name='post_remove'),
	url(r'^category/(?P<ct>[a-zA-Z0-9\u3131-\u3163\uac00-\ud7a3]+)/$', views.post_category, name="post_category"),
	url(r'^(?P<year>[0-9]{4})/(?P<month>[0-9]+)/$', views.month_view),
	url(r'^search/$', views.search_post, name='search_post'),
]