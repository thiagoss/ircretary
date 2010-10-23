#!/usr/bin/env python

import twitter
from circuits import Component, Debugger
from circuits.net.sockets import TCPClient, Connect
from circuits.net.protocols.irc import IRC, Message, User, Nick, Join

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
        pass

bot = Bot("irc.freenode.net", channel="bot") + Debugger()
bot.run()
