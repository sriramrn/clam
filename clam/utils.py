import numpy as np
import sys


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
    
    # nframes = len(raw_traces[0])
    
    triggered_traces = []
    triggered_averages = []
        
    for i in range(len(raw_traces)):

	if np.array(raw_traces).shape[0] > 1:
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


def get_imaging_frames_for_behavior_trigger_times(trigger_times, imaging_timestamp):
    
    loc = []
    for t in trigger_times:
        l = abs(imaging_timestamp - t).argmin()
        loc.append(l)
        
    return loc


