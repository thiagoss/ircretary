# -*- coding: utf-8 -*-

#from core import LogPlugin

import random

class LogPlugin(object):

    def getType(self):
        return 'log'


class Romeryto(LogPlugin):
    def respond(self):
        return 0 == random.randint(0, 0.5 * 100)

    def randResponse(self, data):
        responses = ['Concordo plenamente', 'Parabens %s' % data['user'],
                     'Otima analise %s' % data['user'],
                     'Obrigado pela A atenção']
        return responses[random.randint(0, len(responses) - 1)]

    def log(self, data):
        if self.respond():
            data['output'].write(self.randResponse(data), data['channel'])


class Output:

    def write(self, msg, channel=''):
        print '%s: %s' % (channel, msg)


if __name__ == '__main__':
    homer = Romeryto()

    for i in range(100):
        homer.log({'message': 'python é muito legal',
                   'user': 'dieb',
                   'output': Output(),
                   'channel': '#ufcg'})
