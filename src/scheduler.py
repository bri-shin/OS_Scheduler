"""  
Operating System Lab 2: Scheduling
Task: Simulate scheduling in order to see how the time required depends on the scheduling algorithm and the request patterns

Seung Heon (Brian) Shin
"""

import os
import sys
import copy
import helper
from scheduleAlgo import FCFS, RR, SJF, HPRN
from process import Process, DataSummary

### Helper Function Implementation #####

"""
Process Class - Imitating an individual process with necessary attributes and methods
randomOS Class and Function - generating random number 
Data Summary Class - Implementing sorting functions (by arrival, by ready, by job, and by ratio) and printing results

"""

##### Implementing Scheduling Algorithms: FCFS, RR, SJF, HPRN #####


"""
First Come First Serve (FCFS): "Automatically executes queued requests and processes by the order of their arrival"
(Source: Technopedia)

Round Robin (RR): "Preemptive scheduling algorithm that provides processes a fixed amount of time to run, called quantum"
(Source: Tutorialspoint)

Shortest Job First (SJF): "Scheduling algorithm in which the process with the smallest execution time is selected for execution next"
(Source: Technopedia)

Highest Priority Ratio Next (HPRN): "Scheduling algorithm that decides the order through the calculation of priority ratio"
(Source: Javatpoint)
"""

##### Scheduler Execution #####


# Organizing Input into acceptable format
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
        inputFile.append(inputNumber[inputDigit:inputDigit+4])

    # Okay

    # Printing input
    process = DataSummary()
    for i in range(len(inputFile)):
        process.append(Process(*inputFile[i], i))

    print("The original input was:", process.printAllInput())
    process.firstArrivedSort()
    print("The (sorted) input is:", process.printAllInput(), "\n")

    FCFS().run(copy.deepcopy(process))
    RR().run(copy.deepcopy(process), currQuantum=2)
    SJF().run(copy.deepcopy(process))
    HPRN().run(copy.deepcopy(process))

    # Okay


if __name__ == '__main__':
    helper.variables()
    main()
