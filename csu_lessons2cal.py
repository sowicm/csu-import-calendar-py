# coding: utf-8
from __future__ import print_function
from selenium import webdriver
import time
import urllib
import urllib2
from pyquery import PyQuery as pq
#from scanf import sscanf
from parse import *
from datetime import date, timedelta
import os
import sys
reload(sys)
sys.setdefaultencoding('utf-8')

stuid_str = ''
passwd_str = ''
if os.path.exists('key.txt'):
	with open('key.txt', 'rb') as f:
		stuid_str = f.readline().strip()
		passwd_str = f.readline().strip()

# 参考：
# https://github.com/sowicm/csu-import-calendar/blob/master/source.cpp
# http://www.cnblogs.com/fnng/archive/2013/05/29/3106515.html
# http://my.oschina.net/Early20/blog/363831
# http://www.cnblogs.com/fnng/p/3269450.html
# http://blog.bccn.net/静夜思/16744
# http://blog.csdn.net/warrior_zhang/article/details/50198699
# http://blog.csdn.net/mack415858775/article/details/39696107
# http://wenku.baidu.com/link?url=EZRxlD_zraNyBgdsDU2q5WmPiKmF0OBwH6GhVrK_MeLJyeFgvFmrTqxvdrR12iaDmFFyKqZgHutNzp8PXXfpTVoYLMcZkPSYqU7hBIzcEZS
# https://pypi.python.org/pypi/parse
# http://blog.csdn.net/longshengguoji/article/details/9918645
# https://hkn.eecs.berkeley.edu/~dyoo/python/scanf/
# https://www.zhihu.com/question/21572891

weekdays = {
	'日':7, #0
	'一':1,
	'二':2,
	'三':3,
	'四':4,
	'五':5,
	'六':6
}

node_time = [
	"080000",
	"084500",
	"085500",
	"094000",
	"100000",
	"104500",
	"105500",
	"114000",
	"140000",
	"144500",
	"145500",
	"154000",
	"160000",
	"164500",
	"165500",
	"174000",
	"190000",
	"194500",
	"195500",
	"204000"
]

weekday_short_2 = [
    "SU",
    "MO",
    "TU",
    "WE",
    "TH",
    "FR",
    "SA",
    "SU"
];

first_day = date(2016, 2, 28) - timedelta(days = 7)

if True:
	login_url = 'http://csujwc.its.csu.edu.cn/default.aspx'

	browser = webdriver.Firefox()
	#browser.set_page_load_timeout(20)
	browser.get(login_url)

	browser.find_element_by_id("td3").click()

	browser.switch_to.frame('frmHomeShow')
	if len(stuid_str) > 0:
		stuid = browser.find_element_by_xpath("//input[@name='txt_sdsdfdsfryuiighgdf']")
		stuid.send_keys( stuid_str )
	if len(passwd_str) > 0:
		passwd = browser.find_element_by_xpath("//input[@name='txt_dsfdgtjhjuixssdsdf']")
		passwd.send_keys( passwd_str )
	form = browser.find_element_by_xpath("//form[@name='Logon']")
	#pause = raw_input('先手动输入一下验证码')
	#form.submit()

	while browser.current_url == login_url:
		time.sleep(1)

	#browser.switch_to.frame('frmRpt')

	cookie = [item["name"] + '=' + item["value"] for item in browser.get_cookies()]
	cookiestr = ';'.join(item for item in cookie)
	print('Cookie:')
	print(cookiestr)
	#data = {}
	#data = urllib.urlencode(data)
else:
	with open('csu_lessons2cal.txt', 'rb') as f:
		txt = f.read().decode('utf-8')

def translate(txt, indexes):

	t = pq(txt)
	table = t('input[name="chkCount"]').prev()
	#trs = table('tr')
	itr = 0
	for k in table.children():
		child = pq(k)
		if child.hasClass('T'):
			continue
		if itr == indexes[0]:#1:
			title = child.text()
			title = title[title.index(']')+1:]
