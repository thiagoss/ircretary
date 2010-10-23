#from core import CommandPlugin

class CommandPlugin(object):

    def getType(self):
        return 'command'

    def getCommands(self):
        return []



doEcho = lambda ins, d: d['message']


class Echo(CommandPlugin):

    @property
    def getCommands(self):
        return ['echo', 'repeteae']

    echo = repeteae = doEcho


if __name__ == '__main__':
    echo = Echo()
    print echo.echo({'message': 'hahaha'})
