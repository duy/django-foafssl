from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.conf import settings

class Person(models.Model):
#    user         = models.ForeignKey(User, unique=True, verbose_name=_('user'))

#    name       = models.CharField(_('Nombre completo'),max_length=60)
    mbox         = models.EmailField(_('Mail account'),max_length=60, unique=True, help_text=_("email account"))
    mbox_sha1sum = models.CharField(_('mbox sha1sum'),max_length=40,editable=False)

#    openid       = models.URLField(_('Openid account'),max_length=60,verify_exists=False,blank=True,null=True)
#    weblog       = models.ForeignKey(Weblog, verbose_name=_('weblog'),blank=True,null=True))

#    weblog       = models.URLField(_('Weblog'),max_length=60,verify_exists=False,blank=True,null=True)
    seeAlso      = models.URLField(_('FOAF URI'),max_length=60,verify_exists=False,blank=True,null=True)

#    firstName  = models.CharField(_('Nombre'),max_length=60,blank=True,null=True)
#    family_name= models.CharField(_('Apellidos'),max_length=60,blank=True,null=True)

    nickname     = models.CharField(_('Nickname'),max_length=60, unique=True)
#    surname    = models.CharField(_('Apellido'),max_length=60,blank=True,null=True)
#    given_name = models.CharField(_('Alias'),max_length=60,blank=True,null=True)
#    gender       = models.CharField(_('gender'),max_length=60,choices=GENDER_CHOICES,blank=True,null=True)
#    birthday  = models.CharField(_('Fecha de Nacimiento'),max_length=60,blank=True,null=True)

#    homepage     = models.URLField(_('Homepage'),verify_exists=False,blank=True,null=True)
#    icqChatID    = models.CharField(_('Cuenta ICQ'),max_length=20,blank=True,null=True)
#    aimChatID    = models.CharField(_('Cuenta AIM'),max_length=16,blank=True,null=True)

#    jabberID     = models.EmailField(_('Jabber account'),max_length=60,blank=True,null=True)
#    depiction  = models.ManyToManyField(Depiction, null=True, blank=True)
#    workplaceHomepage= models.URLField(_('Homepage trabajo (url)'),blank=True,null=True)
#    workInfoHomepage = models.URLField(_('Informacion pagina trabajo (url)'),blank=True,null=True)
#    schoolHomepage   = models.URLField(_('Homepage escuela (url)'),blank=True,null=True)

#    currentProject     = models.ManyToManyField(Project, null=True, blank=True, verbose_name=_("Proyectos"), related_name="person_project")
#    interests          = models.ManyToManyField(Knowledge, null=True, blank=True, verbose_name=_("Intereses"), related_name="person_interest")
#    knowledge          = models.ManyToManyField(Knowledge, null=True, blank=True, verbose_name=_("Conocimientos"), related_name="person_knowledge")

    public_exponent = models.IntegerField(editable=False,blank=True,null=True)
    modulus     = models.TextField(unique=True,editable=False,blank=True,null=True)

    def __unicode__(self):
        return self.nickname
    
    def get_absolute_url(self):
        return ('person_rdfa_detail', None, {'nickname': self.nickname})
    get_absolute_url = models.permalink(get_absolute_url)
    
    def get_webid(self):
        return('person_rdf_detail', None, {'nickname': self.nickname})
    get_webid = models.permalink(get_webid)

    class Meta:
        verbose_name = _('person foaf')
        verbose_name_plural = _('persons')
