import os

class randomOSObject():
    def __init__(self, filepath):
        self.randomFile = open(filepath, 'r')

    def stripFile(self):
        return int(self.randomFile.readline().strip())

    def randomOS(self, u):
        randomInt = self.stripFile()
        return 1 + randomInt % u