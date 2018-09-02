# -*- coding: utf-8 -*-
"""
Created on Wed Jul  4 17:02:13 2018

@author: 51667
"""

from collections import OrderedDict

xiulianExp = [n**2 + n*3 + 11 if n > 0 else 0 for n in range(0,26)] 
#xiulianExp存储的是每级的修炼经验

#xiulianCumExp存储的是每级的累计修炼经验
xiulianCumExp = [0 for i in range(0,26)]
for i in range(0,25):
    xiulianCumExp[i+1] = xiulianCumExp[i] + xiulianExp[i+1]

#计算修炼上限(xiulianLimitCumExp)的价值，考虑到20修可以降5修以提升5上限，每级上限可以视作前5级修   
xiulianLimitExp = {n:xiulianExp[n-5] for n in range(21,26)}
xiulianLimitCumExp=OrderedDict()
xiulianLimitCumExp[20]=0
for n in range(20,25):
    xiulianLimitCumExp[n+1] =  xiulianLimitCumExp[n] + xiulianLimitExp[n+1]


xiulianLimitExp_pet={20:0,21:413.69,22:509.52,23:769.63,
                         24:1276.16,25:2111.25}
xiulianLimitCumExp_pet=OrderedDict()
xiulianLimitCumExp_pet[20]=0
for n in range(20,25):
    xiulianLimitCumExp_pet[n+1] = xiulianLimitCumExp_pet[n] + xiulianLimitExp_pet[n+1]