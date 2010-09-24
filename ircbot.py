#!/usr/bin/env python

import twitter
from circuits import Component, Debugger
from circuits.net.sockets import TCPClient, Connect
from circuits.net.protocols.irc import IRC, Message, User, Nick, Join

api = twitter.Api(username='test', password='test')

class Bot(Component):

    def __init__(self, host, port=6667, channel=None):
        super(Bot, self).__init__(channel=channel)
        self += TCPClient(channel=channel) + IRC(channel=channel)
        self.push(Connect(host, port), "connect")
        self.count = 0

    def connected(self, host, port):
        self.push(User("tuite", host, host, "tuitador"), "USER")
        self.push(Nick("tuite"), "NICK")
        self.push(Join('#embedded-ufcg'), "JOIN")

    def numeric(self, source, target, numeric, args, message):
        if numeric == 433:
            self.push(Nick("%s_" % self("getNick")), "NICK")

    def message(self, source, target, message):
        if '!twit' in message:
            message = message.split('!twit')[1]
            self.count += 1

            try:
                status = api.PostUpdate(message)
                message = 'Twitted (' + status.text + ')'

                if self.count > 4:
                    message += ' (delicious spam: http://www.twitter.com/_lolwtf)'
                    self.count = 0

            except Exception, e:
                message = 'Failed to twit! :-(', e

            self.push(Message('#embedded-ufcg', message.strip()), "PRIVMSG")

        #self.push(Message(source[0], message), "PRIVMSG")

bot = Bot("irc.freenode.net", channel="bot") + Debugger()
bot.run()
