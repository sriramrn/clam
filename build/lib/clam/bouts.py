import numpy as np
import scipy.integrate


#Detect indices of bout start and ends
#Disregards bouts that might be cut off at the beginning and end of trials
def bout_detect(data,min_thresh=0.05,max_thresh=0.15,min_spacing=7):


    start=np.array([0])
    end=np.array([0])
    toggle=0

    for i in np.arange(2,len(data)-min_spacing,1):

        if data[i]<min_thresh and data[i+1]>=min_thresh:
            if toggle==0:
                start=np.append(start,[i])
                toggle=1

        if data[i]>=min_thresh and all([values<min_thresh for values in data[i+1:i+min_spacing]]):
            if toggle==1:
                end=np.append(end,[i+1])
                toggle=0

    s=np.array([0])
    e=np.array([0])

    if len(start)>1 and len(end)>1:
        start=start[1::]
        end=end[1::]

        if len(start)>len(end):
            end=end[0::]
            start=start[0:len(end)]

        if len(start)<len(end):
            end=end[1::]
            start=start[0::]

        if start[0]==0:
            start=start[1::]
            end=end[1::]

        if max(end)==len(data)-min_spacing:
            end=end[0:len(end)-1]
            start=start[0:len(start)-1]

        thresh=max_thresh
        i=0
        while i<len(start):
            if max(data[start[i]:end[i]])>thresh:
                s=np.append(s,start[i])
                e=np.append(e,end[i])
            i+=1

        s=s[1::]
        e=e[1::]

    return(s,e)


def bout_duration(bout_index,timestamp):

    start_index=np.array(bout_index[0])
    end_index=np.array(bout_index[1])

    duration=[]
    i=0
    while i<len(start_index):
        if end_index[i]-start_index[i]!=0:
            duration.append(timestamp[end_index[i]]-timestamp[start_index[i]])
        i+=1

    return duration


def mean_bout_velocity(data,bout_index,timestamp,bout_duration):

    start_index=np.array(bout_index[0])
    end_index=np.array(bout_index[1])

    strength=[]
    i=0
    while i<len(start_index):
        if end_index[i]-start_index[i]!=0:
            x=timestamp[start_index[i]:end_index[i]]
            y=data[start_index[i]:end_index[i]]
            auc=scipy.integrate.simps(y,x=x,even='avg')
            strength.append(auc/bout_duration[i])
        i+=1

    return strength


def inter_bout_interval(bout_index,timestamp):

    start_index=np.array(bout_index[0])
    end_index=np.array(bout_index[1])

    IBI=[]
    i=0
    while i<len(start_index)-1:
        if end_index[i]-start_index[i]!=0:
            IBI.append(timestamp[start_index[i+1]]-timestamp[end_index[i]])
        i+=1

    return IBI


def max_bout_velocity(data,bout_index):

    start_index=np.array(bout_index[0])
    end_index=np.array(bout_index[1])

    max_vel=[]
    i=0
    while i<len(start_index):
        max_vel.append(max(data[start_index[i]:end_index[i]]))
        i+=1

    return max_vel


def bout_displacement(bout_duration,mean_bout_velocity):

    disp=[]
    i=0
    while i<len(bout_duration):
        disp.append(mean_bout_velocity[i]*bout_duration[i])
        i+=1

    return disp
