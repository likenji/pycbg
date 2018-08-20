# -*- coding: utf-8 -*-
"""
Created on Thu Jul  5 23:29:38 2018

@author: 51667
"""

from pycbg.PcConstant import *
from pycbg.xyq.exptCnsmpt import *
from pycbg.xyq.qzssCnsmpt import *
from pycbg.xyq.schoolSkillCnsmpt import *
import numpy as np

class Commodity(object):	
	serverID = EMPTY_STRING
	ordersn = EMPTY_STRING

	is_independent = 1
	lock = EMPTY_INT
	lockNew = EMPTY_INT

	price = EMPTY_INT
	accept_bargain = EMPTY_INT
	in_fair_show = EMPTY_INT
	time_left = EMPTY_STRING

	def gen_params(self):
		if is_independent == 0:
			raise("not a commodity")
		else:
			return (
				('act', 'overall_search_show_detail'),
				('serverid', serverID),
				('ordersn', ordersn),
			)

class Role(Commodity):
	name = EMPTY_STRING		# 昵称
	ID = EMPTY_STRING		# ID
	goldID = EMPTY_INT		# 金色ID

	level = EMPTY_INT		# 等级
	state = EMPTY_INT		# 未飞升0，飞升1，渡劫2
	huashenglv = EMPTY_INT	# 化圣层数
	figure = EMPTY_STRING	# 外形
	school = EMPTY_STRING	# 门派
	qianYuanDan = EMPTY_INT # 乾元丹
	addPoint = EMPTY_INT	# 月饼粽子
	jiYuan = EMPTY_INT		# 机缘
	qianNengGuo = EMPTY_INT # 潜能果

	avatar_num = EMPTY_INT	# 锦衣数
	rmb_riding_num = EMPTY_INT 	# 祥瑞数

	sanjiegongji = EMPTY_INT	#三界功绩
	heroScore = EMPTY_INT	# 英雄大会
	swordScore = EMPTY_INT	# 剑会积分

	pkgExt = EMPTY_INT		# 行囊拓展
	petExt = EMPTY_INT		# 召唤兽格子拓展

	cash = EMPTY_INT		# 现金
	saving = EMPTY_INT		# 存款
	learnCash = EMPTY_INT	# 储备金
	goodness = EMPTY_INT	# 善恶点
	xianyu = EMPTY_INT		# 仙玉
	jingli = EMPTY_INT		# 精力
	orgCtrb = EMPTY_INT		# 帮派贡献度
	schCtrb = EMPTY_INT		# 门派贡献度

	achvPoint = EMPTY_INT	# 成就点
	availExp = EMPTY_INT	# 可用经验
	totalExp = EMPTY_INT	# 总经验

	#属性点
	HP_P = EMPTY_INT		# 体力
	MP_P = EMPTY_INT		# 魔力
	AD_P = EMPTY_INT		# 力量
	DEF_P = EMPTY_INT		# 耐力
	SPD_P = EMPTY_INT		# 速度
	unallocated_P = EMPTY_INT		# 未分配点数
	
	#人物修炼
	exptSki1 = EMPTY_INT		# 攻击修炼
	exptSki2 = EMPTY_INT		# 防御修炼
	exptSki3 = EMPTY_INT		# 法术修炼
	exptSki4 = EMPTY_INT		# 抗法修炼
	exptSki5 = EMPTY_INT		# 猎术修炼
	
	maxExpt1 = 20				# 攻修上限
	maxExpt2 = 20				# 防御上限
	maxExpt3 = 20				# 法修上限
	maxExpt4 = 20				# 抗法上限

	#召唤兽修炼
	beastSki1 = EMPTY_INT		# 攻击修炼
	beastSki2 = EMPTY_INT		# 防御修炼
	beastSki3 = EMPTY_INT		# 法术修炼
	beastSki4 = EMPTY_INT		# 抗法修炼
	
	#战斗相关技能
	#师门
	def __init__(self):
		super(Commodity, self).__init__()
		self.equip_list = []		# 装备
		self.riding_list = []		# 坐骑
		self.pet_list = []			# 召唤兽
		self.child = []				# 孩子
		self.avatar_list = []		# 锦衣
		self.rmb_riding_list =[]	# 祥瑞
		self.skill_dict = {}		# 技能
		self.prev_school_list = []	# 历史门派
		self.attrs_option = []		# 属性点分配方案
		self.fabao_list = []		# 法宝
		self.shenqi = {}			# 神器

	def nearest_level_ceiling(self):
		if self.level >= 160:
			return 175
		elif self.level >= 130:
			return 159
		elif self.level >= 110:
			return 129
		elif self.level >= 70:
			return 109
		else:
			return 69

	def get_useful_xiulianLimit(self, expLimit):
		return min(max((self.nearest_level_ceiling - 20) // 5, 20), 25)

	def calculate_xiulian_consumption(self):
	# 单位：万两,可使用储备金		
		consumption = 0
		xiulian_list = [self.exptSki1, self.exptSki2, self.exptSki3, self.exptSki4]
		cumExp_list = [xiulianCumExp[level] for level in xiulian_list]
		consumption += np.dot(np.array([3,2,3,2]), np.array(cumExp_list))
		return consumption

	def calculate_xiulian_limit_consumption(self):
	# 单位：万两,可使用储备金		
		consumption = 0
		limit_list = [self.maxExpt1, self.maxExpt2, self.maxExpt3, self.maxExpt4]
		limit_exp = [xiulianLimitCumExp[get_useful_xiulianLimit(level)] for level in limit_list]		
		consumption += np.dot(np.array([3,2,3,2]), np.array(limit_exp))
		return consumption

	def calculate_xiulian_consumptiont_pet(self):
	# 单位：人民币/元，必须使用现金
		consumption = 0
		beastSki_list = [self.beastSki1, self.beastSki2, self.beastSki3, self.beastSki4]
		cumExp_list = [xiulianCumExp[level] for level in beastSki_list]
		consumption += np.dot(np.array([0.354,0.354,0.354,0.354]), np.array(cumExp_list))
		return consumption

	def calculate_xiulian_limit_consumption_pet(self):
	# 单位：万两,可使用储备金		
		beastSki_list = [self.beastSki1, self.beastSki2, self.beastSki3, self.beastSki4]
		return np.sum([xiulianLimitExp_pet[level] for level in beastSki_list])

	def calculate_school_skill_consumption(self):
	# 单位：万两，可使用储备金
		skills = np.array(list(self.skill_dict.keys())).astype(int)
		schoolSkills = (skills[skills<139])
		level_list = [self.skill_dict[str(skill)] for skill in schoolSkills]
		consumption_list = [schoolSkillCumMoneyCnsmpt[level] for level in level_list] 
		return np.sum(consumption_list)

	def calculate_life_skill_consumption(self):
	# 单位：万两，可使用储备金		
		skills = np.array(list(self.skill_dict.keys())).astype(int)
		lifeSkills = (skills[((skills>203) & (skills<230)) | (skills==231)])
		level_list = [self.skill_dict[str(skill)] for skill in lifeSkills]
		consumption_list = [schoolSkillCumMoneyCnsmpt[level] for level in level_list] 
		return np.sum(consumption_list)

	def calculate_life_skill_ctrb_consumption(self):
	# 单位：帮贡		
		skills = np.array(list(self.skill_dict.keys())).astype(int)
		lifeSkills = (skills[((skills>203) & (skills<237)) | (skills==231)])
		level_list = [self.skill_dict[str(skill)] for skill in lifeSkills]
		consumption_list = [0.5*level**2+level for level in level_list] 
		return np.sum(consumption_list)

	def calculate_fight_skill_consumption(self):	
	# 计算强壮神速消耗,单位万两,可使用储备金
		qs_level = self.skill_dict.get("201", 0)
		mx_level = self.skill_dict.get("202", 0)
		aq_level = self.skill_dict.get("203", 0)
		qz_level = self.skill_dict.get("230", 0)
		ss_level = self.skill_dict.get("237", 0)
		return schoolSkillCumMoneyCnsmpt[qs_level] + schoolSkillCumMoneyCnsmpt[mx_level] +\
			 qzCumMoneyCnsmpt[qz_level] + qzCumMoneyCnsmpt[ss_level]

class Pet(Commodity):
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

	summon_color = EMPTY_INT    # 是否染色
	realColor = EMPTY_INT     	# 染色丹的颜色
	#desc项
	typeName = EMPTY_STRING 	# 召唤兽类型名称
	typeID = EMPTY_STRING   	# 召唤兽类型编号
	level = EMPTY_INT   		# 召唤兽等级

	#HP = None   				# 召唤兽当前气血
	#MP = None   				# 召唤兽当前魔法
	AD = EMPTY_INT  			# 召唤兽攻击力
	DEF = EMPTY_INT				# 召唤兽防御
	SPD = EMPTY_INT  			# 召唤兽速度

	#LYT = None  				 召唤兽忠诚度
	HP_P = EMPTY_INT      		# 召唤兽体力点
	MP_P = EMPTY_INT      		# 召唤兽魔力点
	AD_P = EMPTY_INT      		# 召唤兽力量点
	DEF_P = EMPTY_INT   		# 召唤兽耐力点
	SPD_P = EMPTY_INT   		# 召唤兽速度点
	unallocated_P = EMPTY_INT 	#召唤兽未分配潜力点

	AP = EMPTY_INT  			# 召唤兽灵力
	HP_max = EMPTY_INT  		# 召唤兽最大气血
	MP_max = EMPTY_INT  		# 召唤兽最大魔法
	DRNC = EMPTY_INT      		# 召唤兽寿命(durance)

	#wuxing = None
	AD_APTTD = EMPTY_INT     	# 召唤兽攻击资质
	DEF_APTTD = EMPTY_INT    	# 召唤兽防御资质
	HP_APTTD = EMPTY_INT     	# 召唤兽体力资质
	MP_APTTD = EMPTY_INT     	# 召唤兽法力资质
	SPD_APTTD = EMPTY_INT    	# 召唤兽速度资质
	MS_APTTD = EMPTY_INT     	# 召唤兽躲避资质
	raw_growth = EMPTY_INT   	# 爬取得到的成长, 1264
	growth = EMPTY_FLOAT     	# 用于计算的成长, 1.264
	
	skillList = []  			# 技能列表
	APSkill = EMPTY_INT  		# 法术技能
	is_baobao = None      		# 是否是宝宝?
	used_yuanxiao = EMPTY_INT  	# 元宵
	used_shuijinggao = EMPTY_INT   # 水晶糕
	used_ruyidan = EMPTY_INT    # 如意丹
	used_qianjinlu = EMPTY_INT 	# 千金露
	used_lianshou = EMPTY_INT 	# 炼兽真经
	coreDict = {}    			# 召唤兽内丹

	lingxing = EMPTY_INT     	# 召唤兽最高灵性
	tmp_lingxing = EMPTY_INT   	# 召唤兽当前灵性
	jinjie_cd = EMPTY_INT   	# 召唤兽进阶冷却
	used_qlxl = EMPTY_INT   	# 召唤兽使用过的清灵仙露数

	coreName = EMPTY_STRING 	# 召唤兽特性
	coreID = EMPTY_INT  		# 召唤兽特性ID
	core_positive = EMPTY_INT  	# 召唤兽特性正向效果
	core_negative = EMPTY_INT  	# 召唤兽特性负向效果
	core_close = EMPTY_INT   	# 召唤兽特性关闭状态

	jj_HP_P = EMPTY_INT  		# 进阶110增加的体力
	jj_MP_P = EMPTY_INT  		# 进阶110增加的魔力
	jj_AD_P = EMPTY_INT  		# 进阶110增加的力量
	jj_DEF_P = EMPTY_INT     	# 进阶110增加的耐力
	jj_SPD_P = EMPTY_INT     	# 进阶110增加的速度

	def __init__(self):
		super(Commodity, self).__init__()
		self.skillList = []   	# 防止共享列表
		self.coreDict = {}   	# 防止共享字典

		self.equip1 = Equipment_pet()   # 召唤兽1号位装备
		self.equip2 = Equipment_pet()   # 召唤兽2号位装备
		self.equip3 = Equipment_pet()   # 召唤兽3号位装备
		self.equip4 = Equipment_pet()   # 召唤兽饰品


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

class Equipment(Commodity):
	typeID = EMPTY_INT   		# 装备类型编号

	level = EMPTY_INT    		# 装备等级
	loc = EMPTY_INT   			# 装备位置  
	durance = EMPTY_INT 		# 装备耐久   
	failure = EMPTY_INT 		# 装备失败次数

	accuracy = EMPTY_INT      	# 装备总命中   
	DMG = EMPTY_INT 			# 装备总伤
	HP = EMPTY_INT  			# 装备总气血
	MP = EMPTY_INT  			# 装备初魔法
	DEF = EMPTY_INT 			# 装备总防御
	AP = EMPTY_INT  			# 装备总灵 
	HP_P = EMPTY_INT      		# 装备体质
	MP_P = EMPTY_INT      		# 装备魔力
	AD_P = EMPTY_INT      		# 装备力量
	DEF_P = EMPTY_INT    		# 装备耐力
	SPD_P = EMPTY_INT    		# 装备敏捷

	ultimateSkill = EMPTY_STRING   # 特技  
	specialEffect = []  		# 特效
	suitSkill = EMPTY_STRING    # 套装效果

	hole = EMPTY_INT      		# 开孔数
	totemCombo = EMPTY_STRING   # 符石组合

	gemLevel = EMPTY_INT      	# 镶嵌情况
	gemType = []     
	meltDict = {}    			# 熔炼情况

	creator = EMPTY_STRING   	# 打造者

	def __init__(self):
		super(Commodity, self).__init__()
		self.gemType = []   	# 防止实例列表
		self.specialEffect = [] # 防止共享列表
		self.meltDict = {}   	# 同上

class Equipment_pet(Commodity):
	typeID = EMPTY_INT   		# 装备类型编号
	color = EMPTY_INT    		# 装备颜色（饰品专用）

	level = EMPTY_INT    		# 装备等级
	loc = EMPTY_INT   			# 装备位置
	durance = EMPTY_INT 		# 装备耐久
	failure = EMPTY_INT 		# 装备失败次数

	gemType = EMPTY_STRING   	# 镶嵌类型
	gemLevel = EMPTY_INT     	# 镶嵌等级

	bingoRate = EMPTY_INT   	# 命中率
	DMG = EMPTY_INT   			# 初伤害
	HP = EMPTY_INT  			# 初气血
	MP = EMPTY_INT  			# 初魔法
	DEF = EMPTY_INT   			# 初防御
	SPD = EMPTY_INT   			# 初速度

	HP_P = EMPTY_INT      		# 体力
	MP_P = EMPTY_INT      		# 魔力
	AD_P = EMPTY_INT     		# 力量
	DEF_P = EMPTY_INT    		# 耐力
	SPD_P = EMPTY_INT    		# 速度
	AP = EMPTY_INT  			# 灵力

	def __init__(self):
		super(Commodity, self).__init__()

class LingShi(Commodity):
	typeID = EMPTY_INT
	level = EMPTY_INT
	specialEffect = EMPTY_INT	# 超级简易否？

	durance = EMPTY_INT 		# 装备耐久
	failure = EMPTY_INT 		# 装备失败次数
	gemLevel = EMPTY_INT		# 精练等级

	def __init__(self):
		super(Commodity, self).__init__()
		self.attrs_list = [] 	# 属性列表，包括黄字和绿字

