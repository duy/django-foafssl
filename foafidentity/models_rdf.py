
from rdfalchemy import rdfSubject, rdfSingle, rdfMultiple
from rdflib import Namespace

FOAF=Namespace("http://xmlns.com/foaf/0.1/" )
RDFS=Namespace("http://www.w3.org/2000/01/rdf-schema#")
REL=Namespace("http://purl.org/vocab/relationship/")
CERT=Namespace("http://www.w3.org/ns/auth/cert#")
RSA=Namespace("http://www.w3.org/ns/auth/rsa#")


class Agent(rdfSubject):
  rdf_type=FOAF.Agent
  name=rdfSingle(FOAF.name)
  mbox=rdfSingle(FOAF.mbox)
  openid=rdfSingle(FOAF.openid)
  weblog=rdfSingle(FOAF.weblog)
  seeAlso=rdfSingle(RDFS.seeAlso)

class Person(Agent):
  rdf_type=FOAF.Person
  nickname=rdfSingle(FOAF.nick)
#  firstName=rdfSingle(FOAF.firstName)
#  givenname=rdfSingle(FOAF.givenname)
#  surname=rdfSingle(FOAF.surname)
#  family_name=rdfSingle(FOAF.family_name)
#  knows=rdfMultiple(FOAF.knows,range_type=FOAF.Person)
  homepage=rdfSingle(FOAF.homepage)
#  workplaceHomepage=rdfSingle(FOAF.workplaceHomepage)
#  workInfoHomepage=rdfSingle(FOAF.workInfoHomepage)
#  schoolHomepage=rdfSingle(FOAF.schoolHomepage)
#  interests=rdfMultiple(FOAF.interest)
#  depiction=rdfSingle(FOAF.depiction)
#  knowsByReputation=rdfMultiple(REL.knowsByReputation,range_type=FOAF.Person)
#  friendOf=rdfMultiple(REL.friendOf,range_type=FOAF.Person)
#  worksWith=rdfMultiple(REL.worksWith,range_type=FOAF.Person)
#  wouldLikeToKnow=rdfMultiple(REL.wouldLikeToKnow,range_type=FOAF.Person)
#  hasMet=rdfMultiple(REL.hasMet,range_type=FOAF.Person)

class PersonalProfileDocument(rdfSubject):
  rdf_type=FOAF.PersonalProfileDocument
  maker=rdfSingle(FOAF.maker)
  primaryTopic=rdfSingle(FOAF.primaryTopic)
