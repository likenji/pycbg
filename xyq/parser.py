# -*- coding: utf-8 -*-
"""
Created on Thu Jul 19 20:55:11 2018

@author: 51667
"""
from pycbg.xyq.object.xyqObject import *
from icecream import ic
import json
#import pycbg.xyq.skillMap import *
role_map = {
	"usernum":"ID",
	"cName":"name",
	"iGrade":"level",
	"AllEquip":"equip_list",
	"AllRider":"riding_list",
	"AllSummon":"pet_list",
	"ExAvt":"clothes_list",
	"HugeHorse":"rmb_riding_list",
	"TA_iAllNewPoint":"qianYuanDan",
	"addPoint":"addPoint",
	"all_skills":"skill_dict",
	"changesch":"prev_school_list",
	"child":"child",
	"datang_feat":"datang_feat",
	"iCash":"cash",
	"iLearnCash":"learnCash",
	"iCor_All":"HP_P",
	"iMag_All":"MP_P",
	"iStr_All":"AD_P",
	"iSpe_All":"SPD_P",
	"iNutsNum":"qianNengGuo",
	"iOrgOffer":"orgCtrb",
	"iSchOffer":"schCtrb",
	"iPcktPage":"pkgExt",
	"iSchool":"school",
	"iSaving":"saving",
}
role_identical = [
	""
]
attr_map={
	"等级":"level",
	"命中":"accurateP",
	"伤害":"DMG",
	"气血":"HP",
	"魔法":"MP",
	"防御":"DEF",
	"灵力":"AP",
	"速度":"SPD",
	"命中率":"bingoRate",
	"体质":"HP_P",
	"魔力":"MP_P",
	"法力":"MP_P",
	"力量":"AD_P",
	"耐力":"DEF_P",
	"敏捷":"SPD_P",
	"耐久度":"durance",
	"修理失败":"failure",
	"锻炼等级":"gemLevel",
	"镶嵌宝石":"gemType",
	"镶嵌等级":"gemLevel",
	"精炼等级":"gemLevel",
	"特技":"ultimateSkill",
	"特效":"specialEffect",
	"套装效果":"suitSkill",
	"开运孔数":"hole",
	"符石组合":"totemCombo",
	"熔炼效果":"meltDict",
	"制造者":"creator",
};

