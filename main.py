import queue
import random

k=6

q=queue.Queue(k)
q2=queue.Queue(k)


count=0
count1=0
count2=0
count2_1=0
count2_2=0
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

while(count<11000):
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
            pkt_delay1[count2]=t_record2-pkt_delay1[count2]
            q.task_done()
            count2+=1
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
            q2.task_done()
            count2_2+=1
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
        if(not q.full()):
            q.put(count)
            ##print(count, "in1",q.qsize(), " " ,t_record1)
            count1+=1
            if(count>1000):
                c+=1
            pkt_delay1=pkt_delay1+[t_record1]
    else:
        if(not q2.full()):
            q2.put(count)
            count2_1+=1
            if(count>1000):
                c+=1
print(count,count1,count2,count2_1,count2_2,c)
print(sum(pkt_delay1[500:])/(len(pkt_delay1)-500))

