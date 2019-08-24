import random

class PowerPlant(object):
    '''Weirdly named random character generator'''
    def __init__(self):
        self.__voltage = 0
        self.__matrix = 'abcdefghijklmnopqrstuvwxyz123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ.,!?;:/\\\'"`|[]{}()*&^%$#@<>+=-_~'
        self.__rating = len(self.__matrix) - 1
        self.battery = ''

    def load_entropy(self, level = 10):
        self.__voltage = level

    def select(self, chartype = 'alpha'):
        if chartype == 'alpha':
            self.__matrix = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ'
            self.__rating = len(self.__matrix) - 1
        elif chartype == 'num':
            self.__matrix = '123456789'
            self.__rating = len(self.__matrix) - 1
        elif chartype == 'sym':
            self.__matrix = '.,!?;:/\\\'"`|[]{}()*&^%$#@<>+=-_~'
            self.__rating = len(self.__matrix) - 1
        elif chartype == 'alphanum':
            self.__matrix = 'abcdefghijklmnopqrstuvwxyz123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ'
            self.__rating = len(self.__matrix) - 1
        elif chartype == 'all':
            pass
        else:
            raise ValueError, 'Unknown chartype!'

    def __generate(self):
        electron = self.__matrix[random.randint(0, self.__rating)]
        return electron

    def generate(self):
        self.battery = ''
        while self.__voltage > 0:
            self.battery += self.__generate()
            self.__voltage -= 1
        return self.battery
