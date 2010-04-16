from django.conf import settings
from django import forms

from foafidentity.models import Person

class PersonForm(forms.ModelForm):

    class Meta:
        model = Person
#        exclude = ('user',)
