# -*- coding: utf-8 -*-

#from core import LogPlugin

import random

class LogPlugin(object):

    def getType(self):
        return 'log'


class Romeryto(LogPlugin):
    def respond(self):
        # bigger the range, smaller the chance
        return 0 == random.randint(0, 10)

    def randResponse(self, data):
        responses = ['Concordo plenamente', 'Parabens %s' % data['user'],
                     'Otima analise %s' % data['user'],
                     'Obrigado pela A atenção',
                     '%s: e voce se orgulha disso?' % data['user']]
        return responses[random.randint(0, len(responses) - 1)]

    def message(self, data):
        if self.respond():
            data['output'].write(self.randResponse(data))
