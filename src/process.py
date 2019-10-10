import helper


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
                self.blockedTime += 1
        # print(self.leftOverCPU)

        # print("Hello Im here")
        return

    # Updating the status of process
    def updateStatus(self):
        currentTimeCounter = helper.currTime.getTimeCount()
        if self.processStatus == 2:                 # Process is running
            if self.leftOverCPU == 0:
                self.processStatus = 4              # process terminated
                self.finishTime = currentTimeCounter
                return
            elif self.currBurst == 0:               # If current burst is used up
                self.processStatus = 3              # process blocked
                self.currBurst = self.M * self.prevBurst
                return
            elif self.quantumCount == 0:            # If quantum is used up
                self.processStatus = 1              # process ready / preempt
                self.initialTime = helper.currTime.getTimeCount()
                return
        elif self.processStatus == 0:               # Process is unstarted
            if currentTimeCounter == self.A:
                self.processStatus = 1
                self.initialTime = helper.currTime.getTimeCount()
                return
        elif self.processStatus == 3:
            if self.currBurst == 0:
                self.processStatus = 1
                self.initialTime = helper.currTime.getTimeCount()
                return
        else:
            pass

        # print("hello")
        return self.processStatus

    # Must create in order to access randomObj as an object
    def randomBurst(self):
        self.prevBurst = helper.randomObj.randomOS(self.B)
        self.currBurst = self.prevBurst

    # Running Process (+ Setting random burst)
    def runProcess(self):
        self.processStatus = 2
        if helper.RRquantum:
            self.quantumCount = helper.RRquantum

        if self.currBurst == 0:
            self.randomBurst
            # self.prevBurst = randomObj.randomOS(self.B)
            # self.currBurst = self.prevBurst

    def firstArrived(self):
        return self.A

    # Printing initial Input
    def printInput(self):
        return "({} {} {} {})".format(self.A, self.B, self.C, self.M)

    # Printing the Result of Burst Status
    def printResult(self):
        printStatus = (' '*10 + self.processStatus)[-10:]
        if not helper.RRquantum:
            burstPrint = self.currBurst
        else:
            burstPrint = self.quantumCount
        printBurst = (' '*3 + str(burstPrint))[-3:]
        return printStatus + printBurst

    # Printing Overall Summary Data
    def printProcessSummary(self):
        print("""	(A,B,C,M) = ({},{},{},{})\n\tFinishing time: {}\n\tTurnaround time: {}\n\tI/O time: {}\n\tWaiting time: {}\n""" .format(
            self.A, self.B, self.C, self.M, self.finishTime, self.turnaroundTime, self.blockedTime, self.waitingTime))

    def getRatio(self):
        T = self.turnaroundTime
        t = max(1, self.runningTime)
        return T/t


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

    def isTerminated(self):
        for element in self:
            if element.processStatus != 4:
                return False
        self.finishTime = helper.currTime.getTimeCount() - 1
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
        cpuUtil = 0
        for process in self:
            cpuUtil += process.runningTime
        cpuUtil = cpuUtil / self.finishTime

        # Calculating IO Utilization
        ioUtil = self.ioUtilization / self.finishTime

        # Calculating Throughput
        throughput = 100*len(self) / self.finishTime

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
        for processID, process in enumerate(self):
            print("Process", int(processID))
            process.printProcessSummary()
        print("Summary Data:")
        print("\t Finishing Time:", self.finishTime)
        print("\t CPU Utilization:", cpuUtil)
        print("\t I/O Utilization:", ioUtil)
        print("\t Throughput:", throughput, "processes per hundred cycle")
        print("\t Average turnaround time:", avgTurnaroundTime)
        print("\t Average waiting time:", avgWaitingTime)

##### End of Helper Function Implementation #####
