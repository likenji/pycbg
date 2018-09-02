# -*- coding: utf-8 -*-
"""
Created on Mon Jul  9 01:37:45 2018

@author: 51667
"""

qzMoneyCnsmpt = [0 for i in range(41)]

qzMoneyCnsmpt[1] = 43
for i in range(1,40):
    qzMoneyCnsmpt[i + 1] = qzMoneyCnsmpt[i] + i + 5.5
    
qzCumMoneyCnsmpt = [0 for i in range(41)]
for i in range(40):
    qzCumMoneyCnsmpt[i + 1] = qzCumMoneyCnsmpt[i] + qzMoneyCnsmpt[i + 1]
    
qzCumExpCnspmt = [4*n for n in qzCumMoneyCnsmpt]