from django.conf.urls.defaults import *

#def show_foaf(nickname):
#    if :
#        ('^rdf/(?P<nickname>[\w\._-]+)/$', direct_to_template, {
#        'template': 'about.html'
#        })
#    else:
#        url(r'^rdf/(?P<nickname>[\w\._-]+)/$', 'foafidentity.views.person_rdf_detail', name="person_rdf_detail")


urlpatterns = patterns('',
    url(r'^edit/$', 'foafidentity.views.person_edit', name='person_edit'),
    url(r'^$', 'foafidentity.views.person_edit_rdfa', name='person_edit_rdfa'),
    url(r'^rdf/(?P<nickname>[\w\._-]+)/$', 'foafidentity.views.person_rdf_detail', name="person_rdf_detail"),
    url(r'^rdfa/(?P<nickname>[\w\._-]+)/$', 'foafidentity.views.person_rdfa_detail', name="person_rdfa_detail"),
)

