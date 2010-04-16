from django.core.urlresolvers import reverse
from django.conf import settings
from django.shortcuts import render_to_response, get_object_or_404
from django.template import RequestContext
from django.http import HttpResponse, HttpResponseForbidden, HttpResponseRedirect

from django.utils.translation import ugettext_lazy as _
from django.utils.translation import ugettext

from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User

from foafidentity.models import Person
from foafidentity.forms import PersonForm
from foafidentity.foaf_conversions import person_orm_to_rdf


def person_edit(request, form_class=PersonForm, **kwargs):
    
    template_name = kwargs.get("template_name", "foafidentity/person_edit.html")
    
    if request.method == "POST":
        person_form = form_class(request.POST)
        if person_form.is_valid():
#            person = person_form.save(commit=False)
            person_orm = person_form.save(commit=False)
#            person.user = request.user
#            person.save()
#            return HttpResponseRedirect(reverse("person_detail", args=[request.user.nickname]))
#            return HttpResponseRedirect(reverse("person_rdf_detail", person)
            foaf_data = person_orm_to_rdf(person_orm)
            return HttpResponse(foaf_data, mimetype="application/xhtml+xml")
    else:
        person_form = form_class()
    
    return render_to_response(template_name, {
        "person_form": person_form,
    }, context_instance=RequestContext(request))

def person_edit_rdfa(request, form_class=PersonForm, **kwargs):
    template_name = kwargs.get("template_name", "foafidentity/person_rdfa_edit.html")
    messages = []
    if request.method == "POST":
        person_form = form_class(request.POST)
        if person_form.is_valid():
            person_orm = person_form.save()
            return HttpResponseRedirect(reverse("person_rdfa_detail", args=[person_orm.name]))
        else:
            print person_form.errors
            message = "The user with email already exits"
            messages.append(person_form.errors)
            
    else:
        person_form = form_class()
    
    return render_to_response(template_name, {
        "person_form": person_form,
        "MEDIA_URL": settings.MEDIA_URL,
        "STATIC_URL": settings.STATIC_URL,
        'messages': messages,
    }, context_instance=RequestContext(request))


def person_rdf_detail(request, nickname):
    person_orm = get_object_or_404(Person, nickname=nickname)
    foaf_data = person_orm_to_rdf(person_orm)
##    content_type = "application/xhtml+xml; charset=%s" % DEFAULT_CHARSET,
    return HttpResponse(foaf_data, mimetype="application/xhtml+xml")

def person_rdfa_detail(request, nickname, template_name="foafidentity/person_rdfa_detail.html"):
    person_orm = get_object_or_404(Person, nickname=nickname)
    print person_orm
    return render_to_response(template_name, {
        "person": person_orm,
        "MEDIA_URL": settings.MEDIA_URL,
        "STATIC_URL": settings.STATIC_URL,
    }, context_instance=RequestContext(request))
