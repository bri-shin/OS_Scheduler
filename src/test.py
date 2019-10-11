
import sys
import os
import copy
import helper

### Helper Functions Implemented ###

### Random OS Object is created to generate random number when requested
class randomOSObject():
    def __init__(self, filepath):
        self.randomFile = open(filepath, 'r')

    def stripFile(self):
        return int(self.randomFile.readline().strip())

    def randomOS(self, u):
        randomInt = self.stripFile()
        return 1 + randomInt % u

### Counter Object is the overarching time counter for the program
class TimeCounter():
    def __init__(self):
        self.currentTimeCount = 0

    def getTimeCount(self):
        return self.currentTimeCount

    def updateTimeCount(self):
        self.currentTimeCount += 1


# Process Class (simulating a process and its necessary functions)

class Process():
    def __init__(self, A, B, C, M, processID):
        # Necessary Variables
        self.A = A                         # Arrival time of the process
        # Upper Bound of CPU burst times of the given random integer list
        self.B = B
        self.C = C                         # Total CPU time needed
        self.M = M                         # Multiplier of CPU burst time

        # The process ID given upon input read (order)
        self.processID = processID

        # 0: unstarted, 1: ready, 2: running, 3: blocked, 4: terminated
        self.processStatus = 0

        # The cycle when the the process finishes (initially -1)
        self.finishTime = 0
        self.turnaroundTime = 0          # finishTime - A
        self.blockedTime = 0            # Time in 'Blocked' (I/O) state
        self.waitingTime = 0            # Time in 'Ready' State
        self.runningTime = 0            # Time in 'Runing' State
        self.initialTime = 0            # Initial time when ready
        self.cpuUtilization = 0         # CPU Utilization
        self.ioUtilization = 0          # IO Utilization

        self.currBurst = 0              # Remaining time for any state
        self.prevBurst = 0              # Previous Burst length

        self.leftOverCPU = C            # Left over CPU time
        self.quantumCount = helper.RRquantum      # Left over quantum in RR

    # Updating time variables (i.e. current burst, left over CPU time, quantum, turnaround time, running time / waiting time / blocked time)
    def updateTime(self):
        # if not unstarted nor terminated
        # print(self.processStatus)
        if (self.processStatus != 0) and (self.processStatus != 4):
            self.turnaroundTime += 1

            # print("This is turnaround time", self.turnaroundTime)

            if self.processStatus == 2:
                if self.currBurst > 0:              # If current Burst remains, it is used and decreased by 1
                    self.currBurst -= 1
                # print(helper.RRquantum)
                if helper.RRquantum > 0:                   # IF quantum remains, it is used and decreased by 1
                    self.quantumCount -= 1
                    # print("hi")
                self.runningTime += 1               # Running time increases by 1
                self.leftOverCPU -= 1               # Left over CPU time decreases by 1
            elif self.processStatus == 1:
                self.waitingTime += 1
            elif self.processStatus == 3:
                if self.currBurst > 0:
                    self.currBurst -= 1
                    # print("Current Burst is:", currBurst)
                self.blockedTime += 1

        # print(self.leftOverCPU)
        # print("test test test")
        return

    # Updating the status of process
    def updateStatus(self):
        currentTimeCounter = helper.currTime.getTimeCount()
        if self.processStatus == 2:                 # Process is running
            if self.leftOverCPU == 0:
                self.processStatus = 4              # process terminated
                self.finishTime = currentTimeCounter
                
            elif self.currBurst == 0:               # If current burst is used up
                self.processStatus = 3              # process blocked
                self.currBurst = self.M * self.prevBurst
                
            elif self.quantumCount == 0:            # If quantum is used up
                self.processStatus = 1              # process ready / preempt
                self.initialTime = currentTimeCounter
                
        elif self.processStatus == 0:               # Process is unstarted
            if currentTimeCounter == self.A:
                self.processStatus = 1
                self.initialTime = currentTimeCounter
                
        elif self.processStatus == 3:               # Process is blocked
            if self.currBurst == 0:
                self.processStatus = 1
                self.initialTime = currentTimeCounter
                
        else:
            pass

        # print("hello")
        return self.processStatus
        

    # Running Process (+ Setting random burst)
    def runProcess(self):
        self.processStatus = 2
        if helper.RRquantum:
            self.quantumCount = helper.RRquantum
        # print("testestest:", self.currBurst)
        if self.currBurst == 0:
            # self.randomBurst
            self.prevBurst = helper.randomObj.randomOS(self.B)
            self.currBurst = self.prevBurst
            # print("testestest222:", self.currBurst)

    # Returning self.A 
    def firstArrived(self):
        return self.A

    # Printing initial Input
    def printInput(self):
        return "({} {} {} {})".format(self.A, self.B, self.C, self.M)

    # For verbose
    def __repr__(self):
        return "({} {} {} {})".format(self.A, self.B, self.C, self.M)

    # Printing the Result of Burst Status
    # def printResult(self):
    #     if self.processStatus == 0:
    #         processStatusStr = "unstarted"
    #     elif self.processStatus == 1:
    #         processStatusStr = "ready"
    #     elif self.processStatus == 2:
    #         processStatusStr = "running"
    #     elif self.processStatus == 3:
    #         processStatusStr = "blocked"
    #     elif self.processStatus == 4:
    #         processStatusStr = "terminated"

    #     printStatus = ('     ' + processStatusStr)
    #     if not helper.RRquantum:
    #         burstPrint = self.currBurst
    #     else:
    #         burstPrint = self.quantumCount
    #     printBurst = ('   '*3 + str(burstPrint))
    #     return printStatus + printBurst
    
    # def __str__(self):
    #     return "Hello"

    # For Verbose
    def __str__(self):
        if self.processStatus == 0:
            processStatusStr = "unstarted"
        elif self.processStatus == 1:
            processStatusStr = "ready"
        elif self.processStatus == 2:
            processStatusStr = "running"
        elif self.processStatus == 3:
            processStatusStr = "blocked"
        elif self.processStatus == 4:
            processStatusStr = "terminated"

        printStatus = ('          ' + processStatusStr)[-10:]
        if not helper.RRquantum:
            burstPrint = self.currBurst
            # print("First IF, currBurst is:", self.currBurst)
        else:
            burstPrint = self.quantumCount
            # print("SECOND IF")
        printBurst = ('   ' + str(burstPrint))[-3:]

        return printStatus + printBurst

    # Printing Overall Summary Data
    def printProcessSummary(self):
        print("\t(A,B,C,M)= ("+str(self.A)+','+str(self.B)+','+str(self.C)+','+str(self.M)+')')
        print("\tFinishing time:", self.finishTime)
        print("\tTurnaround time:", self.turnaroundTime)
        print("\tI/O time:", self.blockedTime)
        print("\tWaiting time", self.waitingTime,"\n")

    def getRatio(self):
        T = self.turnaroundTime
        t = max(1, self.runningTime)
        return T/t

    def __lt__(self,process):
        if self.A != process.A:
            return self.A < process.A
        else:
            return self.processID < process.processID
        


