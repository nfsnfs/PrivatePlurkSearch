#!/usr/bin/python
# old version 
# prepare to update to Plurk API 2.0
# -*- coding: utf-8 -*-
import urllib, urllib2, cookielib, time, simplejson, string, sys


def _baseN(num, b):
	return ((num == 0) and  "0" ) or ( _baseN(num // b, b).lstrip("0") + "0123456789abcdefghijklmnopqrstuvwxyz"[num % b])  # from plurkapi.py


opener = urllib2.build_opener(urllib2.HTTPCookieProcessor())
api_key = ''	# your api key
get_api_url = lambda x: 'http://www.plurk.com/API%s' % x
encode = urllib.urlencode
user_name = '' # your username
pass_word = '' # your password

max_plurk = 100 # default max plurks
total_plurk = 0

reload(sys)
sys.setdefaultencoding('utf-8')

search_user = ''
search_word = ''

if api_key == '' or user_name == '' or pass_word == '':
	print 'api_key, user_name, pass_word is not well-set!'
	exit()


nowtime = time.strftime("%Y-%m-%dT%H:%M:%S", time.localtime(time.time()))

only_private = 'only_private'

month = {'Jan':'01', 'Fab':'02', 'Mar':'03', 'Apr':'04', 'May':'05', 'Jun': '06', 'Jul':'07', 'Aug': '08', 'Sep':'09', 'Oct':'10', 'Nov':'11', 'Dec':'12'}

#print nowtime

# login
fp = opener.open(get_api_url('/Users/login'),
               	encode({'username': user_name,
               	        'password': pass_word,
                        'no_data': 1,
                        'api_key': api_key}))

result = simplejson.load(fp);

if result['success_text'] == 'ok':
	print 'Login Success'


# get plurk
while total_plurk < max_plurk:
	fp = opener.open(get_api_url('/Timeline/getPlurks'),
			 encode({'api_key': api_key,
				 'offset': nowtime,
				 'limit': max_plurk-total_plurk,
				 'filter': only_private}))

	result = simplejson.load(fp)
	max = len(result['plurks'])
	total_plurk = total_plurk + max

	if max != 0:
		i = 0
		while i < max:
			s = simplejson.dumps(result['plurks'][i])
			plurkset = simplejson.loads(s)
			ownerid_set = str(plurkset['owner_id'])
			k = simplejson.dumps(result['plurk_users'][ownerid_set])
			id = simplejson.loads(k)
			
			if id['nick_name'] == search_user or search_user == '':
				if search_word in plurkset['content_raw']:
					print   id['nick_name'].decode('cp950').encode('utf-8') + ' ' + plurkset['qualifier'].decode('cp950').encode('utf-8') + ':' + plurkset['content_raw'] + ' ' + 'http://www.plurk.com/p/'+ _baseN(plurkset['plurk_id'], 36)
			i = i + 1

	# time combination
		s = simplejson.dumps(result['plurks'][i-1])
		r = simplejson.loads(s)
		nowtime = time.strptime(r['posted'][5:8] + month[r['posted'][8:11]] + r['posted'][11:25], '%d %m %Y %H:%M:%S')
	
	else:
		fp.close()
		print 'Search ' + str(total_plurk) + ' plurks'
		exit()

print 'Search ' + str(total_plurk) + ' plurks'
fp.close()

