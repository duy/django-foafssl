from django.http import HttpResponse
from django.shortcuts import render_to_response
#from foafcert import create_openssl
from  foafcert.xmpp_foaf_cert import *
from  foafcert.foaf_cert_openssl import *
#from foafssl.reg_sqlite import *
from datetime import datetime
#from pytz import timezone
from foafssl.forms import *
from settings import JABBER_CACERT_PATH, JABBER_CAKEY_PATH, JABBER_DOMAIN
from django.utils.translation import ugettext_lazy as _
from jabberutils import JabberUtil
"""
@TODO:
 * Create form for custom name and webid
 * Include in the form  the password and change foafcert to get it from variable/file
 * Firefox should ask to import the cert instead of downloading
 * include FOAF in jabber vCard
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

def gen_cert_openssl(request):
    
    name = "henrystory"
    webid = "http://bblfish.net/people/henry/card#me"
    create_openssl(name, webid)
    generate_cert_x509(name)
    openssl_pkcs12_file_path = export_pkcs12(name)
    length = os.path.getsize(openssl_pkcs12_file_path)
#    now_utc = datetime.now(timezone('UTC'))
#    datetime_obj_utc = now_utc.astimezone(timezone('Europe/Berlin'))
#    # RFC2822 'Thu, 18 Mar 2010 17:05:57 +0100''
#    date = datetime_obj_utc.strftime("%a, %d %b %Y %H:%M:%S %z")
    print openssl_pkcs12_file_path
    fp = open(openssl_pkcs12_file_path)
    content = fp.read()
    fp.close()

#    r.headers['Content-Type'] = "application/x-x509-user-cert" 
#    r.headers['Content-Length'] =.length
#    r.headers['Last-Modified'] = date

####    r = HttpResponse(mimetype="application/x-pkcs12")
    r = HttpResponse(mimetype="application/x-x509-user-cert")
#    r['Content-Disposition'] = 'attachment; filename=%s' % openssl_pkcs12_file_path

    r['Content-Disposition'] = 'attachment; filename=%s' % "mycert.p12"
#    r['Content-Description'] = 'File Transfer'
#    r["Content-Transfer-Encoding"] = "binary"
    r["Content-Length"] = length
#    r["Pragma"] = "private"
#    r["Expires"] = "0"
#    r["Cache-Control"] = "must-revalidate, post-check=0, pre-check=0"
#    r["Cache-Control"] = "private"
    r["Accept-Ranges"] ="bytes"

    r.write(content)
    return r

