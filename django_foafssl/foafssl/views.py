from django.http import HttpResponse
from django.shortcuts import render_to_response
#from foafcert import create_openssl
from  foafcert.xmpp_foaf_cert import *
#from foafssl.reg_sqlite import *
from datetime import datetime
#from pytz import timezone
from forms import *
from settings import JABBER_CACERT_PATH, JABBER_CAKEY_PATH, JABBER_DOMAIN
from django.utils.translation import ugettext_lazy as _
from jabbe_registration import JabberUtil

"""
@TODO:
 * Create form for custom name and webid
 * Include in the form  the password and change foafcert to get it from variable/file
 * Firefox should ask to import the cert instead of downloading
 * include FOAF URI in jabber vCard
"""
def xmpp_identity(request):
    """
    create jabber account if it does not exits..
    """
    if request.method == 'POST': 
        form = XmppIdentityForm(request.POST) 
        if form.is_valid(): 
            # Process the data in form.cleaned_data
#            id_xmpp = form.cleaned_data['id_xmpp']
            xmpp_password = form.cleaned_data['xmpp_password']
#            username, domain = id_xmpp.split('@')
            username = xmpp_user = form.cleaned_data['xmpp_user']
            domain = JABBER_DOMAIN
            # first create jabber account if it does not exists
            try:
                c = JabberUtil(username, domain, password)
                c.register()
            except:
                print "usuer already exists" #  (or other error)
            
            webid =  form.cleaned_data['webid']
            mkcert_casigned_from_file_save(str(id_xmpp), str(webid), JABBER_CACERT_PATH, JABBER_CAKEY_PATH)
            if 'PEM' in request.POST:
                path = pemcert()
            elif 'PKCS12' in request.POST:
                path = pkcs12cert()

            fp = open(path)
            content = fp.read()
            fp.close()
            length = os.path.getsize(path)
            r = HttpResponse(mimetype="application/x-x509-user-cert")
            r['Content-Disposition'] = 'attachment; filename=%s' % "mycert"
            r["Content-Length"] = length
            r["Accept-Ranges"] ="bytes"
            r.write(content)
#            request.user.message_set.create(message=_("You have finished creating a client certificate with webid: '%(webid)s and xmpp id: %(id_xmpp)s'") % {'webid': webid, 'id_xmpp': id_xmpp})
            return r
    else:
        form = XmppIdentityForm() # An unbound form

    return render_to_response('foafssl/xmpp_identity.html', {
        'form': form,
    })

