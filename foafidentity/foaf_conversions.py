from foafidentity.models_rdf import Person as PersonRDF
from django.conf import settings

from rdflib import URIRef, Literal, BNode, Namespace, ConjunctiveGraph, RDF
from rdflib import Namespace

FOAF=Namespace("http://xmlns.com/foaf/0.1/" )
RDFS=Namespace("http://www.w3.org/2000/01/rdf-schema#")
REL=Namespace("http://purl.org/vocab/relationship/")
CERT=Namespace("http://www.w3.org/ns/auth/cert#")
RSA=Namespace("http://www.w3.org/ns/auth/rsa#")

def person_orm_to_rdfalchemy(person_orm):
#    person_rdf = PersonRDF()
    person_rdf = PersonRDF(resUri='<http://localhost:8000/rdf'+person_orm.nickname+'#me>')
    for key in person_orm.__dict__.keys():
        if person_orm.__dict__[key] and not key.endswith('id') :
            #value = str(person_rdf.__dict__[key])
            value = getattr(person_orm, key)
            setattr(person_rdf, key, value)
#    rdf = person_rdf.db.serialize(format='rdf', encoding='utf-8')
#    return rdf
    return person_rdf

def complete_person_orm_to_rdfalchemy(person_orm):
    person_rdf =  person_orm_to_rdfalchemy(person_orm)
#    for friend in person_orm.person_from_set.all():
#        friend_rdf =  =  person_orm_to_rdfalchemy(friend.person_to)
#        person_rdf.knows.append(friend_rdf)

def person_orm_to_rdf(person_orm):
    #rdf graph
    store = ConjunctiveGraph()
    
    #namespaces
#        store.bind('sioc', SIOC)
    store.bind('foaf', FOAF)
#        store.bind('dc', DC)
    store.bind('rel', REL)
#        store.bind('doap', DOAP)
#        store.bind('air', AIR)
#        store.bind('contact', CONTACT)
#        store.bind('rss', RSS)
    store.bind('rdfs', RDFS)
    store.bind('rsa', RSA)
    store.bind('cert', CERT)


    # person graph
    person_uri = URIRef('http://localhost:8000/rdf'+person_orm.nickname+'#me')
    person = URIRef('http://localhost:8000/rdf'+person_orm.nickname)
    store.add((person, RDF.type, FOAF["Person"]))
    # person information
    for key in person_orm.__dict__.keys():
        if person_orm.__dict__[key] and not key.endswith('id') and not key in ['mbox_sha1sum', 'modulus', 'public_exponent']:
            value = getattr(person_orm, key)
            if key=='seeAlso':
                store.add((person_uri, RDFS[key], URIRef(value)))
            else:
                store.add((person_uri, FOAF[key], Literal(value)))

    if person_orm.modulus:
        cert = BNode()
        store.add((cert, RDF.type, RSA['RSAPublicKey']))
        store.add((cert, CERT['identity'], person_uri))
    
        modulus = BNode()
        store.add((cert, RSA['modulus'], modulus))
        store.add((modulus, CERT['hex'], Literal(person_orm.modulus)))
        
        exponent = BNode()
        store.add((cert, RSA['public_exponent'], exponent))
        store.add((exponent, CERT['decimal'], Literal(person_orm.public_exponent)))

    profile = person
    store.add((profile, RDF.type, FOAF['PersonalProfileDocument']))
    store.add((profile, FOAF['maker'], person_uri))
    store.add((profile, FOAF['primaryTopic'],person_uri))

    rdf=store.serialize(format="pretty-xml", max_depth=10)
#        store.close()
##        error=str(out)
#        file='\n'.join(out)
#        path=settings.FOAF_DATA+self.nickname+'.rdf'
#        local_file=open(path,'w')
#        local_file.write(out)
#        local_file.close()
    return rdf


