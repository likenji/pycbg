# -*- coding: utf-8 -*-
"""
Created on Thu Jul 19 20:55:11 2018

@author: 51667
"""
from pycbg.xyq.object.xyqObject import *
import json
class Parser(object):
	def desc_proprocess(self, desc_raw):
		desc = (desc_raw.replace("([","{")).replace("])","}")
		desc = (desc.replace("({","[")).replace("})","]")
		desc = (desc.replace(",]","]")).replace(",}","}")
		return desc

	def parse_equipment(self, equip_desc_raw):
		desc = self.desc_proprocess(equip_desc_raw)
		exec("desc_dict={}".format(desc))
		return 

	def parse_pet(self, pet_desc_raw):
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

		return pet

	def parse_equipment_pet(self, pet_equip_desc):	
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
'''
import requests,json 
from bs4 import BeautifulSoup       
cookies = {
    'return_url': '',
    '_ntes_nnid': 'f41ef8df7177b5cce4b6998459732ad7,1507306056551',
    '_ntes_nuid': 'f41ef8df7177b5cce4b6998459732ad7',
    'mail_psc_fingerprint': 'c441de3789be31154e56da7e6278eff7',
    '__gads': 'ID=6f7603f0c1535d9d:T=1508233071:S=ALNI_MYk4mdH8HNKjwT5zZ0rYZRrNo2U3Q',
    'vjuids': '68ed97bc2.15f29b24f48.0.195d90906af4b',
    'usertrack': 'ezq0plpCFBFTaw51BOivAg==',
    '_ga': 'GA1.2.2079835337.1515185790',
    'nts_mail_user': 'scrcss^@163.com:-1:1',
    '__f_': '1526827265735',
    'NTES_CMT_USER_INFO': '128102521^%^7C^%^E6^%^9C^%^89^%^E6^%^80^%^81^%^E5^%^BA^%^A6^%^E7^%^BD^%^91^%^E5^%^8F^%^8B07EH1V^%^7C^%^7Cfalse^%^7CejUxNjY3MjMxNUAxNjMuY29t',
    'vjlast': '1508233072.1530296263.12',
    'NTES_PASSPORT': 'QraZxXzQ7YYWWaPYbzHF0kZUm.kRa5WqFFFrYnuUmcEjiMDHHPkwgq1ydXCQMiN2WrAgKzKRAcKtwxEqUQ2wPyUZPETZgbGnPslmOcEfMR5exO0Z1XfH8g5ybuyVXfBo406PSrP9WIHRQ7w4BVM1W6kgrlpm0uQZYL_eGl9o1meqh',
    'Province': '020',
    'City': '020',
    'area_id': '43',
    'P_INFO': 'z516672315^@163.com^|1531912549^|0^|ecard^|00^&9^|gud^&1531896454^&xyq^#gud^&442000^#10^#0^#0^|137555^&0^|xyq^&game^|z516672315^@163.com',
    '__session__': '1',
    'cur_servername': '^%^25E5^%^25A6^%^2582^%^25E6^%^2584^%^258F^%^25E5^%^25B2^%^259B',
    'ne_analysis_trace_id': '1532078257359',
    's_n_f_l_n3': '1e2567de83865b291532078257363',
    'vinfo_n_f_l_n3': '1e2567de83865b29.1.12.1508233072482.1530693619470.1532078548093',
    'latest_views': '79_2722560-79_2614400-79_2690491-79_2723699-79_2674185-79_2687820-79_2730577-79_2730516-79_2730820-79_2646901-79_2690917-79_2679076-79_2703512-79_2594887-79_2729006-79_2690462-79_2654109-79_2729003-79_2730360-79_2693640',
    'wallet_data': '^%^7B^%^22is_locked^%^22^%^3A^%^20false^%^2C^%^20^%^22checking_balance^%^22^%^3A^%^200^%^2C^%^20^%^22balance^%^22^%^3A^%^200^%^2C^%^20^%^22free_balance^%^22^%^3A^%^200^%^7D',
    'cbg_qrcode': '-QD-pP1LNXhaSKwa0cQaZpKYdmPTfRbhSTaSWUOT',
    'NTES_SESS': 'Z7vH2cJNXfCJ1rUhcM6ccgGDWfX5WsQ3vKoyAdMRnwUnVg255XvOEWd.M8hpgVorj3OnN0UBkiXkWdQBj33whtXW_hmdnUg8qxWqr5EMt27dxZaCwOpgKXA5nTYXfQJO2O0e5q5gGL.vkXDdgZt_vdEHaFLytl4yxVr0QznrcSgqsSyomAbJvemmvMT05JO2qVZxp5JRGF9RI',
    'S_INFO': '1532443029^|1^|0^&80^#^#^|z516672315',
    'ANTICSRF': 'fa780103c310bd9505d73490f82c79fc',
    'sid': 'PCPslCIpcxjS-aeYoFpJEgciF_dDld8WS3CV9vbw',
    'fingerprint': '2254594943',
    'no_login_mark': '1',
    'overall_sid': 'vIoEjr7uY_z5z2BX6GB1eCiPbY29A_8KPRCoJS1O',
}

headers = {
    'Connection': 'keep-alive',
    'Cache-Control': 'max-age=0',
    'Upgrade-Insecure-Requests': '1',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.99 Safari/537.36',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
    'Referer': 'https://xyq.cbg.163.com/equip?s=137^&eid=201807222000113-137-N4DUORXHSATR^&o^&equip_refer=1',
    'Accept-Encoding': 'gzip, deflate, br',
    'Accept-Language': 'zh-CN,zh;q=0.9',
    'accept-encoding': 'gzip, deflate, br',
    'accept-language': 'zh-CN,zh;q=0.9',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.99 Safari/537.36',
    'accept': 'image/webp,image/apng,image/*,*/*;q=0.8',
    'referer': 'https://xyq.cbg.163.com/cgi-bin/equipquery.py?act=show_overall_search_pet',
    'authority': 'analytics.163.com',
    'cookie': '_ntes_nnid=f41ef8df7177b5cce4b6998459732ad7,1507306056551; _ntes_nuid=f41ef8df7177b5cce4b6998459732ad7; mail_psc_fingerprint=c441de3789be31154e56da7e6278eff7; __gads=ID=6f7603f0c1535d9d:T=1508233071:S=ALNI_MYk4mdH8HNKjwT5zZ0rYZRrNo2U3Q; vjuids=68ed97bc2.15f29b24f48.0.195d90906af4b; usertrack=ezq0plpCFBFTaw51BOivAg==; _ga=GA1.2.2079835337.1515185790; nts_mail_user=scrcss^@163.com:-1:1; __f_=1526827265735; NTES_CMT_USER_INFO=128102521^%^7C^%^E6^%^9C^%^89^%^E6^%^80^%^81^%^E5^%^BA^%^A6^%^E7^%^BD^%^91^%^E5^%^8F^%^8B07EH1V^%^7C^%^7Cfalse^%^7CejUxNjY3MjMxNUAxNjMuY29t; vjlast=1508233072.1530296263.12; NTES_PASSPORT=QraZxXzQ7YYWWaPYbzHF0kZUm.kRa5WqFFFrYnuUmcEjiMDHHPkwgq1ydXCQMiN2WrAgKzKRAcKtwxEqUQ2wPyUZPETZgbGnPslmOcEfMR5exO0Z1XfH8g5ybuyVXfBo406PSrP9WIHRQ7w4BVM1W6kgrlpm0uQZYL_eGl9o1meqh; Province=020; City=020; P_INFO=z516672315^@163.com^|1531912549^|0^|ecard^|00^&9^|gud^&1531896454^&xyq^#gud^&442000^#10^#0^#0^|137555^&0^|xyq^&game^|z516672315^@163.com; ne_analysis_trace_id=1532078257359; s_n_f_l_n3=1e2567de83865b291532078257363; vinfo_n_f_l_n3=1e2567de83865b29.1.12.1508233072482.1530693619470.1532078548093; NTES_SESS=Z7vH2cJNXfCJ1rUhcM6ccgGDWfX5WsQ3vKoyAdMRnwUnVg255XvOEWd.M8hpgVorj3OnN0UBkiXkWdQBj33whtXW_hmdnUg8qxWqr5EMt27dxZaCwOpgKXA5nTYXfQJO2O0e5q5gGL.vkXDdgZt_vdEHaFLytl4yxVr0QznrcSgqsSyomAbJvemmvMT05JO2qVZxp5JRGF9RI; S_INFO=1532443029^|1^|0^&80^#^#^|z516672315; ANTICSRF=fa780103c310bd9505d73490f82c79fc',
}

params = (
    ('act', 'show_overall_search_pet'),
)

response = requests.get('https://xyq.cbg.163.com/cgi-bin/equipquery.py', headers=headers, params=params, cookies=cookies)

#NB. Original query string below. It seems impossible to parse and
#reproduce query strings 100% accurately so the one below is given
#in case the reproduced version is not "correct".
# response = requests.get('https://xyq.cbg.163.com/cgi-bin/equipquery.py?act=show_overall_search_pet', headers=headers, cookies=cookies)
#page = requests.get(url, headers=header) # 解析网页
response.encoding = "GBK"
bsobj = BeautifulSoup(response.text, "html.parser")
table = bsobj.find("table")
print(table)

pets = json.loads(response.text)
pet=pets["msg"][0]

pet=Pet()
desc = self.desc_proprocess(pet_desc_raw)
desc=one_pet["large_equip_desc"]
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
pet.DRNC = (desc_list[18])

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

pet.equip1 = self.parse_equipment_pet()
'''