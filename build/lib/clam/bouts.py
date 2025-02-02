import numpy as np
import math
import scipy.integrate



def bout_detect(data,min_thresh=0.05,max_thresh=0.15,min_spacing=7):
    """
    detect bouts where the input signal crosses a given threshold

    Input :
    data : 1D signal (eg: timeseries)
    min_thresh : minimum value that must be crossed during a bouts
    max_thresh : minimum value that must be attained during a bout at least once
    min_spacing : minimum number of data points that the signal must be less
                  than 'min_thresh' for a bout to end

    Output :
    indices of start and end of each bout

    Incomplete bouts are ignored
    """

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

        for i in range(len(start)):
            if max(data[start[i]:end[i]])>thresh:
                s=np.append(s,start[i])
                e=np.append(e,end[i])

        s=s[1::]
        e=e[1::]

    return(s,e)


def bout_duration(bout_index,timestamp):

    start_index=np.array(bout_index[0])
    end_index=np.array(bout_index[1])

    duration=[]
    for i in range(len(start_index)):
        if end_index[i]-start_index[i]!=0:
            duration.append(timestamp[end_index[i]]-timestamp[start_index[i]])

    return duration


def mean_bout_velocity(data,bout_index,timestamp,bout_duration):

    start_index=np.array(bout_index[0])
    end_index=np.array(bout_index[1])

    strength=[]
    for i in range(len(start_index)):
        if end_index[i]-start_index[i]!=0:
            x=timestamp[start_index[i]:end_index[i]]
            y=data[start_index[i]:end_index[i]]
            auc=scipy.integrate.simps(y,x=x,even='avg')
            strength.append(auc/bout_duration[i])

    return strength


def inter_bout_interval(bout_index,timestamp):

    start_index=np.array(bout_index[0])
    end_index=np.array(bout_index[1])

    IBI=[]
    for i in range(len(start_index)-1):
        if end_index[i]-start_index[i]!=0:
            IBI.append(timestamp[start_index[i+1]]-timestamp[end_index[i]])

    return IBI


def max_bout_velocity(data,bout_index):

    start_index=np.array(bout_index[0])
    end_index=np.array(bout_index[1])

    max_vel=[]
    for i in range(len(start_index)):
        if len(data[start_index[i]:end_index[i]]) != 0:
            max_vel.append(max(data[start_index[i]:end_index[i]]))

    return max_vel


def bout_displacement(bout_duration,mean_bout_velocity):

    disp=[]
    for i in range(len(bout_duration)):
        disp.append(mean_bout_velocity[i]*bout_duration[i])

    return disp


def bout_acceleration(data, bout_index, numpoints=6):    
    
    bout_start = bout_index[0]
    bout_end = bout_index[1]
    
    acc = []
    for i in range(len(bout_start)):
        
        if numpoints > bout_end[i] - bout_start[i]:
            a = float('nan')
        
        else:
            a = (data[bout_start[i]+numpoints]-data[bout_start[i]]) / numpoints
            
        acc.append(a)
    
    return acc


def swim_latency(bout_start_time, flow_start_time, flow_end_time, trial_duration):
    
    latency = []
    trial_number = []
    lat_fst = []
    for i in range(len(flow_start_time)):
        s = np.where(np.array(bout_start_time) >= flow_start_time[i])[0]
        if len(s) != 0:
            s = s[0]
            if bout_start_time[s] <= flow_end_time[i]:
                latency.append(bout_start_time[s]-flow_start_time[i])
                trial_number.append(math.floor(bout_start_time[s]/trial_duration))
                lat_fst.append(flow_start_time[i])
    
    return latency, trial_number, lat_fst


def motor_free_flow_start_indices(flow_start, flow_end, motor_activity, motor_threshold=0.2):
    
    mf_fs = []

    for i in range(len(flow_start)):
        if max(motor_activity[flow_start[i]:flow_end[i]]) <= motor_threshold:
            mf_fs.append(flow_start[i])
            
    return mf_fs