"""

  <rdf:Description rdf:about="#me">
    <rdf:type rdf:resource="http://xmlns.com/foaf/0.1/Person"/>
    <ns0:nick>test25</ns0:nick>
    <ns0:homepage rdf:resource=""/>
  </rdf:Description>

  <rdf:Description rdf:about="">
    <rdf:type rdf:resource="http://xmlns.com/foaf/0.1/PersonalProfileDocument"/>
    <ns0:maker rdf:resource="#me"/>
    <ns0:primaryTopic rdf:resource="#me"/>
  </rdf:Description>

  <rdf:Description rdf:about="#cert">
    <rdf:type rdf:resource="http://www.w3.org/ns/auth/rsa#RSAPublicKey"/>
    <ns1:identity rdf:resource="#me"/>
    <ns2:modulus rdf:resource="#modulus"/>
    <ns2:public_exponent rdf:resource="#public_exponent"/>
  </rdf:Description>

  <rdf:Description rdf:about="#modulus"> <ns1:hex>D148F40BC9E894ED116DC8929DD3606D31C74A815BCD100EDF185BFC3F5AD0CAB2F78B9AC39638A86DBFEF27D017D34C1C840D81DC097F540F6D3058CE7409D1868DDD47AF17BB379C99DE4F3908AF51B893C47D4812C87286A9482D7D4132761F09503ABF7040F10EDD11A9BCB3F1A4EF4E863D636E3C278524BBBE10D69467414712B86A544F291D6106634FDD4D3AAF92470CBA02ABB562FD1DE616C4E800DD4CA8653B7ABE0D8F457D423059622F55F63C2F1B8B3187D1F39FEFAC586DE0569FC26CCF472DA8CC4475B1D39BD196F43DB7052B2A291479442D43AEB4F46C07C4BFC038D038C47BA2814B6B2E33547755FB4AB90C5B9C4D3FFB5FE0FE349B</ns1:hex>
  </rdf:Description>

  <rdf:Description rdf:about="#public_exponent">
    <ns1:decimal>65537</ns1:decimal>
  </rdf:Description>



"""


#    def toRDF(self):
#    
#        #rdf graph
#        store = ConjunctiveGraph()
#        
#        #namespaces
#        store.bind('sioc', SIOC)
#        store.bind('foaf', FOAF)
#        store.bind('dc', DC)
#        store.bind('rel', REL)
#        store.bind('doap', DOAP)
#        store.bind('air', AIR)
#        store.bind('contact', CONTACT)
#        store.bind('rss', RSS)

#        # person graph
#        person = URIRef(settings.FOAF_URI+self.nickname+'.rdf')
#        store.add((person, RDF.type, FOAF["Person"]))

##        # 1. search for other classes with foreign key to this
##        # 1a. get all models from current app
##        from django.db.models.loading import get_models, load_app
##        app_models = get_models(load_app(self._meta.app_label))
##        this_class_name = self.__class__.__name__.lower()
##        # or self._meta.module_name
##        # 2. for each model get the related objects
##        for app_model in app_models:
##            app_model.objects.get(this_class_name=self)
##        # the same with self._meta._related_many_to_many_cache?
#        
#        for friend in self.person_from_set.all():
#            self.addFriend(store, person, friend)

##        for friend in self.person_from_set.all():
##            if friend.person_to.seeAlso:
##                uri = str(friend.person_to.seeAlso+'#me')
##                friend_uri = URIRef(uri)
##            else:
##                uri = settings.FOAF_URI+str(friend.person_to.nickname)+'.rdf'
##                friend_uri = URIRef(uri)
##            for relationship_type in friend.relationship.all():
##                store.add((person, REL[str(relationship_type.name)], friend_uri)) #get_name_display()

#        # project graphs
#        for project in self.currentProject.all():
#            self.addProject(store, person, project)

#        # knowledge graphs
#        for knowledge in self.knowledge.all():
#            self.addKnowledge(store, person, knowledge)

