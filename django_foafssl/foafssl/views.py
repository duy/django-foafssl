from django.http import HttpResponse 
#from foafcert import create_openssl
from  foafcert.foafcert import *
from datetime import datetime
#from pytz import timezone


"""
@TODO:
 * Create form for custom name and webid
 * Include in the form  the password and change foafcert to get it from variable/file
 * Firefox should ask to import the cert instead of downloading
"""
def gen_cert(request):
    
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

