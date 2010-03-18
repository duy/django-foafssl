from django.http import HttpResponse 
#from foafcert import create_openssl
from  foafcert.foafcert import *
from datetime import datetime
#from pytz import timezone

#def gen_cert(request,
#    template_name="foafssl/gen_cert.html"):
def gen_cert(request):
    
    name = "henrystory"
    webid = "http://bblfish.net/people/henry/card#me"
#    openssl_file_path = "data/openssl-foaf.cnf"
#    openssl_custom_file_path = "/tmp/%s_openssl-foaf.cnf" % (name)
#    openssl_cert_file_path = "/tmp/%s_cert.pem" % name
#    openssl_private_key_file_path = "/tmp/%s_privatekey.pem" % name
#    openssl_pkcs12_file_path = "/tmp/%s_cert.p12" % name
#    create_openssl(name, webid, openssl_custom_file_path)
    create_openssl(name, webid)
#    generate_cert_x509(openssl_custom_file_path, openssl_cert_file_path)
    generate_cert_x509(name)
#    export_pkcs12(openssl_cert_file_path, openssl_private_key_file_path, openssl_pkcs12_file_path)
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
#    t = Template(response.content)
#    response.content = t.render(RequestContext(request))

#    r = render_to_response(template_name, {
#        "join_request_form": join_request_form,
#        "invites_received": invites_received,
#        "invites_sent": invites_sent,
#        "joins_sent": joins_sent,
#    }, context_instance=RequestContext(request))

#    r = HttpResponse(content,mimetype="application/x-x509-user-cert")
#    r = HttpResponse(mimetype="application/x-x509-user-cert")
#    r.headers['Content-Type'] = "application/x-x509-user-cert" 
#    r.headers['Content-Length'] =.length
#    r.headers['Last-Modified'] = date
#    r.headers['Accept-Ranges'] = 'bytes'

    r = HttpResponse(mimetype="application/x-pkcs12")
    r['Content-Disposition'] = 'attachment; filename=%s' % openssl_pkcs12_file_path
    r['Content-Description'] = 'File Transfer'
    r["Content-Transfer-Encoding"] = "binary"
    r["Content-Length"] = length
    r["Pragma"] = "private"
    r["Expires"] = "0"
    r["Cache-Control"] = "must-revalidate, post-check=0, pre-check=0"
    r["Cache-Control"] = "private"

    r.write(content)
    return r

