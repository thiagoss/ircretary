# -*- coding: utf-8 -*-

#from core import LogPlugin

import random

class LogPlugin(object):

    def getType(self):
        return 'log'


class Romeryto(LogPlugin):
    def respond(self):
        # bigger the range, smaller the chance
        return 0 == random.randint(0, 17)

    def randResponse(self, data):
        responses = ['Concordo plenamente.', 'Parabéns %s' % data['user'],
                     'Ótima análise, %s' % data['user'],
                     'Obrigado pela A atenção',
                     '%s: e voce se orgulha disso?' % data['user'],
                     'Era exatamente o que eu ia dizer, %s' % data['user'],
                     '%s, tirou as palavras da minha boca!' % data['user'],
                     'Te amo minha Driihhh!']
        return responses[random.randint(0, len(responses) - 1)]

    def message(self, data):
        if self.respond():
            data['output'].write(self.randResponse(data))
