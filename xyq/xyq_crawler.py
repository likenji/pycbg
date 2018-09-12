# -*- coding: utf-8 -*-
"""
Created on Tue Aug 21 11:00:28 2018

@author: 51667
"""
from bs4 import BeautifulSoup
import datetime
import json
import re
import requests

from pycbg.xyq.xyq_parser import Parser
SERVER_ID = 79
LIST_SELLING_INFO = ["price", "can_bargain", "status", "selling_time"]

class Crawler(object):	
	def __init__(self):	
		self.type_name = "xyq"
		self.session = requests.Session()			
		self.headers = self.get_headers()
		self.cookies = self.get_cookies(SERVER_ID)
		self.parser = Parser()

	def get_headers(self):
		return {
		'Connection': 'keep-alive',
		'Upgrade-Insecure-Requests': '1',
		'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.75 Safari/537.36',
		'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
		'Referer': 'https://xyq.cbg.163.com/',
		'Accept-Encoding': 'gzip, deflate, br',
		'Accept-Language': 'zh-CN,zh;q=0.9',}

	def refresh_cookies(self, server_id):
		self.session.get("https://xyq.cbg.163.com", headers = self.headers,)
		data={
			  "act": "do_anon_auth",
			  "server_id": server_id,
		}
		self.session.post("https://xyq.cbg.163.com/cgi-bin/login.py", data=data, headers=self.headers)
		self.cookies = self.session.cookies

	def get_cookies(self, server_id):
		self.refresh_cookies(server_id)
		return self.session.cookies

	def get_exchange_rate(self, server_id, page_num=1):
		#结果可以保存到本地
		gold_price_list = []
		self.cookies = self.get_cookies(server_id)
		for page in range(1, page_num+1):
			params = (
			('act', 'query'),
			('server_id', server_id),
			('page', page),
			('kindid', '23'),)
			response = requests.get('https://xyq.cbg.163.com/cgi-bin/query.py', headers=self.headers, params=params, cookies=self.cookies)
			response.encoding = "GBK"
			bsobj = BeautifulSoup(response.text, "html.parser")
			gold_price_list.extend([eval(gold_info.findAll("td")[-1].text.split(" ")[-1].split("元/万两")[0]) for gold_info in bsobj.findAll("tr")])
		return gold_price_list

	def get_overall_role_id(self, page_num=1):
		list_info = []
		for page in range(1, page_num+1):
			print(page)
			params = (
				('server_type', '3'),
				('act', 'overall_search_role'),
				('page', page),
				('order_by', 'expire_time DESC')
			)
			response = requests.get('https://xyq.cbg.163.com/cgi-bin/xyq_overall_search.py?', headers=self.headers, params=params,)
			#NB. Original query string below. It seems impossible to parse and
			#reproduce query strings 100% accurately so the one below is given
			#in case the reproduced version is not "correct".
			# response = requests.get('https://xyq.cbg.163.com/cgi-bin/xyq_overall_search.py?server_type=3&act=overall_search_role&page=1', headers=headers, cookies=cookies)
			info = json.loads(response.text)
			list_info.append(info)

		list_role_id = []    
		for info in list_info:
			list_role_id.extend([(sub["serverid"], sub["game_ordersn"]) for sub in info["equip_list"]])
		return list_role_id

	def get_server_role(self, server_id, page_num=1):
		role_urls = []
		cookies = self.get_cookies(server_id)
		for page in range(1, page_num+1):
			params = (
			('act', 'search_role'),
			('page', page),
			('query_order', 'selling_time DESC')
		)
			response = requests.get('https://xyq.cbg.163.com/cgi-bin/query.py', headers=headers, params=params, cookies=self.cookies)
			response.encoding = "GBK"
			bsobj = BeautifulSoup(response.text, "html.parser")
			role_info = bsobj.findAll("a",{"class":"soldImg"})
			role_urls.extend([info["href"] for info in role_info])
		return role_urls

	def get_response_by_id(self, role_id):		
		if type(role_id) == tuple:
			while 1:
				params = (
					('act', 'overall_search_show_detail'),
					('serverid', role_id[0]),
					('ordersn', role_id[1]),
					#('equip_refer', '1'),			
				)
				response = requests.get('https://xyq.cbg.163.com/cgi-bin/equipquery.py', headers=self.headers, params=params,)
				response.encoding = "GBK"
				if response:
					return response
				else:					
					self.cookies = self.get_cookies(server_id)
					print(response)
					print("retry with latest cookies!")

	def get_role_desc_by_id(self, role_id):
		if type(role_id) == tuple:
			while 1:
				params = (
					('act', 'overall_search_show_detail'),
					('serverid', role_id[0]),
					('ordersn', role_id[1]),
					#('equip_refer', '1'),			
				)
				response = requests.get('https://xyq.cbg.163.com/cgi-bin/equipquery.py', headers=self.headers, params=params,)
				response.encoding = "GBK"
				bsobj = BeautifulSoup(response.text, "html.parser")
				role_desc = bsobj.findAll("textarea", {"id":"equip_desc_value"})[0].text
				if role_desc:
					return role_desc
				else:
					self.cookies = self.get_cookies(server_id)
					print("retry with latest cookies!")

	def get_role_by_id(self, role_id):	
		response = self.get_response_by_id(role_id)
		bsobj = BeautifulSoup(response.text, "html.parser")
		role_desc = bsobj.findAll("textarea", {"id":"equip_desc_value"})[0].text
		role = self.parser.parse_role(self.parser.desc_preprocess(self.parser.remove_tap(role_desc)))
		role.server_id = role_id[0]
		role.ordersn = role_id[1]
		
		script = bsobj.findAll("script")[25].text.replace("\n","").replace("\t","")
		if "var equip =" in script:
			str_sellingInfo = re.findall('var equip = (.*?),\"valid_bargain_resp\"', script)[0] + "}"
			dict_sellingInfo = json.loads(str_sellingInfo)
			role.sellingInfo.append(dict_sellingInfo)
		else:
			raise("not found sellingInfo")
		return role

	def get_latest_role_sellingInfo(self, role_id):	
		response = self.get_response_by_id(role_id)
		bsobj = BeautifulSoup(response.text, "html.parser")
		role_desc = bsobj.findAll("textarea", {"id":"equip_desc_value"})[0].text
		role = self.parser.parse_role(self.parser.desc_preprocess(self.parser.remove_tap(role_desc)))
		role.server_id = role_id[0]
		role.ordersn = role_id[1]
		
		script = bsobj.findAll("script")[25].text.replace("\n","").replace("\t","")
		str_sellingInfo = re.findall('var equip = (.*?),\"valid_bargain_resp\"', script)[0] + "}"
		dict_sellingInfo = json.loads(str_sellingInfo)

		role.sellingInfo.append(dict_sellingInfo)
		return role


if __name__ == "__main__":
	crawler = Crawler()
	'''
	price = crawler.get_exchange_rate(39)
	list_role_id=crawler.get_overall_role_id()
	print(list_role_id)
	print(crawler.get_role_desc_by_id(list_role_id[0]))
	print(crawler.get_role_by_id((139, '95_1473036251_95768900')).__dict__)
	'''
	r = crawler.get_response_by_id((139, '95_1473036251_95768900'))
	print(r)