#        # interest graphs
#        for interest in self.interests.all():
#            self.addInterest(store, person, interest)
#            
#        # the weblog graph
#        if self.weblog:
#            self.addForum(store, person,  self.weblog)
#            
#        # coordinates
#        if len(self.basednear_set.all()) == 1:
#            self.addCoordinate(store, person, self.basednear_set.all()[0])
#        
#        # nearest airport
#        if len(self.nearestairport_set.all()) == 1:
#            self.addAirport(store, person, self.nearestairport_set.all()[0])
#        
#        # account
#        for account in self.holdsaccount_set.all() :
#            self.addAccount(store, person, account)
#        
#        # person information
#        for key in self.__dict__.keys():
#            if not key in ['id', 'mbox', 'user_id', 'weblog_id', '_weblog_cache'] and self.__dict__[key]:
#                value = str (self.__dict__[key])
#                store.add((person, FOAF[key], Literal(value)))
#            if key=='seeAlso' and self.__dict__[key]:
#                value = str (self.__dict__[key]) 
#                store.add((person, RDFS[key], URIRef(value)))


#        out=store.serialize(format="pretty-xml", max_depth=10)
#        store.close()
##        error=str(out)
#        file='\n'.join(out)
#        path=settings.FOAF_DATA+self.nickname+'.rdf'
#        local_file=open(path,'w')
#        local_file.write(out)
#        local_file.close()
##        return out
#    
#    def addCoordinate(self, store, person, coordinate):
#        """
#        Add the coordinates
#        
#        @param graph: person graph
#        @param url: forum url
#        """        
#        lat = str(coordinate.lat)
#        lon = str(coordinate.long)
#        if (lat != None and lon != None): 
#            store.bind('geo', GEO)                       
#            geo = BNode()
#            store.add((person, FOAF['based_near'], geo))
#            store.add((geo, RDF.type, GEO['Point']))
#            store.add((geo, GEO['lat'], Literal(lat)))
#            store.add((geo, GEO['long'], Literal(lon)))
#                
#    def addForum(self, store, person, weblog):
#        """
#        Add the forum
#        
#        @param graph: person graph
#        @param url: forum url
#        """
#        if weblog.forum:
#            forum = str(weblog.forum)
#            forum_uri = URIRef(forum)
#        else:
#            forum_uri = BNode()
#        store.add((person, FOAF['weblog'], forum_uri))
#        store.add((forum_uri, RDF.type, SIOC['Forum']))
##        if weblog.type:
##            store.add((forum_uri, RDF.type, URIRef(str(weblog.type))))
#        if weblog.channel:
#            store.add((forum_uri, RSS["channel"], URIRef(str(weblog.channel))))
#        if weblog.has_owner:
#            store.add((forum_uri, SIOC['has_owner'], URIRef(str(weblog.has_owner))))
#        if weblog.title:
#            store.add((forum_uri, DC['title'], Literal(str(weblog.title))))

#    def addInterest(self, store, person, interest):
#        """
#        Add the interest
#        
#        @param graph: person graph
#        @param url: interest url
#        """
#        if interest.description:
#            description = str(interest.description)
#            interest_uri =  URIRef(description)
#            store.add((person, FOAF['interest'], interest_uri))
#            store.add((interest_uri, RDF.type, RDF['Description']))
#        else: 
#            interest_uri = BNode()
#            store.add((person, FOAF['interest'], interest_uri))
#        if interest.title:
#            store.add((interest_uri, DC['title'], Literal(str(interest.title))))
#                
#    def addProject(self, store, person, project):
#        """
#        Add the project
#        
#        @param graph: person graph
#        @param url: project url
#        """
#        project_node = BNode()
#        store.add((person, FOAF['currentProject'], project_node))
#        store.add((project_node, RDF.type, DOAP['Project']))
##        if project.seeAlso: 
##            graph.add((graph, RDFS['seeAlso'], URIRef(str(project.seeAlso))))
#        if project.identifier:
#            store.add((project_node, DOAP['homepage'], URIRef(str(project.identifier))))
#        if project.description:
#            store.add((project_node, DOAP['description'], Literal(str(project.description))))
#        if project.title:
#            store.add((project_node, DOAP['name'], Literal(str(project.title))))
#    
#    def addFriend(self, store, person, friend):
#        """
#        Add the friend
#        
#        @param graph: person graph
#        @param url: forum url
#        """
#        if friend.person_to.seeAlso:
#            uri = str(friend.person_to.seeAlso+'#me')
#            friend_uri = URIRef(uri)
#        else:
#            uri = settings.FOAF_URI+str(friend.person_to.nickname)+'.rdf'
#            friend_uri = URIRef(uri)
##        friend_uri = BNode()
#        store.add((person, FOAF['knows'], friend_uri))
#        store.add((friend_uri, RDF.type, FOAF['Person']))
#        store.add((friend_uri, FOAF['nick'], Literal(str(friend.person_to.nickname))))
#        store.add((friend_uri, FOAF['mbox_sha1sum'], Literal(str(friend.person_to.mbox_sha1sum))))
#        if friend.person_to.homepage:
#            store.add((friend_uri, FOAF['homepage'], URIRef(str(friend.person_to.homepage))))
##        if friend.person_to.seeAlso:
##            store.add((friend_uri, RDFS["seeAlso"], URIRef(str(friend.person_to.seeAlso))))
#        store.add((friend_uri, RDFS["seeAlso"], friend_uri))

