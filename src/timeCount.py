class TimeCounter():
    def __init__(self):
        self.currentTimeCount = 0

    def getTimeCount(self):
        return self.currentTimeCount

    def updateTimeCount(self):
        self.currentTimeCount += 1