#			print('title:')
#			print(title)
		elif itr == indexes[1]:#2:
			grade = child.text()
		elif itr == indexes[2]:#4:
			teacher = child.text()
		elif itr == indexes[3]:#10:
			#if not '周' in child.text():
			if not '[' in child.text():
				print('Attention:' + title)
				itr = 0
				continue
			lines = child.text().replace('@', ' ').split(' ')
			for line in lines:
	#			print('line:')
	#			print(line)
				info = line.split('/')
	#			print('info:')
	#			print(info)
	#			print('info[0]')
	#			print(info[0])
				location = info[1]
				timeinfo = parse('[{}周]星期{}[{}-{}节]'.decode('utf-8'), info[0])
#				print('timeinfo:')
#				print(timeinfo)
#				print('timeinfo[1]')
#				print(timeinfo[1])
#				print(weekdays)
				#while True:print eval(raw_input('DEBUG>>>'))
				weeks = []
				for w in timeinfo[0].split(','):
					#if '-' in w:
					#	weeks.append(w.split('-'))
					#else:
					#	weeks.append()
					weeks.append(w.split('-'))
					if len(weeks[-1]) < 2:
						weeks[-1].append(weeks[-1][0])
				#if '-' in timeinfo[0]:
				#	week = timeinfo[0].split('-')
				#elif 
				for week in weeks:
					start_day = first_day + timedelta(days = 7 * int(week[0]))
					number_weeks = int(week[1]) - int(week[0]) + 1
					weekday = weekdays.get(timeinfo[1].encode('utf-8'))
					start_day += timedelta(days = weekday)
					fp.write('BEGIN:VEVENT\n')
					start_node = int(timeinfo[2])-1
					end_node = int(timeinfo[3])-1
					fp.write("DTSTART;TZID=Asia/Shanghai:" + start_day.strftime('%Y%m%dT') + node_time[start_node * 2] + '\n')
					fp.write("DTEND;TZID=Asia/Shanghai:" + start_day.strftime('%Y%m%dT') + node_time[end_node * 2 + 1] + '\n')
					if number_weeks > 1:
						fp.write('RRULE:FREQ=WEEKLY;COUNT=' + str(number_weeks) + ';BYDAY=' + weekday_short_2[weekday] + '\n')
					fp.write("DESCRIPTION:" + teacher + ';(' + grade + ")\n")
					fp.write('LOCATION:' + location + '\n')
					fp.write("STATUS:CONFIRMED\n")
					fp.write("SUMMARY:" + title + "\n")
					fp.write("TRANSP:OPAQUE\nEND:VEVENT\n")
			itr = -1
		itr += 1

fp = open('csu_lessons2cal.ics', 'wb')
fp.write("BEGIN:VCALENDAR\nVERSION:2.0\nPRODID:-//Sowicm.com//CSU Export Class Info as iCalendar//EN\n")

headers = {'cookie': cookiestr}

#req = urllib2.Request(method='post', 'xxx', data = data, headers = headers)
req = urllib2.Request('http://csujwc.its.csu.edu.cn/wsxk/stu_zxjg_rpt.aspx', headers = headers)
response = urllib2.urlopen(req)
txt = response.read().decode('gb18030') #.encode('utf-8')
with open('csu_lessons_zx.txt', 'wb') as f:
	f.write(txt.encode('utf-8'))

translate(txt, [1,2,4,10])

req = urllib2.Request('http://csujwc.its.csu.edu.cn/wsxk/stu_cxjg_rpt.aspx', headers = headers)
response = urllib2.urlopen(req)
txt = response.read().decode('gb18030') #.encode('utf-8')
with open('csu_lessons_cx.txt', 'wb') as f:
	f.write(txt.encode('utf-8'))

translate(txt, [1,2,4,9])

fp.write("END:VCALENDAR")

