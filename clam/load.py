import glob
import numpy as np


def load_raw_data(path, separator = ',\n'):

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
