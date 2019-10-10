from timeCount import TimeCounter
import helper
import sys
import process
from randomOS import randomOSObject


# First Come First Serve (FCFS)
class FCFS():
    def __init__(self):
        # Setting up random numbers from random number text file
        # The file name can be changed from the global variables on top
        helper.randomObj = randomOSObject(helper.RandomNumberText)

        # Reseting global time value to keep track of time for FCFS
        # currTime = TimeCounter()
        self.currentTime = helper.currTime = TimeCounter()

    def run(self, process):
        # while (process.processStatus != 4):
        while not process.isTerminated():
            # verbose function needed

            process.updateAllTime()             # updating all time
            process.updateAllStatus()           # updating process status

            if len(process.retrieveStatus(2)) == 0:
                nextProcess = process.retrieveStatus(1)
                nextProcess = nextProcess.inputOrderSort()
                nextProcess = nextProcess.firstArrivedSort()
                nextProcess = nextProcess.readyOrderSort()
                if len(nextProcess) > 0:
                    nextProcess.pop(0).runProcess()
            self.currentTime.updateTimeCount()
        print("\n")
        print("The scheduling algorithm used was First Come First Served\n")
        process.printDataSummary()


# Round Robin (RR)
class RR():
    def __init__(self):
        # Setting up random numbers from random number text file
        # The file name can be changed from the global variables on top
        helper.randomObj = randomOSObject(helper.RandomNumberText)

        # Reseting global time value to keep track of time for FCFS
        self.currentTime = helper.currTime = TimeCounter()

    def run(self, process, currQuantum):
        helper.RRquantum = currQuantum
        # while (process.processStatus != 4):
        # while(process.isTerminated() == False):
        while not process.isTerminated():
            # print("hello")
            # verbose function needed
            process.updateAllTime()             # updating all time
            process.updateAllStatus()           # updating process status

            if len(process.retrieveStatus(2)) == 0:
                nextProcess = process.retrieveStatus(1)
                nextProcess = nextProcess.inputOrderSort()
                nextProcess = nextProcess.firstArrivedSort()
                nextProcess = nextProcess.readyOrderSort()
                if len(nextProcess) > 0:
                    nextProcess.pop(0).runProcess()
            self.currentTime.updateTimeCount()
        print("\n")
        print("The scheduling algorithm used was Round Robin\n")
        process.printDataSummary()
        helper.RRquantum = False

# Shortest Job First (SJF)


class SJF():
    def __init__(self):
        # Setting up random numbers from random number text file
        # The file name can be changed from the global variables on top
        helper.randomObj = randomOSObject(helper.RandomNumberText)

        # Reseting global time value to keep track of time for FCFS
        self.currentTime = helper.currTime = TimeCounter()

    def run(self, process):
        # while (process.processStatus != 4):
        while(process.isTerminated() == False):
            # verbose function needed
            process.updateAllTime()             # updating all time
            process.updateAllStatus()           # updating process status

            if len(process.retrieveStatus(2)) == 0:
                nextProcess = process.retrieveStatus(
                    1).inputOrderSort().firstArrivedSort().jobOrderSort()
                # nextProcess = getattr(nextProcess, sortType)
                if len(nextProcess) > 0:
                    nextProcess.pop(0).runProcess()
            self.currentTime.updateTimeCount()
        print("\n")
        print("The scheduling algorithm used was Shortest Job First\n")
        process.printDataSummary()

# Highest Priority Ratio Next (HPRN)


class HPRN():
    def __init__(self):
        # Setting up random numbers from random number text file
        # The file name can be changed from the global variables on top
        helper.randomObj = randomOSObject(helper.RandomNumberText)

        # Reseting global time value to keep track of time for FCFS
        self.currentTime = helper.currTime = TimeCounter()

    def run(self, process):
        # while (process.processStatus != 4):
        while(process.isTerminated() == False):
            # verbose function needed
            process.updateAllTime()             # updating all time
            process.updateAllStatus()           # updating process status

            if len(process.retrieveStatus(2)) == 0:
                nextProcess = process.retrieveStatus(
                    1).inputOrderSort().firstArrivedSort().ratioSort()
                # nextProcess = getattr(nextProcess, sortType)
                if len(nextProcess) > 0:
                    nextProcess.pop(0).runProcess()
            self.currentTime.updateTimeCount()
        print("\n")
        print("The scheduling algorithm used was Highest Priority Ratio Next\n")
        process.printDataSummary()

##### End of Scheduler Implementation #####
