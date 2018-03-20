# -*- coding: utf-8 -*-
"""
Created on Mon Jan  8 14:28:34 2018

@author: Sriram Narayanan
"""

import glob

def paramdict(pathtoparamfile):
   
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

    
expName = 'BoutClamp'
expParamFile = 'D:/ClosedLoopRaw/BCParams.txt' 
savePath = 'D:/ClosedLoopRaw/'
expParam = paramdict(expParamFile)

dataPath = 'D:/ClosedLoopRaw/'
paramPath = glob.glob(dataPath+'/**/params.txt',recursive=True)

pathList = []

for paramFile in paramPath:
    
    tempParam = paramdict(paramFile)
    accept = True
    
    for key in list(expParam.keys()):
        
        if key in list(tempParam.keys()):
            if tempParam[key] != expParam[key]:
                accept = False
        else:
            accept = False
            
    if accept:
        pathList.append(paramFile.split('params.txt')[0])

file = open(savePath+expName+'_DataPath.txt','w+')
for p in pathList:
    file.writelines(p+'\n')
file.close()        