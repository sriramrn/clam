import numpy as np
import sys
import math


def peakdet(v, delta, x = None):
    """
    https://gist.github.com/endolith/250860#file-peakdetect-py-L11

    Converted from MATLAB script at http://billauer.co.il/peakdet.html

    Returns two arrays

    function [maxtab, mintab]=peakdet(v, delta, x)
    %PEAKDET Detect peaks in a vector
    %        [MAXTAB, MINTAB] = PEAKDET(V, DELTA) finds the local
    %        maxima and minima ("peaks") in the vector V.
    %        MAXTAB and MINTAB consists of two columns. Column 1
    %        contains indices in V, and column 2 the found values.
    %
    %        With [MAXTAB, MINTAB] = PEAKDET(V, DELTA, X) the indices
    %        in MAXTAB and MINTAB are replaced with the corresponding
    %        X-values.
    %
    %        A point is considered a maximum peak if it has the maximal
    %        value, and was preceded (to the left) by a value lower by
    %        DELTA.

    % Eli Billauer, 3.4.05 (Explicitly not copyrighted).
    % This function is released to the public domain; Any use is allowed.

    """
    maxtab = []
    mintab = []

    if x is None:
        x = np.arange(len(v))

    v = np.asarray(v)

    if len(v) != len(x):
        sys.exit('Input vectors v and x must have same length')

    if not np.isscalar(delta):
        sys.exit('Input argument delta must be a scalar')

    if delta <= 0:
        sys.exit('Input argument delta must be positive')

    mn, mx = np.Inf, -np.Inf
    mnpos, mxpos = np.NaN, np.NaN

    lookformax = True

    for i in np.arange(len(v)):
        this = v[i]
        if this > mx:
            mx = this
            mxpos = x[i]
        if this < mn:
            mn = this
            mnpos = x[i]

        if lookformax:
            if this < mx-delta:
                maxtab.append((mxpos, mx))
                mn = this
                mnpos = x[i]
                lookformax = False
        else:
            if this > mn+delta:
                mintab.append((mnpos, mn))
                mx = this
                mxpos = x[i]
                lookformax = True

    return np.array(maxtab), np.array(mintab)


def filter_peaks_by_spacing(peaks, minspacing):
    """
    pick the largest peak if there is a cluster of peaks
    peaks : numpy array of the form (index,peak_value)
    minspacing : minimum interval between peaks
    """
    peakindex = peaks[:,0]
    peakvalue = peaks[:,1]

    npeaks = len(peakindex)

    iterations = int(npeaks/2)+1

    for ii in range(iterations):

        filtered_peakindex = []
        filtered_peakvalue = []

        skip = False

        for i in range(npeaks-1):

            if skip == False:

                if peakindex[i+1]-peakindex[i] >= minspacing:
                    filtered_peakindex.append(peakindex[i])
                    filtered_peakvalue.append(peakvalue[i])
                    if i==npeaks-2:
                        filtered_peakindex.append(peakindex[i+1])
                        filtered_peakvalue.append(peakvalue[i+1])
                else:
                    skip = True
                    temp_peaks = np.array([peakvalue[i],peakvalue[i+1]])
                    thisornext = np.where(temp_peaks == max(temp_peaks))[0][0]
                    filtered_peakindex.append(peakindex[i+thisornext])
                    filtered_peakvalue.append(peakvalue[i+thisornext])
            else:
                skip = False

        peakindex = filtered_peakindex
        peakvalue = filtered_peakvalue
        npeaks = len(peakindex)

    filtered_peaks = np.transpose(np.vstack((filtered_peakindex,filtered_peakvalue)))

    return filtered_peaks


def smoothen(data,window):
    """sliding window average of input signal"""
    w = np.ones(window)/window
    return np.convolve(data,w,'same')


def rolling_avg(data,w):
    
    w = w + np.remainder(w,2)
    hw = int(w/2)
    
    avg = []
    for i in range(len(data)):
    
        if i < hw:
            a = np.mean(data[0:w])
            
        if i > hw and len(data)-i > hw:
            a = np.mean(data[i-hw:i+hw])
            
        if i > hw and len(data)-i < hw:
            a = np.mean(data[-w::])
            
        avg.append(a)
    
    return avg


def local_stdv(data,window):

    """
    Standard deviation of a sliding window across 1D data
    Function adapted from:
    http://matlabtricks.com/post-20/calculate-standard-deviation-case-of-sliding-window
    """
    data = np.array(data)
    W = window
    N = len(data)
    n = np.convolve(np.ones(N), np.ones(W), 'same')
    s = np.convolve(data, np.ones(W), 'same')
    q = data**2;
    q = np.convolve(q, np.ones(W), 'same')
    o = (q-s**2/n)/(n-1);
    o = o**0.5

    return o


