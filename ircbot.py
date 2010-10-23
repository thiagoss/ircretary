#!/usr/bin/env python

from circuits import Component, Debugger
from circuits.net.sockets import TCPClient, Connect
from circuits.net.protocols.irc import IRC, Message, User, Nick, Join

class Bot(Component):

    def __init__(self, properties):
        self.server = properties['server']
        self.port = properties.get('port', 6667)
        self.nick = properties.get('nick', 'romeryto')
        self.my_channels = properties.get('channels')
        self.welcome_message = properties.get('welcome_msg', 'Oie')
        channel = 'bot'
        super(Bot, self).__init__(channel=channel)
        self += TCPClient(channel=channel) + IRC(channel=channel)
        self.push(Connect(self.server, int(self.port)), "connect")
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
        self.push(User(self.nick, host, host, "tuitador"), "USER")
        self.push(Nick(self.nick), "NICK")
        for channel in self.my_channels:
            self.push(Join(channel), "JOIN")
            self.push(Message(channel, self.welcome_message), "PRIVMSG")

    def numeric(self, source, target, numeric, args, message):
        if numeric == 433:
            self.push(Nick("%s_" % self("getNick")), "NICK")

    def message(self, source, target, message):
        nick = source[0]
        channel = message[1]
        msg = message[2]
        output = Output(self, channel)

        parameters = {}
        parameters['user'] = nick
        parameters['channel'] = channel
        parameters['msg'] = msg
        parameters['output'] = output
        for log_plugin in self._log_plugins:
            log_plugin.message(parameters)

        #parse message for commands
        if msg.startswith('!'):
            tokens = msg.split(' ')
            name = tokens[0][1:]
            parameters['msg'] = ' '.join(tokens[1:])
            plugins = self._cmd_plugins[name]
            for p in plugins:
                f = getattr(p, name)
                f(parameters)

class Output:
    def __init__(self, bot, channel):
        self.bot = bot
        self.channel = channel

    def write(self, msg, channel=None):
        if channel == None:
            channel = self.channel
        self.bot.push(Message(channel, msg))


if __name__=="__main__":
    import properties_manager
    properties = properties_manager.get_properties()
    
    bot = Bot(properties) + Debugger()
    #bot = Bot()
    bot.run()
