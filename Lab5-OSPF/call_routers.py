# NAME: Hari Charan Korrapati
# Roll Number: CS20B086
# Course: CS3205 Jan. 2023 semester
# Lab number: 5
# Date of submission:= 29/04/2023
# I confirm that the source file is entirely written by me without resorting to any dishonest means.
# Website(s) that I used for basic socket programming code are:

import subprocess
import sys
import time

id = 0
infile = 'input.txt'
outfile = 'output'
hello = 1
lsa = 5
spf = 20

for i in range(1, len(sys.argv)):
    if sys.argv[i] == '-i':
        id = int(sys.argv[i+1])
        outfile = 'output-' + str(id) + '.txt'

    elif sys.argv[i] == '-f':
        infile = sys.argv[i+1]
    
    elif sys.argv[i] == '-o':
        outfile = sys.argv[i+1] + '-' + str(id) + '.txt'
    
    elif sys.argv[i] == '-h':
        hello = int(sys.argv[i+1])

    elif sys.argv[i] == '-a':
        lsa = int(sys.argv[i+1])
    
    elif sys.argv[i] == '-s':
        spf = int(sys.argv[i+1])

input_file = open(str(infile), 'r')
N = int(input_file.readline().strip().split()[0])

process_list = []
for i in range(N):
    print('Router', i, 'intiated')
    process=subprocess.Popen(["python3", "Lab5-OSPF.py", "-i",str(i), "-f",infile, "-o",outfile, "-h", str(hello), "-a", str(lsa), "-s",str(spf)])
    process_list.append(process)

start=time.time()
while(1):
    if(time.time()-start>=50):
        for x in process_list:
            x.kill()
        print('Killed')
        break