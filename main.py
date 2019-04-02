import queue
import random
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

k=6

q=queue.Queue(k)
q2=queue.Queue(k)


count=0
count1=0
q1_processed=0
count2_1=0
q2_processed=0
t_record1=0
t_record2=0
t_record2_2=0
rate_l=8
rate_m=5
c=0
prob_1=0.5
pkt_delay1=[]
pkt_delay2=[]
flag1=False
flag2=False
timecount1=0
timecount2=0


while(count<5000):
    ##print(q.qsize())
    ##print(count)
    count+=1
    t=random.expovariate(rate_l)
    t_record1+=t
    while(t_record2<=t_record1 and (not q.empty())):
        if(not flag1):
            t_out=random.expovariate(rate_m)
            t_record2+=t_out
        if(t_record2<t_record1):
            ##print(q.get(), "out1",q.qsize(), " " ,t_record1," ",t_record2)
            q.get()
            pkt_delay1[q1_processed]=t_record2-pkt_delay1[q1_processed]
            if(q1_processed==500):
                timecount1=t_record2
            q.task_done()
            q1_processed+=1
            flag1=False
        else:
            flag1=True
            break
    while(t_record2_2<=t_record1 and (not q2.empty())):
        if(not flag2):
            t_out=random.expovariate(rate_m)
            t_record2_2+=t_out
        if(t_record2_2<t_record1):
            ##print(q2.get(), "out2",q2.qsize(), " " ,t_record1," ",t_record2_2)
            q2.get()
            pkt_delay2[q2_processed]=t_record2_2-pkt_delay2[q2_processed]
            if(q2_processed==500):
                timecount2=t_record2_2
            q2.task_done()
            q2_processed+=1
            flag2=False
        else:
            flag2=True
            break
    if(q.empty()):
        t_record2=t_record1
    if(q2.empty()):
        t_record2_2=t_record1
    ##print(t_record1, t_record2)
    if(random.random()<prob_1):
        ##print(count,"1")
        count1+=1
        if(not q.full()):
            q.put(count)
            ##print(count, "in1",q.qsize(), " " ,t_record1)
            if(count>1000):
                c+=1
            pkt_delay1=pkt_delay1+[t_record1]
    else:
        count2_1+=1
        if(not q2.full()):
            q2.put(count)
            if(count>1000):
                c+=1
            pkt_delay2=pkt_delay2+[t_record1]
print("Total packets:",count, "packets going to q1:",count1,"q1 processed packets",q1_processed,"packets going to q2",count2_1,"q2 processed packets",q2_processed,c)
print("system blocking prob:", 1-(q1_processed+q2_processed)/(count-q.qsize()-q2.qsize()))
print("queue 1 blocking prob:",1-(q1_processed/(count1-q.qsize())))
print("queue 2 blocking prob:",1-(q2_processed/(count2_1-q2.qsize())))
print("average delay for queue1:",sum(pkt_delay1[500:])/(len(pkt_delay1)-500))
print("average delay for queue2:",sum(pkt_delay2[500:])/(len(pkt_delay2)-500))
print("average packet number in the system:")
print(sum(pkt_delay1[500:])/(t_record1-timecount1))
print(sum(pkt_delay2[500:])/(t_record1-timecount2))
plt.plot(pkt_delay1[:-10],'-')