# Summary Data
# finishTime - when all processes have finished
# cpuUtilization = 0.0        # Percentage of time some job is running
# ioUtilization = 0.0         # The amount of time until the process finishes being blocked
# throughput = 0              # Processes completed per hundred time units
# IOBurst = 0                   # The amount of time until the process finishes being blocked
# # The CPU availability of the process (has to be > 1 to move to running)
# CPUBurst = 0
# quantum = 0                   # Used for schedulers that utilise pre-emption

# # Helper: Generating random variable from provided text file


# Helper: Creating Data Summary by inheriting from Process Class
# This class subclasses list in order to iterate through the processes for complete summary


class DataSummary(list):
    def __init__(self):
        super().__init__()
        self.ioUtilization = 0          # IO Utilization
        self.finishTime = 0
    
    def printAllInput(self):
        inputString = str(len(self))
        for i in self:
            inputString += i.printInput()
        return inputString

    # for verbose
    def __str__(self):
        inputString = ""
        for i in self:
            inputString += "{}".format(i)
        return inputString

    # for verbose
    def __repr__(self):
        inputString = str(len(self))
        for i in self:
            inputString += "{}".format(i.__repr__())
        return inputString


    def isTerminated(self):
        for element in self:
            if element.processStatus != 4:
                return False
        self.finishTime = helper.currTime.getTimeCount() - 1
        # print("This is finish time:",self.finishTime)
        return True

