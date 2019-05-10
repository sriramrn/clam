import numpy as np
import matplotlib.pyplot as plt


def hide_mpl_axis(axis_handle):
    axis_handle.spines['right'].set_visible(False)
    axis_handle.spines['top'].set_visible(False)
    # Only show ticks on the left and bottom spines
    axis_handle.yaxis.set_ticks_position('left')
    axis_handle.xaxis.set_ticks_position('bottom')
    
    
def trig_plot_err(data, tstamp, error = 'stdv', linestyle = '-', color = 'black', linealpha = 1,
                  erralpha = 0.15, linewidth = 2, figsize = [4,4], axdim = [0.15, 0.15, 0.75, 0.75],
                  axis_handle = None, hideaxis = True, label = None ):
    
    ta = np.mean(data, 0)
    
    er_ta = np.std(data, 0)
    
    if error == 'ste':
        er_ta = er_ta/np.sqrt(len(data))
        
    if axis_handle == None:
    
        fig = plt.figure(figsize = figsize)
    
        ax = fig.add_axes(axdim)
        ax.plot(tstamp, ta, color = color, linestyle = linestyle, alpha = linealpha, 
                linewidth = linewidth, label = label)
        ax.fill_between(tstamp, ta+er_ta, ta-er_ta, color = color, alpha = erralpha, linewidth=0)
        
    else:
        
        ax = axis_handle
        
        ax.plot(tstamp, ta, color = color, linestyle = linestyle, alpha = linealpha, 
                linewidth = linewidth, label = label)
        ax.fill_between(tstamp, ta+er_ta, ta-er_ta, color = color, alpha = erralpha, linewidth=0)
    
    if hideaxis:
        hide_mpl_axis(ax)
    
    return ax, ta, er_ta 



def trig_plot_traces(data, tstamp, color = 'black', linealpha = 1, tracealpha = 0.15, linewidth = 2,
                     tracewidth = 1, figsize = [4,4], axdim = [0.15, 0.15, 0.75, 0.75], 
                     axis_handle = None, hideaxis = True, label = None ):
    
    ta = np.mean(data, 0)
        
    if axis_handle == None:
    
        fig = plt.figure(figsize = figsize)
        ax = fig.add_axes(axdim)
        
        for i in range(np.array(data).shape[0]):
            ax.plot(tstamp, data[i], color = color, alpha = tracealpha, linewidth = tracewidth)
            
        
        ax.plot(tstamp, ta, color = color, alpha = linealpha, linewidth = linewidth, label = label)
        
    else:
        
        ax = axis_handle
        
        for i in range(np.array(data).shape[0]):
            ax.plot(tstamp, data[i], color = color, alpha = tracealpha, linewidth = linewidth)        
        
        ax.plot(tstamp, ta, color = color, alpha = linealpha, linewidth = linewidth, label = label)
    
    if hideaxis:
        hide_mpl_axis(ax)
    
    return ax, ta

