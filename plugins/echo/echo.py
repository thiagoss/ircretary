#from core import CommandPlugin

class CommandPlugin(object): pass


doEcho = lambda ins, d: d['message']


class Echo(CommandPlugin):

    @property
    def getCommands(self):
        return ['echo', 'repeteae']

    echo = repeteae = doEcho


if __name__ == '__main__':
    echo = Echo()
    print echo.echo({'message': 'hahaha'})