# Important things to keep in mind:
# - Cannot use sorted() as it returns a list by default
# - must use sort() as it sorts the object itself
# - lambda can come in handy

    # Sort by First Arrived
    # def firstArrived(self, process):
    #     return process.A

    # def firstArrivedSort(self):
    #     sortedList = sorted(self, key=firstArrived(process))
    #     return sortedList

    def firstArrivedSort(self):
        # self = sorted(self, key=lambda process: process.A)
        self.sort(key=lambda process: process.A)
        return self

    # Sort by Ready Order
    # def readyOrder(self):
    #     return self.initialTime

    def readyOrderSort(self):
        # self = sorted(self, key=lambda process: process.initialTime)
        self.sort(key=lambda process: process.initialTime)
        return self

    # Sort by Input Order
    # def inputOrder(self):
    #     return self.processID

    def inputOrderSort(self):
        # Cannot use sorted, as it returns a list instead of an object
        # self = sorted(self, key=lambda process: processID)
        self.sort(key=lambda process: process.processID)
        return self

    # Sort by Job
    # def jobOrder(self):
    #     return self.C - self.runningTime

    def jobOrderSort(self):
        # self = sorted(
        #     self, key=lambda process: process.C - process.runningtime)
        self.sort(key=lambda process: process.C - process.runningTime)
        return self

    # Sort by Ratio

    # (!) Might need ratio of process itself not process table
    # def getRatio(self):
    #     maxTime = max(1, self.runningTime)
    #     return (self.turnaroundTime / maxTime)

    def ratioSort(self):
        # self = sorted(self, key=lambda process: -process.getRatio())
        self.sort(key=lambda process: -process.getRatio())
        return self

    # Update all process's time
    def updateAllTime(self):
        for process in self:
            process.updateTime()

        # For blocked processes
        dataSummaryObj = DataSummary()

        for process in self:
            if process.processStatus == 3:
                dataSummaryObj.append(process)
        if len(dataSummaryObj) > 0:
            self.ioUtilization += 1
            # print("test test test")
    #
    # CHANGE TO FOR LOOP
    #

    def updateAllStatus(self):
        for process in self:
            process.updateStatus()

    # Checking status
    def retrieveStatus(self, status):
        dataSummaryObj = DataSummary()
        for process in self:
            if (process.processStatus == status):
                dataSummaryObj.append(process)
        return dataSummaryObj

    # def retrieveStatus(self, status):
    #     return self.checkStatus(status)

    def printDataSummary(self):
        self.firstArrivedSort()
        # Calculating CPU Utilization
        # print("This is finish time", self.finishTime)
        
        # Calculating Throughput
        # print("This is len(self)", len(self))
        throughput = 100*len(self) / self.finishTime
        
        cpuUtil = 0
        for process in self:
            cpuUtil += process.runningTime
        cpuUtil = cpuUtil / self.finishTime

        # Calculating IO Utilization
        ioUtil = self.ioUtilization / self.finishTime

        # Calulcating Average Turnaround Time
        avgTurnaroundTime = 0
        for process in self:
            avgTurnaroundTime += process.turnaroundTime
        avgTurnaroundTime = avgTurnaroundTime/len(self)

        # Calculating Average Waiting TIme
        avgWaitingTime = 0
        for process in self:
            avgWaitingTime += process.waitingTime
        avgWaitingTime = avgWaitingTime / len(self)

        # Printing Process Summary
        for iter, process in enumerate(self):
            print("Process", int(iter),":")
            process.printProcessSummary()
        print("Summary Data:")
        print("\t Finishing Time:", self.finishTime)
        print("\t CPU Utilization:", cpuUtil)
        print("\t I/O Utilization:", ioUtil)
        print("\t Throughput:", throughput, "processes per hundred cycle")
        print("\t Average turnaround time:", avgTurnaroundTime)
        print("\t Average waiting time:", avgWaitingTime)

