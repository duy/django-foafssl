from django.conf.urls.defaults import *

urlpatterns = patterns('',
#    url(r'^$', 'foafssl.views.gen_cert', name='gen_cert'),
    url(r'^$', 'foafssl.views.xmpp_identity', name='xmpp_identity'),
)


