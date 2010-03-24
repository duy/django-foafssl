from django import forms

"""
@TODO: Fix max_lenght
"""
class XmppIdentityForm(forms.Form):
    id_xmpp = forms.CharField(max_length=255)
    xmpp_password = forms.CharField(widget=forms.PasswordInput(render_value=False), max_length=255)
    webid = forms.URLField()

