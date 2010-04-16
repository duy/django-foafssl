from django.conf.urls.defaults import *
from django.conf import settings

# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()

urlpatterns = patterns('',
    # Example:
#    (r'^django_foafssl/', include('django_foafssl.foafssl.urls')),
    (r'^$', include('foafssl.urls')),
    (r'^foaf/', include('foafidentity.urls')),
#    url(r'^$', homepage, name="home"),
#    url(r'^$', direct_to_template, {
#        "template": "homepage.html",
#    }, name="home"),
    # Uncomment the admin/doc line below and add 'django.contrib.admindocs' 
    # to INSTALLED_APPS to enable admin documentation:
    # (r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    # (r'^admin/', include(admin.site.urls)),
#    (r'^media/(?P<path>.*)$', 'django.views.static.serve', {
#        'document_root': settings.MEDIA_ROOT
#    }),
)


from django.conf import settings
if settings.SERVE_MEDIA:
    urlpatterns += patterns('',
        (r'^site_media/', include('staticfiles.urls')),
    )
    
