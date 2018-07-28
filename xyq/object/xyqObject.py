# -*- coding: utf-8 -*-
"""
Created on Thu Jul  5 23:29:38 2018

@author: 51667
"""

from pycbg.PcConstant import *

class Character(object):
    serverName = None
    name = None
    ID = None
    state = None
    level = None
    figure = None
    org = None
    sch = None
    orgCtrb = None
    schCtrb = None
    goldID = None
    achvPt = None
    ptntlNum = None
    availExp = None
    qianYuanDan = None
    totalExp = None
    mnckZongzi = None
    jiyuan = None
    formerTribe = None
    formerOriginList = []
    shuXingOption = []
    
    #人物修炼
    ADBuffLevel = None
    ADBuffLevelCeiling = None
    ADDeLevel = None
    ADDeLevelCeiling = None
    APBuffLevel = None
    APBuffLevelCeiling = None
    APDeLevel = None
    APDeLevelCeiling = None
    
    #猎术修炼
    HuntBuffLevel = None
    
    #召唤兽修炼
    ADBuffLevel_BB = None
    ADDeLevel_BB = None
    APBuffLevel_BB = None
    APDeLevel_BB = None
    
    #战斗相关技能
    #师门
    schoolSkill1 = None
    schoolSkill2 = None
    schoolSkill3 = None
    schoolSkill4 = None
    schoolSkill5 = None
    schoolSkill6 = None
    schoolSkill7 = None
    
    #战斗辅助技能
    #技能映射    
    qiangShen = None
    mingXiang = None
    qiangZhuang = None
    shenSu = None

class Pet(object):
    '''    
    areaName = None
    areaID = None
    serverName = ""
    serverType = None
    serverID = None

    sellerID = None
    sellerName = ""
    price = None
    accept_bargain = 0
    collect_num = None
    create_time = ""
    front_status = None
    '''

    color = None
    realColor = None    
    #desc项
    typeName = EMPTY_STRING #0
    typeID = EMPTY_STRING #1
    level = EMPTY_INT #2

    #HP = None #3
    #MP = None #4
    AD = EMPTY_INT #5
    DEF = EMPTY_INT #6
    SPD = EMPTY_INT #7

    #LYT = None #8
    HP_P = EMPTY_INT
    MP_P = EMPTY_INT
    AD_P = EMPTY_INT
    DEF_P = EMPTY_INT
    SPD_P = EMPTY_INT
    unallocated_P = EMPTY_INT

    AP = EMPTY_INT
    HP_max = EMPTY_INT
    MP_max = EMPTY_INT
    DRNC = EMPTY_INT

    #wuxing = None
    AD_APTTD = EMPTY_INT
    DEF_APTTD = EMPTY_INT
    HP_APTTD = EMPTY_INT
    MP_APTTD = EMPTY_INT
    SPD_APTTD = EMPTY_INT
    MS_APTTD = EMPTY_INT
    raw_growth = EMPTY_INT
    growth = EMPTY_FLOAT
    
    skillList = []
    APSkill = None
    is_baobao = None				# is it a BaoBao?
    used_yuanxiao = None			# 元宵
    used_shuijinggao = None         # 水晶糕
    used_ruyidan = None			# 如意丹
    used_qianjinlu = None 			# 千金露
    used_lianshou = None 	# 炼兽真经
    coreDict = {}

    lingxing = EMPTY_INT
    tmp_lingxing = EMPTY_INT
    jinjie_cd = EMPTY_INT
    used_qlxl = EMPTY_INT

    coreName = EMPTY_STRING
    coreID = EMPTY_INT
    core_positive = EMPTY_INT 
    core_negative = EMPTY_INT
    core_close = EMPTY_INT

    jj_HP_P = EMPTY_INT
    jj_MP_P = EMPTY_INT
    jj_AD_P = EMPTY_INT
    jj_DEF_P = EMPTY_INT
    jj_SPD_P = EMPTY_INT

    def __init__(self):
        self.skillList = []         # 防止共享列表
        self.coreDict = {}          # 防止共享字典

        self.equip1 = Equipment_pet()
        self.equip2 = Equipment_pet()
        self.equip3 = Equipment_pet()
        self.equip4 = Equipment_pet()


    def quality(self, lingxing = 90):    
        quality_dict = OrderedDict()
        quality_dict["AD_DEF"] = self.AD_APTTD * self.level * 0.001 * (1.9 + self.growth/1000 * 1.3) +\
                                self.DEF_APTTD * self.level * 0.001 * (1.23 + self.growth/1000 * 0.87) / (4/3) +\
                                self.HP_APTTD * self.level * 0.001 / 6 +\
                                self.growth/1000 * (self.level + self.level + self.level + self.level*5 + (50 if not self.is_baobao else 100) + lingxing * 2)        
        quality_dict["AD_HP"] = self.AD_APTTD * self.level * 0.001 * (1.9 + self.growth/1000 * 1.3) +\
                                self.DEF_APTTD * self.level * 0.001 * (1.23 + self.growth/1000 * 0.87) / (6) +\
                                self.HP_APTTD * self.level * 0.001 / 6 +\
                                self.growth/1000 * (self.level + self.level + self.level*5 + (50 if not self.is_baobao else 100) + lingxing * 2 )
        quality_dict["AD"] = self.AD_APTTD * self.level * 0.001 * (1.9 + self.growth/1000 * 1.3) +\
                                self.growth/1000 * (self.level + self.level*5 + (50 if not self.is_baobao else 100) + lingxing * 2)

        return quality_dict


class Equipment(object):
    typeNum = None
    level = None
    bingoRate = None
    accurateP = None
    DMG = None
    HP = None
    MP = None
    DEF = None
    SPD = None
    DRNC = None
    HP_P = None
    MP_P = None
    AD_P = None
    DEF_P = None
    SPD_P = None
    failure = None
    suitSkill = None
    gemType = None
    gemlevel = None
    creator = None

class Equipment_pet(object):
    typeID = None
    color = None
    level = EMPTY_INT
    loc = EMPTY_INT
    DRNC = EMPTY_INT
    failure = EMPTY_INT

    bingoRate = EMPTY_INT
    DMG = EMPTY_INT
    HP = EMPTY_INT
    MP = EMPTY_INT
    DEF = EMPTY_INT
    SPD = EMPTY_INT

    HP_P = EMPTY_INT
    MP_P = EMPTY_INT
    AD_P = EMPTY_INT
    DEF_P = EMPTY_INT
    SPD_P = EMPTY_INT