##### End of Helper Function Implementation #####
# First Come First Serve (FCFS)
class FCFS():
    def __init__(self):
        # Setting up random numbers from random number text file
        # The file name can be changed from the global variables on top
        helper.randomObj = randomOSObject(helper.RandomNumberText)

        # Reseting global time value to keep track of time for FCFS
        # currTime = TimeCounter()
        # self.currentTime = currTime
        self.currentTime = helper.currTime = TimeCounter()

    def run(self, process):
        # while (process.processStatus != 4):
        while(process.isTerminated() == False):
            if (helper.verbose == True):
                print("Before cycle    "+str(self.currentTime.getTimeCount())+":     {}.".format(process))
            # verbose function needed
            # print("test test test")
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
        # currTime = TimeCounter()
        # self.currentTime = currTime
        self.currentTime = helper.currTime = TimeCounter()

    def run(self, process, currQuantum):
        helper.RRquantum = currQuantum
        # while (process.processStatus != 4):
        while(process.isTerminated() == False):
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
        # currTime = TimeCounter()
        # self.currentTime = currTime
        self.currentTime = helper.currTime = TimeCounter()

    def run(self, process):
        # while (process.processStatus != 4):
        while(process.isTerminated() == False):
            # verbose function needed
            process.updateAllTime()             # updating all time
            process.updateAllStatus()           # updating process status

            if len(process.retrieveStatus(2)) == 0:
                nextProcess = process.retrieveStatus(1)
                nextProcess = nextProcess.inputOrderSort()
                nextProcess = nextProcess.firstArrivedSort()
                nextProcess = nextProcess.jobOrderSort()
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
        # currTime = TimeCounter()
        # self.currentTime = currTime
        self.currentTime = helper.currTime = TimeCounter()

    def run(self, process):
        # while (process.processStatus != 4):
        while(process.isTerminated() == False):
            # verbose function needed
            process.updateAllTime()             # updating all time
            process.updateAllStatus()           # updating process status

            if len(process.retrieveStatus(2)) == 0:
                nextProcess = process.retrieveStatus(1)
                nextProcess = nextProcess.inputOrderSort()
                nextProcess = nextProcess.firstArrivedSort()
                nextProcess = nextProcess.ratioSort()
                if len(nextProcess) > 0:
                    nextProcess.pop(0).runProcess()
            self.currentTime.updateTimeCount()
        print("\n")
        print("The scheduling algorithm used was Highest Priority Ratio Next\n")
        process.printDataSummary()

##### End of Scheduler Implementation #####

def main():
    inputFile = []

    # Reading User Input
    fileName = sys.argv[-1]
    inputText = open(fileName, 'r')
    inputNumber = []
    for line in inputText:
        for digit in line.strip().split():
            if digit.isdigit():
                inputNumber.append(int(digit))
    inputText.close()

    for inputDigit in range(inputNumber.pop(0)):
        # inputFile.append(inputNumber[inputDigit:inputDigit+4])
        # inputFile.append(inputNumber[2*inputDigit:2*inputDigit+4])
        inputFile.append(inputNumber[4*inputDigit:4*inputDigit+4])

    # Okay

    # Printing input
    process = DataSummary()
    for i in range(len(inputFile)):
        process.append(Process(*inputFile[i], i))

    print("The original input was:", process.printAllInput())
    process.firstArrivedSort()
    print("The (sorted) input is:", process.printAllInput(), "\n")

    if helper.verbose == True:
        print("This detailed printout gives the state and remaining burst for each process\n")

    FCFS().run(copy.deepcopy(process))
    RR().run(copy.deepcopy(process), currQuantum=2)
    SJF().run(copy.deepcopy(process))
    HPRN().run(copy.deepcopy(process))

    # Okay


if __name__ == '__main__':
    ### Resource: https://stackabuse.com/command-line-arguments-in-python/ 
    if len(sys.argv) == 1:
        sys.argv.append("--verbose")
    # Global Variables
    helper.variables()
    if "--verbose" in sys.argv:
        helper.verbose = True
    main()
