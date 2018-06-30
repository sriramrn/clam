import glob
import numpy as np


def load_raw_data(path, separator = ',\n'):

    """
    load 1D data (eg: timeseries) from all text files in the specified path
    each value in the data vector should be separated by the character specified
    by the 'separator'. This could be a line break ('\n') or something else
    """

    files = glob.glob(path+"*.txt")
    data = [[] for x in range(len(files))]
    fileID = [[] for x in range(len(files))]

    error = False

    for i in range(len(files)):
        f = files[i]
        read = open(f,"r")
        temp = read.read()

        try:
            temp = np.array(temp.split(separator)[:-1], dtype=float)

        except Exception as e:
            if not error:
                print('Error Loading Data:')
                error = True
            print('incorrect separator, ' + str(e))

        if len(temp) == 0:
            if not error:
                print('Error Loading Data:')
                error = True
            print('incorrect separator, no data returned')

        read.close()
        data[i] = temp
        fileID[i] = f.split("/")[-1].split(".txt")[0]

    data_dict = dict(zip(fileID,data))

    return data_dict


def load_group(file_group, separator = ',\n'):

    """load data from multiple sessions as a list of dictionaries"""

    data_dicts = []
    for path in file_group:
        d = load_raw_data(path, separator = separator)
        data_dicts.append(d)
        
    return data_dicts


def paramdict(pathtoparamfile):
    
    """load experiment settings from the saved params.txt file"""
   
    f = open(pathtoparamfile,'r')
    params = f.readlines()
    f.close()
    
    paramlist = []
    entry = []
    for i in range(len(params)):
        if len(params[i])>1:
            paramlist.append(params[i].split(':',1)[0].split('\t',1)[0])
            entry.append(params[i].split(':',1)[1][1::].split('\n',1)[0])
    
    zippedparams = zip(paramlist,entry)
    param_dict = dict(zippedparams)
    
    return param_dict
