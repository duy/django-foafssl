from django import forms
from settings import JABBER_DOMAIN
"""
@TODO: Fix max_lenght
"""
class XmppIdentityForm(forms.Form):
#    id_xmpp = forms.CharField(max_length=255)
    xmpp_user = forms.CharField(max_length=255)
#    xmpp_domain = forms.CharField(max_length=255, default = JABBER_DOMAIN, editable=False)
    xmpp_password = forms.CharField(widget=forms.PasswordInput(render_value=False), max_length=255)
    webid = forms.URLField()

