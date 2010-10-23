#!/usr/bin/env python

from circuits import Component, Debugger
from circuits.net.sockets import TCPClient, Connect
from circuits.net.protocols.irc import IRC, Message, User, Nick, Join

class Bot(Component):

    def __init__(self, host, port=6667, channel=None):
        super(Bot, self).__init__(channel=channel)
        self += TCPClient(channel=channel) + IRC(channel=channel)
        self.push(Connect(host, port), "connect")
        self.count = 0

        self._cmd_plugins = {}
        self._log_plugins = []

    def registerPlugin(self, plugin):
        if plugin.getType() == 'command':
            commandList = plugin.getCommands()
            for c in commandList:
                self._addCmdPlugin(c, plugin)
        elif plugin.getType() == 'log':
            self._log_plugins.append(plugin)
        else:
            raise exception, "Unknown plugin type %s" % str(plugin.getType())

    def _addCmdPlugin(self, cmd, plugin):
        if cmd not in self._cmd_plugins.keys():
            self._cmd_plugins[cmd] = []
        self._cmd_plugins[cmd].append(plugin)

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
