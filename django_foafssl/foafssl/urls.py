from django.conf.urls.defaults import *

urlpatterns = patterns('',
    url(r'^$', 'foafssl.views.gen_cert', name='gen_cert'),
)


