#!/usr/bin/env python
# -*- coding: utf-8 -*-

from circuits import Component, Debugger
from circuits.net.sockets import TCPClient, Connect
from circuits.net.protocols.irc import IRC, Message, User, Nick, Join

import engine


class Bot(Component):

    Channel = '#ufcg'
    Nick = "tuite"

    def __init__(self, host, port=6667, channel=None):
        super(Bot, self).__init__(channel=channel)
        self += TCPClient(channel=channel) + IRC(channel=channel)
        self.push(Connect(host, port), "connect")
        self.engine = engine.Engine()

    def connected(self, host, port):
        self.push(User(Bot.Nick, host, host, "tuitador"), "USER")
        self.push(Nick(Bot.Nick), "NICK")
        self.push(Join(Bot.Channel), "JOIN")
        self.push(Message(Bot.Channel, "Cheguei ja sensualizando!"), "PRIVMSG")

    def numeric(self, source, target, numeric, args, message):
        if numeric == 433:
            self.push(Nick("%s_" % self("getNick")), "NICK")

    def say(self, msg):
        self.push(Message(Bot.Channel, msg.strip()), 'PRIVMSG')

    def reload_hook(self):
        global engine
        engine = reload(engine)
        del self.engine
        self.engine = engine.Engine()

    def message(self, source, target, message):
        if "!reload" in message:
            if len(source) > 0 and 'dieb' in source[0]:
                self.reload_hook()
                self.say('Engine reloaded!')
                return

        ans = self.engine.process(message)

        print ans

        if isinstance(ans, engine.Echo):
            print 'echoing back'
            self.say(ans)


bot = Bot("irc.freenode.net", channel="bot") + Debugger()
bot.run()