def ttl_edges(digital_signal, logic_level, begin_low = True, end_low = True):
    """logic_level should be 1 or 5"""

    if logic_level == 1:
        digital_signal = digital_signal*5

    if end_low:
        if digital_signal[-1] >= 1:
            digital_signal[-1] = 0
            
    if begin_low:
        if digital_signal[0] >= 1:
            digital_signal[0] = 0
    
    all_edges = np.diff(digital_signal).astype(int)

    rising_edges = np.where(all_edges >= 1)[0]
    falling_edges = np.where(all_edges <= -1)[0]
    
    
    return rising_edges, falling_edges


def triggered_response(raw_traces, trig_indices, trig_range, nframes):
            
    ntraces = 1
    if len(np.array(raw_traces).shape) > 1:
        ntraces = np.array(raw_traces).shape[0]  
    
    triggered_traces = []
    triggered_averages = []
        
    for i in range(ntraces):

        if ntraces > 1:
            cell = raw_traces[i]
        else:
            cell = raw_traces

        tt = []
        
        for ti in trig_indices:
        
            if ti+trig_range[0] >= 0 and ti+trig_range[1] <= nframes:
                
                crop = cell[ti+trig_range[0]:ti+trig_range[1]]
                tt.append(crop)

        triggered_traces.append(tt)
        if len(tt) > 0:
            triggered_averages.append(np.mean(tt,0))
        
    return triggered_traces, triggered_averages


def get_trigger_frames_from_trigger_times(trigger_times, imaging_timestamp):
    
    loc = []
    for t in trigger_times:
        l = abs(imaging_timestamp - t).argmin()
        loc.append(l)
        
    return loc


def select_cells_from_triggered_responses(triggered_traces, triggered_averages, cell_indices):
    
    selected_traces, selected_averages = [],[]
    for i in range(len(triggered_averages)):
        if i in cell_indices:
            selected_traces.append(triggered_traces[i])
            selected_averages.append(triggered_averages[i])
    
    return selected_traces, selected_averages



def select_trials_from_triggered_responses(triggered_traces, trial_indices):
    
    # assumes this is a list of lists. If its a numpy array, this may return ntrials instead of ncells
    ncells = len(triggered_traces)
    
    selected_traces, selected_averages = [],[]
    
    for i in range(ncells):
        st = []
        for ii in range(len(triggered_traces[i])):
            if ii in trial_indices:
                st.append(triggered_traces[i][ii])
        
        selected_traces.append(st)
        selected_averages.append(np.mean(st,0))
    
    return selected_traces, selected_averages



def optimal_latency_window(latencies, w = 0.128, step = 0.128, lat_range = [0.512, 2]):
    
    latencies = np.array(latencies)
    
    optimal_latency = 0
    nbouts = 0
    
    steps = math.ceil(np.diff(lat_range)/step)
    
    for i in range(steps):
        
        lat = i*step + lat_range[0]
        
        bouts_within_window = latencies[latencies >= lat-w]
        bouts_within_window = bouts_within_window[bouts_within_window <= lat+w]
    
        if len(bouts_within_window) >= nbouts:
            
            optimal_latency = lat
            nbouts = len(bouts_within_window)
                    
    return optimal_latency, nbouts



def latency_clamped_flow_times(flow_start_time, flow_end_time, bout_start_time,
                               latency_clamp, w = 0.128):
    
    lat_clamp_fs_time = []
    for i in range(len(flow_start_time)):
        s = np.where(np.array(bout_start_time) > flow_start_time[i])[0]
        if len(s) != 0:
            s = s[0]
            s = bout_start_time[s]
            if s < flow_end_time[i]:
                latency = s - flow_start_time[i]
                if abs(latency - latency_clamp) <= w:
                    lat_clamp_fs_time.append(flow_start_time[i])
            
    return lat_clamp_fs_time



def detect_significant_responses(triggered_traces, idx_before, idx_after, span, std_thresh = 1.5):

    responses = []
    response_amplitudes = []
    
    for i in range(len(triggered_traces)):
        
        mean = np.mean(triggered_traces[i][idx_before-span : idx_before+span])
        std = np.std(triggered_traces[i][idx_before-span : idx_before+span])
        
        threshold = mean + std_thresh*std
        
        signal = np.mean(triggered_traces[i][idx_after-span : idx_after+span])
        
        response_amplitudes.append(signal)
        
        if signal > threshold:
            responses.append(1)
        else:
            responses.append(0)
            
            
    response_fraction = np.mean(responses)
    
    mean_response_amplitude = np.mean(response_amplitudes)
    
    return response_fraction, responses, response_amplitudes, mean_response_amplitude