gem_map = {
	"黑宝石":"速度",
	"红玛瑙":"命中",
	"太阳石":"伤害",
	"月亮石":"防御",
	"舍利子":"灵力",
	"光芒石":"气血",
	"翡翠石":"法防",
	"神秘石":"躲避",
	"红宝石":"火吸",
	"绿宝石":"雷吸",
	"黄宝石":"土吸",
	"蓝宝石":"水吸",
};
gem_number = {
	"黑宝石": 8,
	"红玛瑙": 25,
	"太阳石": 8,
	"月亮石": 12,
	"舍利子": 6,
	"光芒石": 40,
	"翡翠石": 12,
	"神秘石": 20,
	"红宝石": 4,
	"绿宝石": 4,
	"黄宝石": 4,
	"蓝宝石": 4,
}
class Parser(object):
	def desc_proprocess(self, desc_raw):
		desc = (desc_raw.replace("([","{")).replace("])","}")
		desc = (desc.replace("({","[")).replace("})","]")
		desc = (desc.replace(",]","]")).replace(",}","}")
		return desc

	def get_skill_name(self, skillNo):
		No_str = str(skillNo)
		if 1 <= skillNo <= 132:
			return skill_map["school_skill"][No_str]["name"]
		elif 151 <= skillNo <= 161:
			return skill_map["ju_qing_skill"][skillNo]
		elif 201 <= skillNo <= 237:
			return skill_map["life_skill"][skillNo]
		else:
			print(skillNo)
			raise("skillNo out of range")

	def remove_sharp_marker(self, desc):
		styleStart = "#"
		length = len(desc)
		i = 0
		new_desc = ""
		while(i < length):
			if desc[i] == styleStart:
				i += 1
				if i == length:
					break
				elif desc[i] == "c":
					i += 7
				else:
					i += 1
			else:
				new_desc += desc[i]
				i += 1
		return new_desc

	def remove_last_space(self, dict_desc):
		i = -1
		while(1):
			if dict_desc[i] != " ":
				break
			i -= 1
		return dict_desc[:i]

	def parse_role(self, role_desc):
		role = Role()
		if type(role_desc) != dict:			
			desc = self.desc_proprocess(role_desc)
			role_dict = eval(desc)
		else:
			role_dict = role_desc
		role.equip_list = [self.parse_equipment2(equip_dict) for equip_dict in role_dict["AllEquip"].values()]
		role.pet_list = [self.parse_pet2(pet_dict) for pet_dict in role_dict["AllSummon"]]
		role.riding_list = role_dict["AllRider"].values()
		role.avatar_list = role_dict["ExAvt"].values()
		role.rmb_riding_list = role_dict["HugeHorse"].values()
		role.attrs_option = role_dict["propKept"].values()		

		role.avatar_num = role_dict["total_avatar"]
		role.rmb_riding_num = role_dict["total_horse"]
		role.sanjiegongji = role_dict["datang_feat"]
		role.heroScore = role_dict["HeroScore"]
		role.swordScore = role_dict["sword_score"]
		role.skill_dict = role_dict["all_skills"]

		role.ID = role_dict["usernum"]
		role.level = role_dict["iGrade"]
		role.state = role_dict["iZhuanZhi"]	
		role.huashenglv = role_dict["i3FlyLv"]
		role.name = role_dict["cName"]
		role.school = role_dict["iSchool"]
		role.achvPoint = role_dict["AchPointTotal"]
		role.availExp = role_dict["iUpExp"]
		role.totalExp = role_dict["sum_exp"]

		role.cash = role_dict["iCash"]
		role.saving = role_dict["iSaving"]
		role.learnCash = role_dict["iLearnCash"]
		role.goodness = role_dict["iGoodness"] + role_dict["igoodness_sav"]
		role.xianyu = role_dict["xianyu"]
		role.jingli = role_dict["energy"]
		role.schCtrb = role_dict["iSchOffer"]
		role.orgCtrb = role_dict["iOrgOffer"]
		role.smith = role_dict["iSmithski"]
		role.sew = role_dict["iSewski"]

		role.qianYuanDan = role_dict["TA_iAllNewPoint"]
		role.addPoint = role_dict["addPoint"]
		role.jiYuan = role_dict["jiyuan"]
		role.prev_school_list = role_dict["changesch"]
		role.qianNengGuo = role_dict["iNutsNum"]
		role.pkgExt = role_dict["iPcktPage"]
		role.petExt = role_dict["iSumAmountEx"]	

		role.exptSki1 = role_dict["iExptSki1"]
		role.exptSki2 = role_dict["iExptSki2"]
		role.exptSki3 = role_dict["iExptSki3"]
		role.exptSki4 = role_dict["iExptSki4"]
		role.exptSki5 = role_dict["iExptSki5"]

		role.maxExpt1 = role_dict["iMaxExpt1"]
		role.maxExpt2 = role_dict["iMaxExpt2"]
		role.maxExpt3 = role_dict["iMaxExpt3"]
		role.maxExpt4 = role_dict["iMaxExpt4"]

		role.beastSki1 = role_dict["iBeastSki1"]
		role.beastSki2 = role_dict["iBeastSki2"]
		role.beastSki3 = role_dict["iBeastSki3"]
		role.beastSki4 = role_dict["iBeastSki4"]

		return role
		
	def parse_equipment(self, equip_desc_raw):
		# 解析商品——人物装备		
		desc = self.desc_proprocess(equip_desc_raw)
		desc_list = desc.split("#r")
		length = len(desc_list)
		equip = Equipment()		
		level_info = self.remove_sharp_marker(desc_list[1]).split(" ")
		equip.__dict__[attr_map[level_info[0]]] = int(level_info[1])

		i = 2
		if not self.remove_sharp_marker(desc_list[i]):
			i += 1
		panel_attrs = self.remove_sharp_marker(desc_list[i]).split(" ")
		for j in range(len(panel_attrs)//2):
			equip.__dict__[attr_map[panel_attrs[2*j]]] = int(panel_attrs[2*j + 1])
		i += 1
		
		while(i < length):
			to_parse = self.remove_sharp_marker(desc_list[i])	
			if "耐久度 " in to_parse:
				durance_info = to_parse.split("  ")
				for info in durance_info:
					k1,v1 = info.split(" ") 
					equip.__dict__[attr_map[k1]] = int(v1[-2]) if "次" in v1 else int(v1)
				i += 1
			elif "锻炼等级 " in to_parse:
				gem_info = to_parse.split("  ")
				k1, v1 = gem_info[0].split(" ")
				equip.__dict__[attr_map[k1]] = int(v1)
				gem_type = gem_info[1].replace("、", "").split(" ")
				equip.__dict__[attr_map[gem_type[0]]] = gem_type[1:]
				i += 1
			elif "特技：" in to_parse:
				k1, v1 = to_parse.split("：")
				equip.__dict__[attr_map[k1]] = v1
				i += 1
			elif "特效：" in to_parse:
				k1, v1 = to_parse.split("：")
				equip.__dict__[attr_map[k1]] = v1.split(" ")
				i += 1
			elif "套装效果：" in to_parse:
				k1, v1 = to_parse.split("：")
				equip.__dict__[attr_map[k1]] = v1
				i += 1
			elif "开运孔数：" in to_parse:		
				k1, v1 = to_parse.split("：")
				equip.__dict__[attr_map[k1]] = int(v1[0])
				i += 1
			elif not to_parse or "符石:" in to_parse or "星位:" in to_parse or "星相互合:" in to_parse:
				i +=1
			elif "符石组合: " in to_parse:			   
				k1, v1 = to_parse.split(": ")
				equip.__dict__[attr_map[k1]] = v1
				i += 3
			elif "制造者：" in to_parse:					 
				k1, v1 = to_parse.split("：")
				equip.__dict__[attr_map[k1]] = v1
				i += 1
			elif "熔炼效果：" in to_parse:
				i += 2
				to_parse = self.remove_sharp_marker(desc_list[i])
				melt_info = to_parse.split("  ")
				for info in melt_info[:-1]:
					equip.meltDict[info[-2:]] = int(info[:-2]) 
			else:
				i += 1
		return equip

	def parse_equipment2(self, equip_dict):
		# 解析人物商品中的equip_list项
		equip_desc_raw = self.remove_last_space(equip_dict["cDesc"])
		typeID = equip_dict.get("iType", 0)
		if 27000<= typeID <=28000:
			equip = self.parse_lingShi(equip_desc_raw)
		elif 9000<= typeID <=10000:
			equip = self.parse_equipment_pet(equip_desc_raw)
		elif 1000<=typeID<3000 or 31000<typeID<31399:
			"""
			aaabb
			1000-3000 & 31000-31300	(311..为空)
				aaa=类型
				10=剑
				11=刀
				12=锤
				13=爪
				14=斧钺
				15=扇
				16=枪
				17=鞭子
				18=棒子
				19=飘带
				20=双环
				21=双剑
				22=法杖
				23=宝珠
				24=弓箭
				25=头
				26=衣
				27=鞋
				28=项链
				29=腰带
				310=重剑
				312=灯
				313=伞
				bb=等级&大光&类型
				武器：
					bb<=9, 10*(bb-1)=等级
					50<=bb<60, 小光
					60<=bb<70, 大光
					bb=70, 150
					bb=80, 160
				头衣：
					bb<=9, 男 10*(bb-1)=等级
					10<=bb<=18, 女 10*(bb-10)=等级
					50<=bb<=58, 男 10*(bb-42)=等级
					60<=bb<=68, 女 10*(bb-52)=等级
				其他防具：
					同男性头衣
			"""
			equip = self.parse_equipment(equip_desc_raw)
		else:
			print(typeID)
			equip=Equipment()

		equip.typeID = equip_dict.get("iType", 0)
		equip.lock = equip_dict.get("iLock", 0)
		equip.lockNew = equip_dict.get("iLockNew", 0)
		return equip

	def parse_lingShi(self, lingShi_desc):
		lingShi = LingShi()
		desc_list = lingShi_desc.split("#r")
		length = len(desc_list)		

		i = 0
		while(i < length):
			to_parse = self.remove_sharp_marker(desc_list[i])
			if not to_parse:
				i += 1
			elif i <= 1 and "等级 " == to_parse.split(" ")[0]:
				lingShi.level = int(to_parse.split(" ")[1])
				i += 1
				if not to_parse:					
					i += 1
					to_parse = self.remove_sharp_marker(desc_list[i])
					attr, num = to_parse.split(" ")
					lingShi.attrs_list.append([attr, int(num)])
					i += 1
			elif i <= 4 and "耐久度" in to_parse:
				durance_info = to_parse.split("  ")
				for info in durance_info:
					k1, v1 = info.split(" ")
					lingShi.__dict__[attr_map[k1]] = int(v1[-2]) if "次" in v1 else int(v1)
				i += 1
			elif "精炼等级 " in to_parse:
				k1, v1 = to_parse.split(" ")
				lingShi.__dict__[attr_map[k1]] = int(v1)
				i += 1
			elif "特效：" in to_parse:
				k1, v1 = to_parse.split(" ")
				lingShi.__dict__[attr_map[k1]] = int(v1)
				i += 1
			elif "制造者：" in to_parse:
				i += 1
			else:
				attr, num = to_parse.split(" ")[:2]
				lingShi.attrs_list.append([attr, int(num)])
				i += 1
		return lingShi

	def parse_pet(self, pet_desc_raw):
		# 解析商品召唤兽
		pet=Pet()
		desc = self.desc_proprocess(pet_desc_raw)
		desc_list = desc.split(";")

		pet.typeName = desc_list[0]
		pet.typeID = desc_list[1]
		pet.level = int(desc_list[2])

		pet.AD = int(desc_list[5])
		pet.DEF = int(desc_list[6])
		pet.SPD = int(desc_list[7])

		pet.HP_P = int(desc_list[9])
		pet.MP_P = int(desc_list[10])
		pet.AD_P = int(desc_list[11])
		pet.DEF_P = int(desc_list[12])
		pet.SPD_P = int(desc_list[13])
		pet.unallocated_P = int(desc_list[14])
		pet.AP = int(desc_list[15])
		pet.HP_max = int(desc_list[16])
		pet.MP_max = int(desc_list[17])
		pet.DRNC = int(desc_list[18])

		pet.AD_APTTD = int(desc_list[20])
		pet.DEF_APTTD = int(desc_list[21])
		pet.HP_APTTD = int(desc_list[22])
		pet.MP_APTTD = int(desc_list[23])
		pet.SPD_APTTD = int(desc_list[24])
		pet.MS_APTTD = int(desc_list[25])
		pet.raw_growth = int(desc_list[26])
		pet.growth = pet.raw_growth/1000

		pet.skillList = desc_list[27].split("|")
		pet.APSkill = desc_list[28]
		pet.is_baobao = int(desc_list[29])

		pet.used_yuanxiao = int(desc_list[30])
		pet.used_ruyidan = int(desc_list[31])
		pet.used_qianjinlu = int(desc_list[32])
		pet.used_lianshou = int(desc_list[33])

		json_str = self.desc_proprocess(desc_list[-1])
		details=eval(json_str)

		for k, v in details["summon_core"].items():
			pet.coreDict[k] = v[0] 
		pet.summon_color = details.get("summon_color", 0)
		pet.realColor = details.get("iRealColor", 0)

		jinjie_dict = details.get("jinjie", {})
		pet.lingxing = jinjie_dict.get("lx", 0)
		pet.tmp_lingxing = details.get("tmp_lingxing", 0)
		pet.jinjie_cd = details.get("iJjFeedCd", 0)
		pet.left_qlxl = 7 - jinjie_dict.get("cnt", 0)
		pet.used_shuijinggao = details.get("sjg", 0)

		coreInfo = jinjie_dict.get("core", {})
		pet.coreName = coreInfo.get("name", "")
		pet.coreID = coreInfo.get("id", 0)
		pet.core_positive = details.get("strengthen", 0)
		pet.core_negative = details.get("weaken", 0)
		pet.core_close = details.get("core_close", 0)

		if details.get("jj_extra_add", 0)!=0:
			pet.jj_HP_P = details["jj_extra_add"]["iCor"]
			pet.jj_MP_P = details["jj_extra_add"]["iMag"]
			pet.jj_AD_P = details["jj_extra_add"]["iStr"]
			pet.jj_DEF_P = details["jj_extra_add"]["iRes"]
			pet.jj_SPD_P = details["jj_extra_add"]["iSpe"]		

		if "summon_equip1" in details:			
			pet.equip1 = self.parse_equipment_pet(details["summon_equip1"]["cDesc"])
			pet.equip1.typeID = details["summon_equip1"]["iType"]
		if "summon_equip2" in details:			
			pet.equip2 = self.parse_equipment_pet(details["summon_equip2"]["cDesc"])
			pet.equip2.typeID = details["summon_equip2"]["iType"]
		if "summon_equip3" in details:			
			pet.equip3 = self.parse_equipment_pet(details["summon_equip3"]["cDesc"])
			pet.equip3.typeID = details["summon_equip3"]["iType"]
		if details.get("summon_equip4_desc", 0):
			pet.equip4 = Equipment_pet()
			pet.equip4.typeID = details["summon_equip4_type"]
			info = details["summon_equip4_desc"]			
			if "失败" in info:
				fail_info, durance_info = info.split("#Y#r")
				pet.equip4.failure = int(fail_info[-2])
			else:
				durance_info = info		
			durance_list = durance_info.split(" ")
			pet.equip4.DRNC = int(durance_list[1])
			pet.equip4.color = 1 if len(durance_list)==3 else None
		return pet

	def parse_pet2(self, pet_dict):
		# 解析人物身上的召唤兽
		pet=Pet()
		pet.lock = pet_dict.get("iLock", 0)
		pet.lockNew = pet_dict.get("lockNew", 0)
		pet.typeID = pet_dict["iType"]   
		pet.level = pet_dict["iGrade"]
		pet.DRNC = pet_dict["life"]

		pet.summon_color = pet_dict.get("summon_color", 0)
		pet.realColor = pet_dict.get("iRealColor", 0)
		
		pet.skillList = list(pet_dict["all_skills"].keys())		
		pet.APSkill = pet_dict["iGenius"]

		pet.AD_APTTD = pet_dict["att"]
		pet.DEF_APTTD = pet_dict["def"]
		pet.raw_growth = pet_dict["grow"]
		pet.growth = pet.raw_growth/1000
		pet.MP_APTTD = pet_dict["mp"]
		pet.HP_APTTD = pet_dict["hp"]
		pet.SPD_APTTD = pet_dict["spe"]
		pet.MS_APTTD = pet_dict["dod"]

		pet.used_yuanxiao = pet_dict["yuanxiao"]
		pet.used_ruyidan = pet_dict["ruyidan"]
		pet.used_qianjinlu = pet_dict["qianjinlu"]
		pet.used_lianshou = pet_dict["lianshou"]		
		pet.used_shuijinggao = pet_dict.get("sjg", 0)

		pet.HP_P = pet_dict["iCor_all"]
		pet.MP_P = pet_dict["iMag_all"]
		pet.AD_P = pet_dict["iStr_all"]
		pet.DEF_P = pet_dict["iRes_all"]
		pet.SPD_P = pet_dict["iSpe_all"]
		pet.unallocated_P = pet_dict["iPoint"]

		for k, v in pet_dict["summon_core"].items():
			pet.coreDict[k] = v[0]
		jinjie_dict = pet_dict.get("jinjie", {})
		pet.lingxing = jinjie_dict.get("lx", 0)
		pet.tmp_lingxing = pet_dict.get("tmp_lingxing", 0)
		pet.jinjie_cd = pet_dict.get("iJjFeedCd", 0)
		pet.left_qlxl = 7 - jinjie_dict.get("cnt", 0)

		coreInfo = jinjie_dict.get("core", {})
		pet.coreName = coreInfo.get("name", "")
		pet.coreID = coreInfo.get("id", 0)

		if pet_dict.get("jj_extra_add", 0)!=0:
			pet.jj_HP_P = pet_dict["jj_extra_add"]["iCor"]
			pet.jj_MP_P = pet_dict["jj_extra_add"]["iMag"]
			pet.jj_AD_P = pet_dict["jj_extra_add"]["iStr"]
			pet.jj_DEF_P = pet_dict["jj_extra_add"]["iRes"]
			pet.jj_SPD_P = pet_dict["jj_extra_add"]["iSpe"]

		if "summon_equip1" in pet_dict:			
			pet.equip1 = self.parse_equipment_pet(pet_dict["summon_equip1"]["cDesc"])
			pet.equip1.typeID = pet_dict["summon_equip1"]["iType"]
			pet.equip1.lock = pet_dict["summon_equip1"].get("iLock", 0)
			pet.equip1.lockNew = pet_dict["summon_equip1"].get("iLockNew", 0)
		if "summon_equip2" in pet_dict:			
			pet.equip2 = self.parse_equipment_pet(pet_dict["summon_equip2"]["cDesc"])
			pet.equip2.typeID = pet_dict["summon_equip2"]["iType"]
			pet.equip2.lock = pet_dict["summon_equip2"].get("iLock", 0)
			pet.equip2.lockNew = pet_dict["summon_equip2"].get("iLockNew", 0)
		if "summon_equip3" in pet_dict:			
			pet.equip3 = self.parse_equipment_pet(pet_dict["summon_equip3"]["cDesc"])
			pet.equip3.typeID = pet_dict["summon_equip3"]["iType"]			
			pet.equip3.lock = pet_dict["summon_equip3"].get("iLock", 0)
			pet.equip3.lockNew = pet_dict["summon_equip3"].get("iLockNew", 0)
		if pet_dict.get("summon_equip4_desc", 0):
			pet.equip4 = Equipment_pet()
			pet.equip4.typeID = pet_dict["summon_equip4_type"]
			info = pet_dict["summon_equip4_desc"]			
			if "失败" in info:
				fail_info, durance_info = info.split("#Y#r")
				pet.equip4.failure = int(fail_info[-2])
			else:
				durance_info = info		
			durance_list = durance_info.split(" ")
			pet.equip4.DRNC = int(durance_list[1])
			pet.equip4.color = 1 if len(durance_list)==3 else None
		return pet

	def parse_child(self, child_dict):
		pass
		#to do 

	def parse_equipment_pet(self, pet_equip_desc):
		equip_pet = Equipment_pet()

		desc_list = pet_equip_desc.split("#r")
		length = len(desc_list)
		i = 1
		k1,v1 = desc_list[i].split(" ")[:2]
		equip_pet.__dict__[attr_map[k1]] = int(v1)
		i += 1

		panel_attrs = desc_list[i].split(" ")
		l = len(panel_attrs)
		for j in range(l//2):
			if panel_attrs[2*j] != "" and panel_attrs[2*j+1] != "":
				equip_pet.__dict__[attr_map[panel_attrs[2*j]]] = int(panel_attrs[2*j+1][:-1]) if "%" in panel_attrs[2*j+1] else int(panel_attrs[2*j+1])
			if "命中率" == panel_attrs[2*j]:
				equip_pet.loc = 1
			elif "速度" == panel_attrs[2*j]:				
				equip_pet.loc = 2
			elif "防御" == panel_attrs[2*j]:
				equip_pet.loc = 3
		i += 1
		while(i < length):	
			to_parse = self.remove_sharp_marker(desc_list[i])
			if i == 3 and "耐久度 " in to_parse:
				durance_info = to_parse.split("  ")
				for info in durance_info:
					k1, v1 = info.split(" ")
					equip_pet.__dict__[attr_map[k1]] = int(v1[-2]) if "次" in v1 else int(v1)
					i += 1
			elif i == 4 and ("+" in to_parse or "-" in to_parse):
				add_attrs = to_parse.split(" ")
				l = len(add_attrs)
				for j in range(l//2):
					if add_attrs[2*j] != "" and add_attrs[2*j+1] != "":
						equip_pet.__dict__[attr_map[add_attrs[2*j]]] = int(add_attrs[2*j+1])
				i += 1
			elif "套装效果：附加状态" in to_parse:
				equip_pet.__dict__[attr_map[to_parse[:4]]] = to_parse[9:]
				i += 1
			elif "制造者：" in to_parse:
				i += 1
			elif "镶嵌等级：" in to_parse:
				type_info, level_info = to_parse.split(" ")[:2]
				equip_pet.gemType = type_info[-2:]
				equip_pet.gemLevel = int(level_info.split("：")[1])
				i += 1
			else:
				i += 1
		return equip_pet
	def parse_equipment_pet_deprecated(self, pet_equip_desc):
		# deprecated	
		equip_pet = Equipment_pet()		
		'''
		desc = self.desc_proprocess(pet_equip_desc)
		desc_dict = json.loads("{"+ desc + "}")
		equip_pet.typeNum = desc_dict["iType"]
		detail = desc_dict["cDesc"]
		'''
		detail = pet_equip_desc
		detail_l0 = detail.split("#Y#r#r")
		if len(detail_l0) == 2:			
			equip_gemInfo = detail_l0[-1].split(" 镶嵌等级：")
			equip_pet.gemType = equip_gemInfo[0][-2:]
			equip_pet.gemLevel = int(equip_gemInfo[1])
		detail_l1 = detail_l0[0].split("#Y#r#W")
		'''
		if len(detail_l >= 2):
			equip_pet.creator = detail_l[1][4:-2]
		'''
		detail_l2 = detail_l1[0].split("#Y#r#c4DBAF4")
		if len(detail_l2) == 2:
			equip_pet.suitSkill= detail_l2[1].split("#c4DBAF4")[1].replace("#Y","")

		detail_l3 = detail_l2[0].split("#r#G#G")

		detail_l4 = detail_l3[0].split("#r")
		equip_pet.level = int(detail_l4[1].split(" ")[1])
		panel_attrs = detail_l4[2].split(" ")
		for i in range(len(panel_attrs)//2):
			if panel_attrs[2*i] == "命中率":
				equip_pet.bingoRate = int(panel_attrs[2*i+1].split("%")[0])
				equip_pet.loc = 1
			elif panel_attrs[2*i] == "伤害":
				equip_pet.DMG = int(panel_attrs[2*i+1])
			elif panel_attrs[2*i] == "气血":
				equip_pet.HP = int(panel_attrs[2*i+1])
			elif panel_attrs[2*i] == "魔法":
				equip_pet.MP = int(panel_attrs[2*i+1])				
			elif panel_attrs[2*i] == "防御":
				equip_pet.DEF = int(panel_attrs[2*i+1])
				equip_pet.loc = 3
			elif panel_attrs[2*i] == "速度":
				equip_pet.SPD = int(panel_attrs[2*i+1])
				equip_pet.loc = 2
		durance_info = detail_l4[3].split(" ")
		equip_pet.DRNC = int(durance_info[1].split("#Y")[0])
		if len(durance_info) == 4:
			equip_pet.failure = int(durance_info[3][:-1])

		if len(detail_l3) == 2:
			attrs = detail_l3[1].split("#Y #G")
			for attr in attrs:
				attr_l = attr.replace("#Y","").split(" ")
				attr_num = attr_l[1].split("#")[0]
				if attr_l[0] == "体质":
					equip_pet.HP_P = int(attr_num)
				elif attr_l[0] == "法力":
					equip_pet.MP_P = int(attr_num)
				elif attr_l[0] == "力量":
					equip_pet.AD_P = int(attr_num)
				elif attr_l[0] == "耐力":
					equip_pet.DEF_P = int(attr_num)					
				elif attr_l[0] == "敏捷":
					equip_pet.SPD_P = int(attr_num)					
				elif attr_l[0] == "灵力":
					equip_pet.AP_P = int(attr_num)
		return equip_pet




