#http://www.helpim.org/browser/attic/version_2/HelpIM/jabberutils.py?rev=622&format=raw

import pyxmpp.all
import pyxmpp.jabber.all
import pyxmpp.jabber.vcard
from pyxmpp.jabber.clientstream import LegacyAuthenticationError, RegistrationError

#import HelpIM.logger
import logging

#log = logging.getLogger('HelpIM.chatbot')
#logger = log # make logger object for pyxmpp

class JabberUtil(pyxmpp.jabber.client.JabberClient):

    def __init__(self, username, server, password, nickname=None):
        # First set some constants
        self.timeout = 2
        self.resource = "HelpIM_util"
        # Set default vCard content
        self.vCard_data = """BEGIN:vCard
VERSION:3.0
N:HelpIM user
END:vCard"""
        # Set the nickname
        if nickname:
            self.nickname = nickname
        else:
            self.nickname = username
        # initialize a jabber client
        jid = pyxmpp.jid.JID(username, server, self.resource)
        pyxmpp.jabber.client.JabberClient.__init__(self, jid, password)

    def session_started(self):
        """Request the roster and set the presence with a priority of 1,
        This avoids 'hijacking' the session of someone is online, Psi
        defaults to 5."""
        print "session_started"
        self.request_roster()
        p = pyxmpp.Presence(priority=1)
        self.stream.send(p)

        # Set handlers for the presence-stanza's: whe want to add others to
        # our roster. Kindly taken from the echobot example.
        self.stream.set_presence_handler("subscribe", self.presence_control)
        self.stream.set_presence_handler("subscribed", self.presence_control)
        self.stream.set_presence_handler("unsubscribe", self.presence_control)
        self.stream.set_presence_handler("unsubscribed", self.presence_control)

    def presence_control(self, stanza):
        """Handle subscription control <presence/> stanzas -- acknowledge
        them."""
        p=stanza.make_accept_response()
        self.stream.send(p)
        return True

    def loop_until_handled(self, timeout=None):
        if not timeout:
            timeout = self.timeout
        while self.stream is not None and \
              not self.stream.eof and \
              self.stream.socket is not None:
            try:
                act=self.stream.loop_iter(timeout)
            except LegacyAuthenticationError:
                return
            if not act:
                self.stream.idle()
                return
        return

    def register(self, user_list=None, disconnect=True):
        """Handle in-band registration and set vCard. If a userlist is defined,
        then the new registered user wil be added to the rosters of all users in
        the userlist. The user_list must be a list of dictionaries, one
        dictionary for each user. Each dictionary must have the following keys:
        username
        server
        password
        nickname"""
        self.connect(register=True)
        self.loop_until_handled()
        self.disconnect()
        self.loop_until_handled()

        # And set the vCard too
        vcard = pyxmpp.jabber.vcard.VCard(self.vCard_data)
        iq = pyxmpp.iq.Iq(stanza_type='set')
        iq.set_content(vcard)
        self.connect()
        self.loop_until_handled()
        self.stream.send(iq)
        self.loop_until_handled()
        # And add to others roster
        if user_list:
            self.mutual_subscribe_to_list(user_list, 'subscribe')
        if disconnect:
            self.disconnect()
            self.loop_until_handled()
        return

    def unregister(self, user_list=None):
        """Handle in-band unregistration. Also unsubscribes from others roster.
        If a userlist is defined, then the unregistered user wil 'gently' be
        removed from the rosters of all users in the userlist. Otherwise those
        users will be bothered by some removal messages. The user_list must be
        a list of dictionaries, one dictionary for each user. Each dictionary
        must have the following keys:
        username
        server
        password
        nickname"""
        # First connect as usual
        # Let Authentification errors escalate to the calling program
        self.connect()
        self.loop_until_handled()
        
        # And remove from others rosters
        if user_list: # we have a user_list, lets do it in the royal way
            self.mutual_subscribe_to_list(user_list, 'unsubscribe')
        else: # no user_list? bluntly unsubscribe!
            for item in c.roster.get_items():
                p = pyxmpp.presence.Presence(from_jid=self.jid, to_jid=item.jid, stanza_type="unsubscribe")
                self.stream.send(p)
                p = pyxmpp.presence.Presence(from_jid=self.jid, to_jid=item.jid, stanza_type="unsubscribed")
                self.stream.send(p)
            self.loop_until_handled()
        
        # Make removal-form:
        form = pyxmpp.jabber.register.Register()
        form.remove = True
        # Make iq to send it with and send it
        iq = pyxmpp.iq.Iq(to_jid=pyxmpp.jid.JID(None, self.jid.domain), stanza_type = "set")
        iq.set_content(form)
        self.stream.send(iq)
        self.loop_until_handled()
        
        # finally disconnect
        # Note: some servers cache rosters, so it might not be in effect
        # immediatly.
        c.disconnect()
        self.loop_until_handled()

    def send_subscription(self, to_jid, type):
        if type not in ['subscribe', 'unsubscribe', 'subscribed', 'unsubcribed']:
            raise TypeError, 'Invalid type of subscription'
        
        p = pyxmpp.presence.Presence(from_jid=self.jid, to_jid=to_jid, stanza_type=type)
        self.stream.send(p)
        self.loop_until_handled(0.2)

    def mutual_subscribe(self, sec, type):
        self.send_subscription(pyxmpp.jid.JID(node_or_jid=sec.jid.node, domain=sec.jid.domain), type)
        sec.send_subscription(pyxmpp.jid.JID(node_or_jid=self.jid.node, domain=self.jid.domain), type)
        self.loop_until_handled()
        sec.loop_until_handled()

    def mutual_update_roster(self, sec, type):
        if type == "subscribe":
            self_ri = pyxmpp.roster.RosterItem(pyxmpp.jid.JID(node_or_jid=sec.jid.node,
                                                             domain=sec.jid.domain),
                                              subscription='both',
                                              name=sec.nickname)
            sec_ri = pyxmpp.roster.RosterItem(pyxmpp.jid.JID(node_or_jid=self.jid.node,
                                                             domain=self.jid.domain),
                                              subscription='both',
                                              name=self.nickname)
        elif type == "unsubscribe":
            self_ri = self.roster.remove_item(pyxmpp.jid.JID(node_or_jid=sec.jid.node,
                                                           domain=sec.jid.domain))
            sec_ri = sec.roster.remove_item(pyxmpp.jid.JID(node_or_jid=self.jid.node,
                                                           domain=self.jid.domain))
        self.stream.send(self_ri.make_roster_push())
        sec.stream.send(sec_ri.make_roster_push())
        sec.loop_until_handled()
 
    def mutual_subscribe_to_list(self, user_list, type):
        """Subscribes or unsubscribes the first user of the list to the other
        users in user_list and visa versa. The user_list is a list of
        dictionaries, one dictionary for each user. Each dictionary must have
        the following keys:
        username
        server
        password
        nickname
        The second argument might be 'subscribe' or 'unsubscribe'."""

        for user in user_list:
            sec = JabberUtil(user['username'], user['server'], user['password'], user['nickname'])
            sec.connect()
            sec.loop_until_handled()
            self.mutual_subscribe(sec, type)
            self.mutual_update_roster(sec, type)
            sec.disconnect()
            sec.loop_until_handled()

        self.loop_until_handled() # make sure nothing is hanging in the air

    def subscribe_to_list(self, userlist, type):
        for user in userlist:
            self.send_subscription(pyxmpp.jid.JID(user['username'], user['server']), type)
            if type == "subscribed":
                ri = pyxmpp.roster.RosterItem(pyxmpp.jid.JID(
                                                    user['username'],
                                                    user['server']),
                                              subscription='both',
                                              name=user['nickname'])
            elif type == "unsubscribed":
                ri = self.roster.remove_item(pyxmpp.jid.JID(
                                                    user['username'],
                                                    user['server']))
            self.stream.send(ri.make_roster_push())

    def push_roster_of_list(self, userlist, type):
        for user in userlist:
            if type == "subscribe":
                self_ri = pyxmpp.roster.RosterItem(pyxmpp.jid.JID(
                                                        user['username'],
                                                        user['server']),
                                                  subscription='both',
                                                  name=user['nickname'])
            elif type == "unsubscribe":
                self_ri = self.roster.remove_item(pyxmpp.jid.JID(node_or_jid=sec.jid.node,
                                                               domain=sec.jid.domain))
            self.stream.send(self_ri.make_roster_push())
