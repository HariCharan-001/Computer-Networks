# NAME: Hari Charan Korrapati
# Roll Number: CS20B086
# Course: CS3205 Jan. 2023 semester
# Lab number: 4
# Date of submission: 05-04-2023
# I confirm that the source file is entirely written by me without
# resorting to any dishonest means.
# Website(s) that I used for basic socket programming code are:
# URL(s): 

import sys
import socket
from datetime import datetime
import threading
import time

debug_mode = 0
IP_addr = 'localhost'
port  = 0
pkt_len = 0
pkt_rate = 0
n = 0
WS = 0
max_buf_size = 0

for i in range(1, len(sys.argv)):
    if sys.argv[i] == '-d':
        debug_mode = 1

    elif sys.argv[i] == '-s':
        IP_addr = sys.argv[i+1]
    
    elif sys.argv[i] == '-p':
        port = int(sys.argv[i+1])

    elif sys.argv[i] == '-l':
        pkt_len = int(sys.argv[i+1])
    
    elif sys.argv[i] == '-r':
        pkt_rate = int(sys.argv[i+1])
    
    elif sys.argv[i] == '-n':
        n = int(sys.argv[i+1])

    elif sys.argv[i] == '-w':
        WS = int(sys.argv[i+1])

    elif sys.argv[i] == '-f' or sys.argv[i] == '-b':
        max_buf_size = int(sys.argv[i+1])
    

Tproc = 1/ pkt_rate                 #time to create one packet in seconds
rev_addr = (IP_addr, port)
timeout = 0.1                       #timeout in seconds
avg_RTT = 0
window_begin = 0
window_end = window_begin + WS - 1
tot_trans_succ = 0
last_pkt_gen = -1
total_retrans = 0

buffer = []
pkt_sent_time = {}
no_of_attempts = {}
max_attempts = 0

# thread that generates packets periodically at a rate of pkt_rate packets per second
def packet_gen():
    global last_pkt_gen, window_begin, buffer, no_of_attempts

    while True:
        time.sleep(Tproc)
        if(last_pkt_gen == n-1):
            break
        
        if(len(buffer) < window_begin + max_buf_size):
            pkt = chr((last_pkt_gen+1)%256) + 'A' * (pkt_len-1)
            buffer.append(pkt)
            last_pkt_gen += 1
        
        if(max_attempts > 5):
            return

def transmit_window(window_begin):
    global buffer, max_attempts
    window_end = window_begin + WS - 1

    for i in range(window_begin, min(window_end + 1, len(buffer))):
        pkt = buffer[i]
        seq_no = int(ord(pkt[0]))
        
        pkt_sent_time[seq_no] = time.time()

        if(seq_no not in no_of_attempts):
            no_of_attempts[seq_no] = 0
        no_of_attempts[seq_no] += 1

        max_attempts = max(max_attempts, no_of_attempts[seq_no])
        sender_socket.sendto(pkt.encode(), rev_addr)
    
def transmit_packets():
    global window_begin, window_end, timeout, max_attempts

    while(True):
        if(tot_trans_succ == n or max_attempts > 5):
            return
        
        #check for timeout 
        if(window_begin in pkt_sent_time and time.time() - pkt_sent_time[window_begin] > timeout):
            transmit_window(window_begin)
        
        while(window_end != window_begin + WS - 1):
            if(window_end + 1 >= len(buffer)):
                time.sleep(Tproc)
            
            if(window_end + 1 >= len(buffer)):
                break
                
            pkt = buffer[window_end + 1]
            seq_no = int(ord(pkt[0]))
            pkt_sent_time[seq_no] = time.time()
            no_of_attempts[seq_no] = 1
            sender_socket.sendto(pkt.encode(), rev_addr)
            window_end += 1

def print_details():
    print('PACKET_GEN_RATE', pkt_rate)
    print('PACKET_LENGTH', pkt_len)
    print('Retransmission ratio', total_retrans/tot_trans_succ)
    print('Average RTT:' , avg_RTT*1000, 'ms', '\n')
      
def receive_ack():
    global window_begin, window_end, tot_trans_succ, buffer, avg_RTT, timeout, total_retrans, pkt_sent_time, max\

    while True:
        if(tot_trans_succ == n or max_attempts > 5):
                return
        
        ack = sender_socket.recvfrom(pkt_len + 1)[0]
        ack = int(ack.decode())

        #check valid ACK, if not just drop the ACK
        if(ack < window_begin and ack > window_end):
            continue
        
        for i in range(window_begin, ack + 1):
            tot_trans_succ += 1
            i = i % 256
            
            #calculate RTT in milliseconds
            cur_RTT = (time.time() - pkt_sent_time[i])

            #update the timeout value to 2*avg RTT  
            avg_RTT = (avg_RTT * (tot_trans_succ - 1) + cur_RTT)/ tot_trans_succ
            timeout = 2 * avg_RTT

            if(debug_mode == 1):
                print('Seq #:', i, 'Time generated:', int(pkt_sent_time[i]*1000), ':', int(pkt_sent_time[i]*1e6) % 1000, end = " ")
                print('RTT:', cur_RTT*1000, 'Number of Attempts: ', no_of_attempts[i])
        
            #moving window forward
            total_retrans += no_of_attempts[i]
            window_begin += 1
    
# Creating UDP socket for sender
sender_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

# call the packet generation thread
pkt_gen_thread = threading.Thread(target = packet_gen).start()
time.sleep(1)

# transmit the first window
transmit_window(0)

# call the receive ack thread
recv_thread = threading.Thread(target = receive_ack).start()

# call the packets transmission thread
transmit_thread = threading.Thread(target = transmit_packets).start()

while(True):
    if(total_retrans == n or max_attempts > 5):
        print_details()
        sys.exit(0)