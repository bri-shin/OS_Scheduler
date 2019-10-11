# OS Scheduler

<i> Operating System 2019 Fall </i>

<i> Author: Seung Heon Brian Shin </i>



## Program Background:
This program simulates scheduling in order to demonstrate how the time required depends on the scheduling algorithm and the request patterns. This scheduling algorithms implemented are:

1. First Come First Serve 
2. Round Robin
3. Shorted Job First
4. Highest Penalty Ratio Next



 Individual process is characterized by:

- A: Arrival time of the process

- B: Upper Bound of CPU burst time

- C: Total CPU time required

- M: Multiplier of CPU burst time



## Program Specifications:

<i> Programming Language Used: </i> Python 3



## How to run this program:

Before running to program, it is important to sync the "random-numbers.txt" file, which is currently located in .../src. Within .../src/helper.py, it is important to set the correct random number text file by:

```python
RandomNumberText = "random-number.txt"
```



On the terminal, this program can be run by:

```terminal
$ python3 OS_Scheduler.py <input-file>
```



Examples of <input-file> would be "input-1.txt"



Moreover, this program provides detailed result that includes the current status and burst of each process. This can be prompted by:

```terminal
$ python3 OS_Scheduler.py --verbose <input-file>
```