#    def addKnowledge(self, store, person, knowledge):
#        """
#        Add the interest
#        
#        @param graph: person graph
#        @param url: interest url
#        """
#        if knowledge.description:
#            description = str(knowledge.description)
#            knowledge_uri =  URIRef(description)
#            store.add((person, FOAF['knowledge'], knowledge_uri))
#            store.add((knowledge_uri, RDF.type, RDF['Description']))
#        else: 
#            knowledge_uri = BNode()
#            store.add((person, FOAF['knowledge'], knowledge_uri))
#        if knowledge.title:
#            store.add((knowledge_uri, DC['title'], Literal(str(knowledge.title))))

#    def addAccount(self, store, person, account):
#        """
#        Add the account
#        
#        @param graph: person graph
#        @param url: account url
#        """
#        if account.about:
#            about = str(account.about)
#            about_uri =  URIRef(about)
#            store.add((person, FOAF['holdsAccount'], about_uri))
#            store.add((about_uri, RDF.type, SIOC['User']))
#        else: 
#            about_uri = BNode()
#            store.add((person,  FOAF['holdsAccount'], about_uri))
#        if account.name:
#            store.add((about_uri, SIOC['name'], Literal(str(account.name))))
#        if account.accountServiceHomepage:
#            store.add((about_uri, FOAF['accountServiceHomepage'], URIRef(str(account.accountServiceHomepage))))
#        if account.accountProfilePage:
#            store.add((about_uri, FOAF['accountProfilePage'], URIRef(str(account.accountProfilePage))))
#        if account.sameAs:
#            store.add((about_uri, RDFS['sameAs'], URIRef(str(account.sameAs))))
#        if account.seeAlso:
#            store.add((about_uri, RDFS['seeAlso'], URIRef(str(account.seeAlso))))

#    def addAirport(self, store, person, airport):
#        """
#        Add the account
#        
#        @param graph: person graph
#        @param url: account url
#        """
#        if airport.about:
#            about = str(airport.about)
#            about_uri =  URIRef(about)
#            store.add((person, CONTACT['nearestAirport'], about_uri))
#            store.add((about_uri, RDF.type, AIR['Airport']))
#        else: 
#            about_uri = BNode()
#            store.add((person,  CONTACT['nearestAirport'], about_uri))
#        if airport.iataCode:
#            store.add((about_uri, AIR['iataCode'], Literal(str(airport.iataCode))))
#        if airport.title:
#            store.add((about_uri, DC['title'], URIRef(str(airport.title))))

##        <dc:title xml:lang="es">Aeropuerto de Madrid</dc:title>
#            
#    def getShaMail(self,mail):
#        """
#        Services to obtain encrypted email address
#        
#        @param mail: an email address
#        @type mail: string
#        @return: encryted mail on foaf:mbox_sha1sum format
#        @rtype: string
#        """ 
#        mail = mail.lower() # I'm no sure if it's a good idea...
#        return sha.new('mailto:'+mail).hexdigest()
#        
