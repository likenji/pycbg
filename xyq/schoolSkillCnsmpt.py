# -*- coding: utf-8 -*-
"""
Created on Wed Jul  4 16:12:08 2018

@author: 51667
"""
from collections import OrderedDict
import csv

MONEY_BASED = 10**4
i = 0
schoolSkillExpCnsmpt = [i]
schoolSkillMoneyCnsmpt = [i]

with open("schoolSkillCnsmpt.csv","r",encoding="utf-8") as csvfile:    
    reader = csv.reader(csvfile)
    for d in reader:
        i += 1
        schoolSkillExpCnsmpt.append(int(d[1]) / MONEY_BASED)
        schoolSkillMoneyCnsmpt.append(int(d[2]) / MONEY_BASED)

schoolSkillCumExpCnsmpt = [0 for i in range(181)]
schoolSkillCumMoneyCnsmpt = [0 for i in range(181)]

for n in range(180):
    schoolSkillCumExpCnsmpt[n+1] = schoolSkillCumExpCnsmpt[n] \
                                + schoolSkillExpCnsmpt[n+1]
    schoolSkillCumMoneyCnsmpt[n+1] = schoolSkillCumMoneyCnsmpt[n] \
                                + schoolSkillMoneyCnsmpt[n+1] 
