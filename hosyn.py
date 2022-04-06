import asyncio
import base64
import concurrent.futures
import datetime
import glob
import json
import math
import os
import pathlib
import random
import sys
import time
from json import dumps, loads
from random import randint
import re
from re import findall
import requests
import urllib3
from Crypto.Cipher import AES
from hosyn_bot_file  import Bot,encryption
from Crypto.Util.Padding import pad, unpad
from requests import post
from googletrans import Translator
import io
import arabic_reshaper
from bidi.algorithm import get_display
from mutagen.mp3 import MP3
from gtts import gTTS
from threading import Thread
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
from difflib import SequenceMatcher
def similar(a, b):
    return SequenceMatcher(None, a, b).ratio()

def hasAds(msg):
	links = ["http://","https://",".ir",".com",".org",".net",".me"]
	for i in links:
		if i in msg:
			return True

def hasAds(msg):
	links = list(map(lambda ID: ID.strip()[1:],findall("@[\w|_|\d]+", msg))) + list(map(lambda link:link.split("/")[-1],findall("rubika\.ir/\w+",msg)))
	joincORjoing = "joing" in msg or "joinc" in msg

	if joincORjoing: return joincORjoing
	else:
		for link in links:
			try:
				Type = bot.getInfoByUsername(link)["data"]["chat"]["abs_object"]["type"]
				if Type == "Channel":
					return True
			except KeyError: return False

def search_i(text,chat,bot):
    try:
        search = text[11:-1]
        if hasInsult(search)[0] == False and chat['abs_object']['type'] == 'Group':
            bot.sendMessage(chat['object_guid'], 'نتایج کامل به زودی به پیوی شما ارسال میشوند', chat['last_message']['message_id'])                           
            jd = json.loads(requests.get('https://zarebin.ir/api/image/?q=' + search + '&chips=&page=1').text)
            jd = jd['results']
            a = 0
            for j in jd:
                if a <= 8:
                    try:
                        res = requests.get(j['image_link'])
                        if res.status_code == 200 and res.content != b'' and j['cdn_thumbnail'] != '':
                            thumb = str(j['cdn_thumbnail'])
                            thumb = thumb.split('data:image/')[1]
                            thumb = thumb.split(';')[0]
                            if thumb == 'png':
                                b2 = res.content
                                width, height = bot.getImageSize(b2)
                                tx = bot.requestFile(j['title'] + '.png', len(b2), 'png')
                                access = bot.fileUpload(b2, tx['access_hash_send'], tx['id'], tx['upload_url'])
                                bot.sendImage(chat['last_message']['author_object_guid'] ,tx['id'] , 'png', tx['dc_id'] , access, j['title'] + '.png', len(b2), str(bot.getThumbInline(b2))[2:-1] , width, height, j['title'])
                                print('sended file')
                            elif thumb == 'webp':
                                b2 = res.content
                                width, height = bot.getImageSize(b2)
                                tx = bot.requestFile(j['title'] + '.webp', len(b2), 'webp')
                                access = bot.fileUpload(b2, tx['access_hash_send'], tx['id'], tx['upload_url'])
                                bot.sendImage(chat['last_message']['author_object_guid'] ,tx['id'] , 'webp', tx['dc_id'] , access, j['title'] + '.webp', len(b2), str(bot.getThumbInline(b2))[2:-1] , width, height, j['title'])
                                print('sended file')
                            else:
                                b2 = res.content
                                width, height = bot.getImageSize(b2)
                                tx = bot.requestFile(j['title'] + '.jpg', len(b2), 'jpg')
                                access = bot.fileUpload(b2, tx['access_hash_send'], tx['id'], tx['upload_url'])
                                bot.sendImage(chat['last_message']['author_object_guid'] ,tx['id'] , 'jpg', tx['dc_id'] , access, j['title'] + '.jpg', len(b2), str(bot.getThumbInline(b2))[2:-1] , width, height, j['title'])
                                print('sended file')
                        a += 1
                    except:
                        print('image error')
                else:
                    break                                    
        elif chat['abs_object']['type'] == 'User':
            bot.sendMessage(chat['object_guid'], 'در حال یافتن کمی صبور باشید...', chat['last_message']['message_id'])
            print('search image')
            jd = json.loads(requests.get('https://zarebin.ir/api/image/?q=' + search + '&chips=&page=1').text)
            jd = jd['results']
            a = 0
            for j in jd:
                if a < 10:
                    try:                        
                        res = requests.get(j['image_link'])
                        if res.status_code == 200 and res.content != b'' and j['cdn_thumbnail'] != '' and j['cdn_thumbnail'].startswith('data:image'):
                            thumb = str(j['cdn_thumbnail'])
                            thumb = thumb.split('data:image/')[1]
                            thumb = thumb.split(';')[0]
                            if thumb == 'png':
                                b2 = res.content
                                width, height = bot.getImageSize(b2)
                                tx = bot.requestFile(j['title'] + '.png', len(b2), 'png')
                                access = bot.fileUpload(b2, tx['access_hash_send'], tx['id'], tx['upload_url'])
                                bot.sendImage(chat['object_guid'] ,tx['id'] , 'png', tx['dc_id'] , access, j['title'] + '.png', len(b2), str(bot.getThumbInline(b2))[2:-1] , width, height, j['title'], chat['last_message']['message_id'])
                                print('sended file')
                            elif thumb == 'webp':
                                b2 = res.content
                                width, height = bot.getImageSize(b2)
                                tx = bot.requestFile(j['title'] + '.webp', len(b2), 'webp')
                                access = bot.fileUpload(b2, tx['access_hash_send'], tx['id'], tx['upload_url'])
                                bot.sendImage(chat['object_guid'] ,tx['id'] , 'webp', tx['dc_id'] , access, j['title'] + '.webp', len(b2), str(bot.getThumbInline(b2))[2:-1] , width, height, j['title'], chat['last_message']['message_id'])
                                print('sended file')
                            else:
                                b2 = res.content
                                tx = bot.requestFile(j['title'] + '.jpg', len(b2), 'jpg')
                                access = bot.fileUpload(b2, tx['access_hash_send'], tx['id'], tx['upload_url'])
                                width, height = bot.getImageSize(b2)
                                bot.sendImage(chat['object_guid'] ,tx['id'] , 'jpg', tx['dc_id'] , access, j['title'] + '.jpg', len(b2), str(bot.getThumbInline(b2))[2:-1] , width, height, j['title'], chat['last_message']['message_id'])
                                print('sended file')
                        a += 1  
                    except:
                        print('image erorr')
        return True
    except:
        print('image search err')
        return False

def write_image(text,chat,bot):
    try:
        c_id = chat['last_message']['message_id']
        msg_data = bot.getMessagesInfo(chat['object_guid'], [c_id])
        msg_data = msg_data[0]
        if 'reply_to_message_id' in msg_data.keys():
            msg_data = bot.getMessagesInfo(chat['object_guid'], [msg_data['reply_to_message_id']])[0]
            if 'text' in msg_data.keys() and msg_data['text'].strip() != '':
                txt_xt = msg_data['text']
                paramiters = text[8:-1]
                paramiters = paramiters.split(':')
                if len(paramiters) == 5:
                    b2 = bot.write_text_image(txt_xt,paramiters[0],int(paramiters[1]),str(paramiters[2]),int(paramiters[3]),int(paramiters[4]))
                    tx = bot.requestFile('code_image.png', len(b2), 'png')
                    access = bot.fileUpload(b2, tx['access_hash_send'], tx['id'], tx['upload_url'])
                    width, height = bot.getImageSize(b2)
                    bot.sendImage(chat['object_guid'] ,tx['id'] , 'png', tx['dc_id'] , access, 'code_image.png', len(b2) , str(bot.getThumbInline(b2))[2:-1] , width, height ,message_id= c_id)
                    print('sended file') 
                    return True
        return False	              
    except:
        print('server ban bug')
        return False

def uesr_remove(text,chat,bot):
    try:
        admins = [i["member_guid"] for i in bot.getGroupAdmins(chat['object_guid'])["data"]["in_chat_members"]]
        if chat['last_message']['author_object_guid'] in admins:
            c_id = chat['last_message']['message_id']
            msg_data = bot.getMessagesInfo(chat['object_guid'], [c_id])
            msg_data = msg_data[0]
            if 'reply_to_message_id' in msg_data.keys():
                msg_data = bot.getMessagesInfo(chat['object_guid'], [msg_data['reply_to_message_id']])[0]
                if not msg_data['author_object_guid'] in admins:
                    bot.banGroupMember(chat['object_guid'], msg_data['author_object_guid'])
                    bot.sendMessage(chat['object_guid'], 'انجام شد' , chat['last_message']['message_id'])
                    return True
        return False
    except:
        print('server ban bug')
        return False

def speak_after(text,chat,bot):
    try:
        c_id = chat['last_message']['message_id']
        msg_data = bot.getMessagesInfo(chat['object_guid'], [c_id])
        msg_data = msg_data[0]
        if 'reply_to_message_id' in msg_data.keys():
            msg_data = bot.getMessagesInfo(chat['object_guid'], [msg_data['reply_to_message_id']])[0]
            if 'text' in msg_data.keys() and msg_data['text'].strip() != '':
                txt_xt = msg_data['text']
                speech = gTTS(txt_xt)
                changed_voice = io.BytesIO()
                speech.write_to_fp(changed_voice)
                b2 = changed_voice.getvalue()
                tx = bot.requestFile('sound.ogg', len(b2), 'sound.ogg')
                access = bot.fileUpload(b2, tx['access_hash_send'], tx['id'], tx['upload_url'])
                f = io.BytesIO()
                f.write(b2)
                f.seek(0)
                audio = MP3(f)
                dur = audio.info.length
                bot.sendVoice(chat['object_guid'],tx['id'] , 'ogg', tx['dc_id'] , access, 'sound.ogg', len(b2), dur * 1000 ,message_id= c_id)
                print('sended voice')
                return True
        return False
    except:
        print('server gtts bug')
        return False

def info_hosyn(text,chat,bot):
    try:
        user_info = bot.getInfoByUsername(text[7:])	
        if user_info['data']['exist'] == True:
            if user_info['data']['type'] == 'User':
                bot.sendMessage(chat['object_guid'], 'name:\n  ' + user_info['data']['user']['first_name'] + ' ' + user_info['data']['user']['last_name'] + '\n\nbio:\n   ' + user_info['data']['user']['bio'] + '\n\nguid:\n  ' + user_info['data']['user']['user_guid'] , chat['last_message']['message_id'])
                print('sended response')
            else:
                bot.sendMessage(chat['object_guid'], 'کانال است' , chat['last_message']['message_id'])
                print('sended response')
        else:
            bot.sendMessage(chat['object_guid'], 'وجود ندارد' , chat['last_message']['message_id'])
            print('sended response')
        return True
    except:
        print('server bug6')
        return False

def search(text,chat,bot):
    try:
        search = text[9:-1]    
        if hasInsult(search)[0] == False and chat['abs_object']['type'] == 'Group':                               
            jd = json.loads(requests.get('https://zarebin.ir/api/?q=' + search + '&page=1&limit=10').text)
            results = jd['results']['webs']
            text = ''
            for result in results:
                text += result['title'] + '\n\n'
            bot.sendMessage(chat['object_guid'], 'نتایج به پیوی شما ارسال شد', chat['last_message']['message_id'])
            bot.sendMessage(chat['last_message']['author_object_guid'], 'نتایج یافت شده برای (' + search + ') : \n\n'+text)
        elif chat['abs_object']['type'] == 'User':
            jd = json.loads(requests.get('https://zarebin.ir/api/?q=' + search + '&page=1&limit=10').text)
            results = jd['results']['webs']
            text = ''
            for result in results:
                text += result['title'] + '\n\n'
            bot.sendMessage(chat['object_guid'], text , chat['last_message']['message_id'])
        return True
    except:
        print('search zarebin err')
        bot.sendMessage(chat['object_guid'], 'در حال حاضر این دستور محدود یا در حال تعمیر است' , chat['last_message']['message_id'])
        return False

def p_danesh(text,chat,bot):
    try:
        res = requests.get('http://api.codebazan.ir/danestani/pic/')
        if res.status_code == 200 and res.content != b'':
            b2 = res.content
            width, height = bot.getImageSize(b2)
            tx = bot.requestFile('jok_'+ str(random.randint(1000000, 9999999)) + '.png', len(b2), 'png')
            access = bot.fileUpload(b2, tx['access_hash_send'], tx['id'], tx['upload_url'])
            bot.sendImage(chat['object_guid'] ,tx['id'] , 'png', tx['dc_id'] , access, 'jok_'+ str(random.randint(1000000, 9999999)) + '.png', len(b2), str(bot.getThumbInline(b2))[2:-1] , width, height, message_id=chat['last_message']['message_id'])
            print('sended file')                       
        return True
    except:
        print('code bz danesh api bug')
        return False

def anti_insult(text,chat,bot):
    try:
        admins = [i["member_guid"] for i in bot.getGroupAdmins(chat['object_guid'])["data"]["in_chat_members"]]
        if not chat['last_message']['author_object_guid'] in admins:
            print('yek ahmagh fohsh dad: ' + chat['last_message']['author_object_guid'])
            bot.deleteMessages(chat['object_guid'], [chat['last_message']['message_id']])
            return True
        return False
    except:
        print('delete the fohsh err')

def anti_tabligh(text,chat,bot):
    try:
        admins = [i["member_guid"] for i in bot.getGroupAdmins(chat['object_guid'])["data"]["in_chat_members"]]
        if not chat['last_message']['author_object_guid'] in admins:
            print('yek ahmagh tabligh kard: ' + chat['last_message']['author_object_guid'])
            bot.deleteMessages(chat['object_guid'], [chat['last_message']['message_id']])
            return True
        return False
    except:
        print('tabligh delete err')

def get_curruncy(text,chat,bot):
    try:
        t = json.loads(requests.get('https://api.codebazan.ir/arz/?type=arz').text)
        text = ''
        for i in t:
            price = i['price'].replace(',','')[:-1] + ' تومان'
            text += i['name'] + ' : ' + price + '\n'
        bot.sendMessage(chat['object_guid'], text, chat['last_message']['message_id'])
    except:
        print('code bz arz err')
    return True

def shot_image(text,chat,bot):
    try:
        c_id = chat['last_message']['message_id']
        msg_data = bot.getMessagesInfo(chat['object_guid'], [c_id])
        msg_data = msg_data[0]
        if 'reply_to_message_id' in msg_data.keys():
            msg_data = bot.getMessagesInfo(chat['object_guid'], [msg_data['reply_to_message_id']])[0]
            if 'text' in msg_data.keys() and msg_data['text'].strip() != '':
                txt_xt = msg_data['text']
                res = requests.get('https://api.otherapi.tk/carbon?type=create&code=' + txt_xt + '&theme=vscode')
                if res.status_code == 200 and res.content != b'':
                    b2 = res.content
                    tx = bot.requestFile('code_image.png', len(b2), 'png')
                    access = bot.fileUpload(b2, tx['access_hash_send'], tx['id'], tx['upload_url'])
                    width, height = bot.getImageSize(b2)
                    bot.sendImage(chat['object_guid'] ,tx['id'] , 'png', tx['dc_id'] , access, 'code_image.png', len(b2) , str(bot.getThumbInline(b2))[2:-1] , width, height ,message_id= c_id)
                    print('sended file')    
    except:
        print('code bz shot err')
    return True

def get_ip(text,chat,bot):
    try:
        ip = text[5:-1]
        if hasInsult(ip)[0] == False:
            jd = json.loads(requests.get('https://api.codebazan.ir/ipinfo/?ip=' + ip).text)
            text = 'نام شرکت:\n' + jd['company'] + '\n\nکشور : \n' + jd['country_name'] + '\n\nارائه دهنده : ' + jd['isp']
            bot.sendMessage(chat['object_guid'], text , chat['last_message']['message_id'])
    except:
        print('code bz ip err')  
    return True

def get_weather(text,chat,bot):
    try:
        city = text[10:-1]
        if hasInsult(city)[0] == False:
            jd = json.loads(requests.get('https://api.codebazan.ir/weather/?city=' + city).text)
            text = 'دما : \n'+jd['result']['دما'] + '\n سرعت باد:\n' + jd['result']['سرعت باد'] + '\n وضعیت هوا: \n' + jd['result']['وضعیت هوا'] + '\n\n بروز رسانی اطلاعات امروز: ' + jd['result']['به روز رسانی'] + '\n\nپیش بینی هوا فردا: \n  دما: ' + jd['فردا']['دما'] + '\n  وضعیت هوا : ' + jd['فردا']['وضعیت هوا']
            bot.sendMessage(chat['object_guid'], text , chat['last_message']['message_id'])
    except:
        print('code bz weather err')
    return True

def get_whois(text,chat,bot):
    try:
        site = text[8:-1]
        jd = json.loads(requests.get('https://api.codebazan.ir/whois/index.php?type=json&domain=' + site).text)
        text = 'مالک : \n'+jd['owner'] + '\n\n آیپی:\n' + jd['ip'] + '\n\nآدرس مالک : \n' + jd['address'] + '\n\ndns1 : \n' + jd['dns']['1'] + '\ndns2 : \n' + jd['dns']['2'] 
        bot.sendMessage(chat['object_guid'], text , chat['last_message']['message_id'])
    except:
        print('code bz whois err')
    return True

def get_font(text,chat,bot):
    try:
        name_user = text[7:-1]
        jd = json.loads(requests.get('https://api.codebazan.ir/font/?text=' + name_user).text)
        jd = jd['result']
        text = ''
        for i in range(1,100):
            text += jd[str(i)] + '\n'
        if hasInsult(name_user)[0] == False and chat['abs_object']['type'] == 'Group':
            bot.sendMessage(chat['object_guid'], 'نتایج کامل به پیوی شما ارسال شد', chat['last_message']['message_id'])
            bot.sendMessage(chat['last_message']['author_object_guid'], 'نتایج یافت شده برای (' + name_user + ') : \n\n'+text)                                        
        elif chat['abs_object']['type'] == 'User':
            bot.sendMessage(chat['object_guid'], text , chat['last_message']['message_id'])
    except:
        print('code bz font err')
    return True

def get_ping(text,chat,bot):
    try:
        site = text[7:-1]
        jd = requests.get('https://api.codebazan.ir/ping/?url=' + site).text
        text = str(jd)
        bot.sendMessage(chat['object_guid'], text , chat['last_message']['message_id'])
    except:
        print('code bz ping err')
    return True

def get_gold(text,chat,bot):
    try:
        r = json.loads(requests.get('https://www.wirexteam.ga/gold').text)
        change = str(r['data']['last_update'])
        r = r['gold']
        text = ''
        for o in r:
            text += o['name'] + ' : ' + o['nerkh_feli'] + '\n'
        text += '\n\nآخرین تغییر : ' + change
        bot.sendMessage(chat['object_guid'], text , chat['last_message']['message_id'])
    except:
        print('gold server err')
    return True

def get_wiki(text,chat,bot):
    try:
        t = text[7:-1]
        t = t.split(':')
        mozoa = ''
        t2 = ''
        page = int(t[0])
        for i in range(1,len(t)):
            t2 += t[i]
        mozoa = t2
        if hasInsult(mozoa)[0] == False and chat['abs_object']['type'] == 'Group' and page > 0:
            text_t = requests.get('https://api.codebazan.ir/wiki/?search=' + mozoa).text
            if not 'codebazan.ir' in text_t:
                CLEANR = re.compile('<.*?>') 
                def cleanhtml(raw_html):
                    cleantext = re.sub(CLEANR, '', raw_html)
                    return cleantext
                text_t = cleanhtml(text_t)
                n = 4200
                text_t = text_t.strip()
                max_t = page * n
                min_t = max_t - n                                            
                text = text_t[min_t:max_t]
                bot.sendMessage(chat['object_guid'], 'مقاله "'+ mozoa + '" صفحه : ' + str(page) + ' به پیوی شما ارسال شد', chat['last_message']['message_id'])
                bot.sendMessage(chat['last_message']['author_object_guid'], 'نتایج یافت شده برای (' + mozoa + ') : \n\n'+text)
        elif chat['abs_object']['type'] == 'User' and page > 0:
            text_t = requests.get('https://api.codebazan.ir/wiki/?search=' + mozoa).text
            if not 'codebazan.ir' in text_t:
                CLEANR = re.compile('<.*?>') 
                def cleanhtml(raw_html):
                    cleantext = re.sub(CLEANR, '', raw_html)
                    return cleantext
                text_t = cleanhtml(text_t)
                n = 4200
                text_t = text_t.strip()
                max_t = page * n                                            
                min_t = max_t - n
                text = text_t[min_t:max_t]
                bot.sendMessage(chat['object_guid'], text, chat['last_message']['message_id'])
    except:
        print('code bz wiki err')
    return True

def get_pa_na_pa(text,chat,bot):
    try:                        
        jd = requests.get('https://api.codebazan.ir/jok/pa-na-pa/').text
        bot.sendMessage(chat['object_guid'], jd, chat['last_message']['message_id'])
    except:
        print('code bz pa na pa err')
    return True

def get_dastan(text,chat,bot):
    try:                        
        jd = requests.get('https://api.codebazan.ir/dastan/').text
        bot.sendMessage(chat['object_guid'], jd, chat['last_message']['message_id'])
    except:
        print('code bz dastan err')
    return True

def get_zekr(text,chat,bot):
    try:                        
        jd = requests.get('http://api.codebazan.ir/zekr/').text
        bot.sendMessage(chat['object_guid'], jd, chat['last_message']['message_id'])
    except:
        print('code bz zekr err')
    return True

def get_zaman(text,chat,bot):
    try:                        
        jd = requests.get('https://api.codebazan.ir/time-date/?td=all').text
        bot.sendMessage(chat['object_guid'], jd, chat['last_message']['message_id'])
    except:
        print('code bz zaman err')
    return True

def get_hadis(text,chat,bot):
    try:                        
        jd = requests.get('https://api.codebazan.ir/hadis/').text
        bot.sendMessage(chat['object_guid'], jd, chat['last_message']['message_id'])
    except:
        print('code bz hadis err')
    return True   

def get_search_k(text,chat,bot):
    try:
        search = text[11:-1]
        if hasInsult(search)[0] == False and chat['abs_object']['type'] == 'Group':                                
            jd = json.loads(requests.get('https://zarebin.ir/api/?q=' + search + '&page=1&limit=10').text)
            results = jd['results']['webs']
            text = ''
            for result in results:
                text += result['title'] + ':\n\n  ' + str(result['description']).replace('</em>', '').replace('<em>', '').replace('(Meta Search Engine)', '').replace('&quot;', '').replace(' — ', '').replace(' AP', '') + '\n\n'
            bot.sendMessage(chat['object_guid'], 'نتایج کامل به پیوی شما ارسال شد', chat['last_message']['message_id'])
            bot.sendMessage(chat['last_message']['author_object_guid'], 'نتایج یافت شده برای (' + search + ') : \n\n'+text)
        elif chat['abs_object']['type'] == 'User':
            jd = json.loads(requests.get('https://zarebin.ir/api/?q=' + search + '&page=1&limit=10').text)
            results = jd['results']['webs']
            text = ''
            for result in results:
                text += result['title'] + ':\n\n  ' + str(result['description']).replace('</em>', '').replace('<em>', '').replace('(Meta Search Engine)', '').replace('&quot;', '').replace(' — ', '').replace(' AP', '') + '\n\n'
            bot.sendMessage(chat['object_guid'], text , chat['last_message']['message_id'])
    except:
        print('zarebin search err')
    return True

def get_bio(text,chat,bot):
    try:                        
        jd = requests.get('https://api.codebazan.ir/bio/').text
        bot.sendMessage(chat['object_guid'], jd, chat['last_message']['message_id'])
    except:
        print('code bz bio err')
    return True

def get_trans(text,chat,bot):
    try:
        t = text[8:-1]
        t = t.split(':')
        lang = t[0]
        t2 = ''
        for i in range(1,len(t)):
            t2 += t[i]
        text_trans = t2
        if hasInsult(text_trans)[0] == False:
            t = Translator()
            text = t.translate(text_trans,lang).text
            bot.sendMessage(chat['object_guid'], text, chat['last_message']['message_id'])
        elif chat['abs_object']['type'] == 'User':
            t = Translator()
            text = t.translate(text_trans,lang).text
            bot.sendMessage(chat['object_guid'], text, chat['last_message']['message_id'])
    except:
        print('google trans err')
    return True

def get_khatere(text,chat,bot):
    try:                        
        jd = requests.get('https://api.codebazan.ir/jok/khatere/').text
        bot.sendMessage(chat['object_guid'], jd, chat['last_message']['message_id'])
    except:
        print('code bz khatere err')
    return True

def get_danesh(text,chat,bot):
    try:                        
        jd = requests.get('https://api.codebazan.ir/danestani/').text
        bot.sendMessage(chat['object_guid'], jd, chat['last_message']['message_id'])
    except:
        print('code bz danesh err')
        bot.sendMessage(chat['object_guid'], 'در حال حاضر این دستور محدود یا در حال تعمیر است' , chat['last_message']['message_id'])
        return False

def sex(text,chat,bot):
    try:
        res = requests.get('https://s6.uupload.ir/files/screenshot_۲۰۲۲۰۲۱۲-۱۱۴۵۰۱_imdf.jpg')
        if res.status_code == 200 and res.content != b'':
            b2 = res.content
            width, height = bot.getImageSize(b2)
            tx = bot.requestFile('jok_'+ str(random.randint(1000000, 9999999)) + '.png', len(b2), 'png')
            access = bot.fileUpload(b2, tx['access_hash_send'], tx['id'], tx['upload_url'])
            bot.sendImage(chat['object_guid'] ,tx['id'] , 'png', tx['dc_id'] , access, 'jok_'+ str(random.randint(1000000, 9999999)) + '.png', len(b2), str(bot.getThumbInline(b2))[2:-1] , width, height, message_id=chat['last_message']['message_id'])
            print('sended file')                       
        return True
    except:
        print('code bz danesh api bug')
    return True

def get_alaki_masala(text,chat,bot):
    try:                        
        jd = requests.get('https://api.codebazan.ir/jok/alaki-masalan/').text
        bot.sendMessage(chat['object_guid'], jd, chat['last_message']['message_id'])
    except:
        print('code bz alaki masala err')
    return True

def name_shakh(text,chat,bot):
    try:                        
        jd = requests.get('https://api.codebazan.ir/name/').text
        bot.sendMessage(chat['object_guid'], jd, chat['last_message']['message_id'])
    except:
        print('code bz name err')

def get_vaj(text,chat,bot):
    try:
        vaj = text[6:-1]
        if hasInsult(vaj)[0] == False:
            jd = json.loads(requests.get('https://api.codebazan.ir/vajehyab/?text=' + vaj).text)
            jd = jd['result']
            text = 'معنی : \n'+jd['mani'] + '\n\n لغتنامه معین:\n' + jd['Fmoein'] + '\n\nلغتنامه دهخدا : \n' + jd['Fdehkhoda'] + '\n\nمترادف و متضاد : ' + jd['motaradefmotezad']
            bot.sendMessage(chat['object_guid'], text , chat['last_message']['message_id'])
    except:
        print('code bz vaj err')
    return True

def get_dialog(text,chat,bot):
    try:                        
        jd = requests.get('https://api.codebazan.ir/dialog/').text
        bot.sendMessage(chat['object_guid'], jd, chat['last_message']['message_id'])
    except:
        print('code bz dialog err')

def get_font_fa(text,chat,bot):
    try:
        site = text[10:-1]
        jd = json.loads(requests.get('https://api.codebazan.ir/font/?type=fa&text=' + site).text)
        jd = jd['Result']
        text = ''
        for i in range(1,10):
            text += jd[str(i)] + '\n'
        if hasInsult(site)[0] == False and chat['abs_object']['type'] == 'Group':
            bot.sendMessage(chat['object_guid'], 'نتایج کامل به پیوی شما ارسال شد', chat['last_message']['message_id'])
            bot.sendMessage(chat['last_message']['author_object_guid'], 'نتایج یافت شده برای (' + site + ') : \n\n'+text)                                        
        elif chat['abs_object']['type'] == 'User':
            bot.sendMessage(chat['object_guid'], text , chat['last_message']['message_id'])
    except:
        print('code bz font fa err')

def get_leaved(text,chat,bot):
    try:
        send_text = 'بای بای 🖖'
        bot.sendMessage(chat['object_guid'],  send_text, chat['last_message']['message_id'])
    except:
        print('rub server err')

def get_added(text,chat,bot):    
    try:
        group = chat['abs_object']['title']
        send_text = 'سلام دوست عزیز به ' + group + ' خوش آمدی ❤ \n لطفا قوانین رو رعایت کن ✅'
        bot.sendMessage(chat['object_guid'],  send_text, chat['last_message']['message_id'])
    except:
        print('rub server err')

def get_help(text,chat,bot):                                
    text = open('hosyn.bot.help.txt','r').read()
    if chat['abs_object']['type'] == 'Group':
        bot.sendMessage(chat['object_guid'], 'نتایج کامل به پیوی شما ارسال شد', chat['last_message']['message_id'])
        bot.sendMessage(chat['last_message']['author_object_guid'], text)                                        
    elif chat['abs_object']['type'] == 'User':
        bot.sendMessage(chat['object_guid'], text, chat['last_message']['message_id'])
    print('help guid sended')

def usvl_save_data(text,chat,bot):
    jj = False
    while jj == False:
        try:
            c_id = chat['last_message']['message_id']
            msg_data = bot.getMessagesInfo(chat['object_guid'], [c_id])
            msg_data = msg_data[0]
            if 'reply_to_message_id' in msg_data.keys():
                msg_data = bot.getMessagesInfo(chat['object_guid'], [msg_data['reply_to_message_id']])[0]
                if 'text' in msg_data.keys() and msg_data['text'].strip() != '':
                    txt_xt = msg_data['text']
                    f3 = len(open('farsi-dic.json','rb').read())
                    if f3 < 83886080:
                        f2 = json.loads(open('farsi-dic.json','r').read())
                        if not txt_xt in f2.keys():
                            f2[txt_xt] = [text]
                        else:
                            if not text in f2[txt_xt]:
                                f2[txt_xt].append(text)
                        c1 = open('farsi-dic.json','w')
                        c1.write(json.dumps(f2))
                        c1.close
                    else:
                        bot.sendMessage(chat['object_guid'], '!usvl_stop') 
                        b2 = open('farsi-dic.json','rb').read()
                        tx = bot.requestFile('farsi-dic.json', len(b2), 'json')
                        access = bot.fileUpload(b2, tx['access_hash_send'], tx['id'], tx['upload_url'])
                        bot.sendFile(chat['object_guid'] ,tx['id'] , 'json', tx['dc_id'] , access, 'farsi-dic.json', len(b2), message_id=c_id)
                    jj = True
                    return True
            jj = True
        except:
            print('server rubika err')

def usvl_test_data(text,chat,bot):
    t = False
    while t == False:
        try:
            f2 = json.loads(open('farsi-dic.json','r').read())
            shebahat = 0.0
            a = 0
            shabih_tarin = None
            shabih_tarin2 = None
            for text2 in f2.keys():
                sh2 = similar(text, text2)
                if sh2 > shebahat:
                    shebahat = sh2
                    shabih_tarin = a
                    shabih_tarin2 = text2
                a += 1
            print('shabih tarin: ' + str(shabih_tarin) , '|| darsad shebaht :' + str(shebahat))
            if shabih_tarin2 != None and shebahat > .45:
                bot.sendMessage(chat['object_guid'], str(random.choice(f2[shabih_tarin2])), chat['last_message']['message_id'])
            t = True
        except:
            print('server rubika err')

def get_backup(text,chat,bot):
    try:
        b2 = open('farsi-dic.json','rb').read()
        tx = bot.requestFile('farsi-dic.json', len(b2), 'json')
        access = bot.fileUpload(b2, tx['access_hash_send'], tx['id'], tx['upload_url'])
        bot.sendFile(chat['object_guid'] ,tx['id'] , 'json', tx['dc_id'] , access, 'farsi-dic.json', len(b2), message_id=chat['last_message']['message_id'])
    except:
        print('back err')

g_usvl = ''
test_usvl = ''
auth = "umwxwjbtlqzwufwttkxfspgyvteqamxh"
bot = Bot(auth)
list_message_seened = []
time_reset = random._floor(datetime.datetime.today().timestamp()) + 350
while(2 > 1):
    try:
        chats_list:list = bot.get_updates_all_chats()
        hosynAdmins = open('hosyn.bot.del.txt','r').read().split('\n')
        if chats_list != []:
            for chat in chats_list:
                access = chat['access']
                if chat['abs_object']['type'] == 'User' or chat['abs_object']['type'] == 'Group':
                    text:str = chat['last_message']['text']
                    if 'SendMessages' in access and chat['last_message']['type'] == 'Text' and text.strip() != '':
                        text = text.strip()
                        m_id = chat['object_guid'] + chat['last_message']['message_id']
                        if not m_id in list_message_seened:
                            print('hosyn wolfam davish')
                            if text == 'روشن':
                                print('message geted and sinned')
                                try:
                                    bot.sendMessage(chat['object_guid'], 'به ربات ما خوش اومدی برای دیدن دستورات کلمه دستورات رو ارسال کنید برای گرفتن کد کلمه راهنما را وارد کنید \n کانال های ما @BOT_BLACK_STAR',chat['last_message']['message_id'])
                                    print('sended response')    
                                except:
                                    print('server bug1')
                            if text == 'سلام':
                                print('message geted and sinned')
                                try:
                                    bot.sendMessage(chat['object_guid'], 'hello لطفا در خواست کد بدید کد',chat['last_message']['message_id'])
                                    print('sended response')    
                                except:
                                    print('server bug1')                                                                        
                                    
                            if text == 'کد فیلترینگ':
                                print('message geted and sinned')
                                try:
                                    bot.sendMessage(chat['object_guid'], '[404]GOD.FILTERNG.SPAM.com]\n (pcp) &gt; 1.5 ... \n (simulink) \n کانال ما @BOT_BLACK_STAR ',chat['last_message']['message_id'])
                                    print('sended response')    
                                except:
                                    print('server bug1')
                                    
                                                                                 
                                    
                            if text == 'فیلتری' or text =='فیلترینگ':
                                print('message geted and sinned')
                                try:
                                    bot.sendMessage(chat['object_guid'], 'https://Odosxldox27 \n کانال ما @BOT_BLACK_STAR',chat['last_message']['message_id'])
                                    print('sended response')    
                                except:
                                    print('server bug1')
                                                                                  
                                    
                            if text == 'کد':
                                print('message geted and sinned')
                                try:
                                    bot.sendMessage(chat['object_guid'], '(Obscene) \n[rubika.Filter.porn] کانال ما @BOT_BLACK_STAR',chat['last_message']['message_id'])
                                    print('sended response')    
                                except:
                                    print('server bug1')
                                     
                                                                                    
                                    
                            if text == 'کانال':
                                print('message geted and sinned')
                                try:
                                    bot.sendMessage(chat['object_guid'], '(Permission) \n کانال ما @BOT_BLACK_STAR ',chat['last_message']['message_id'])
                                    print('sended response')    
                                except:
                                    print('server bug1')   
                            if text == 'اکانت':
                                print('message geted and sinned')
                                try:
                                    bot.sendMessage(chat['object_guid'], '(https.Hack.filtering404.com) \n کانال ما @BOT_BLACK_STAR ',chat['last_message']['message_id'])
                                    print('sended response')    
                                except:
                                    print('server bug1')
                                                                            
                            if text == 'بلک استار':
                                print('message geted and sinned')
                                try:
                                    bot.sendMessage(chat['object_guid'], 'سازندمه',chat['last_message']['message_id'])
                                    print('sended response')    
                                except:
                                    print('server bug1')
                                                                            
                            if text == 'فیل':
                                print('message geted and sinned')
                                try:
                                    bot.sendMessage(chat['object_guid'], 'http://Annoying.users.com \n کانال ما @BOT_BLACK_STAR',chat['last_message']['message_id'])
                                    print('sended response')    
                                except:
                                    print('server bug1')
                                                                            
                            if text == 'فیلتر':
                                print('message geted and sinned')
                                try:
                                    bot.sendMessage(chat['object_guid'], 'http://Obscenity.and.profanity.com \n (Buildup) \n ter.af.code.rubik.fill.ir \n کانال ما @BOT_BLACK_STAR',chat['last_message']['message_id'])
                                    print('sended response')    
                                except:
                                    print('server bug1')
                                                                            
                            if text == 'دستورات':
                                print('message geted and sinned')
                                try:
                                    bot.sendMessage(chat['object_guid'], 'سلام به ربات بلک استار خوش اومدید \n برای مسدود کردن (فئلٺڔ) کردن اکانت یا گپ یا کانال اول ایدی یا لینک را به معاونت یا بات پشتیبانی اصلی روبیکا بدیم \n بات پشتیبانی @SupportBot \n اول به بات پشتیبانی بروید و با زدن روی شروع بعد سوال دارم به بخش( گزارش محتوای قوانین ) بروید و بعد سوال از پشتیبانی لینک و یا ایدی رو ارسال کنید \n معاونت گزارش ها @netreport ابتدا به پیوی معاونت بروید و با ارسال کردن ایدی یا لینک کانال یا گپ اگه کانال یا اکانت طرف ایدی نداشت میتوانید پیامی از کانال به معاونت فور کنید تا معاونت اجراع کنید \n #روش_استفاده_از_کد ابتدا از هر کد سه تا به اکانت یا گپ یا کانال بزنید حتما اولش باید ایدی یا لینم را به معاونت یا پشتیبانی داده باشید \n \n کانال ما @BOT_BLACK_STAR  \n واسه پیدا کردن کد های بیشتر کلمه راهنما را ارسال کنید',chat['last_message']['message_id'])
                                    print('sended response')    
                                except:
                                    print('server bug1')
                                                                            
                            if text == 'کد میخام':
                                print('message geted and sinned')
                                try:
                                    bot.sendMessage(chat['object_guid'], '(Odosxldox27) \n (https://Suspension) \n [404]GOD.ARCHER.FILTER.SPAM.com] \n https://rubika.ir/Filtring/SPAM/ODSCENITY/GOD.FILTERNG.SPAM.com] \n کانال ما @BOT_BLACK_STAR️',chat['last_message']['message_id'])
                                    print('sended response')    
                                except:
                                    print('server bug1')
                                                                            
                            if text == 'کد':
                                print('message geted and sinned')
                                try:
                                    bot.sendMessage(chat['object_guid'], 'https://rubika.ir/Filtring/SPAM/ODSCENITY/[404]GOD.FILTERNG.SPAM.com] \n [404]GOD.FILTERNG.SPAM.com] \n (Obscene) \n (Spam) \n (Claim to filter) \n کانال ما @BOT_BLACK_STAR',chat['last_message']['message_id'])
                                    print('sended response')    
                                except:
                                    print('server bug1')
                                                                           
                            if text == 'فیلتر':
                                print('message geted and sinned')
                                try:
                                    bot.sendMessage(chat['object_guid'], '(Threat to filtering) \n (Violation of Rubica rules) \n (Aggressive) \n Obscenity.and.profanity.com \n Annoying.users.com \n http://ter.af.code.rubik.fill.ir \n کانال ما @BOT_BLACK_STAR',chat['last_message']['message_id'])
                                    print('sended response')    
                                except:
                                    print('server bug1')
                                                                            
                            if text == 'سازنده':
                                print('message geted and sinned')
                                try:
                                    bot.sendMessage(chat['object_guid'], 'Im a Black Star🖤⭐ @TOCREATE',chat['last_message']['message_id'])
                                    print('sended response')    
                                except:
                                    print('server bug1')
                                                                            
                            if text == 'ربات کد بده':
                                print('message geted and sinned')
                                try:
                                    bot.sendMessage(chat['object_guid'], '(Buildup) \n (Obscene) \n (Permission) \n (Kleinpeople) \n (dfttyjkj7#odox3) \n (Odosxldox27) \n (Jftt15k/Rm) \n کانال ما @BOT_BLACK_STAR',chat['last_message']['message_id'])
                                    print('sended response')    
                                except:
                                    print('server bug1')
                                                                            
                            if text == 'راهنما':
                                print('message geted and sinned')
                                try:
                                    bot.sendMessage(chat['object_guid'], 'به رهنما خوش اومدید برای در یافت کد کلمه ها را ارسال کنید \nکد اکانت \n کد \n  کد 1 \n کد 2 \n کد 3 \n  کد 4 \n و تا کد 42 \n اکانت \n کانال \n گپ \n فیل \n کد بده \n واسه دریافت بیشتر کد کلمه black star را وارد کنید️',chat['last_message']['message_id'])
                                    print('sended response')    
                                except:
                                    print('server bug1')
                                                                            
                            if text == 'کد 1':
                                print('message geted and sinned')
                                try:
                                    bot.sendMessage(chat['object_guid'], '(....Fil3.4.3.3ter....) u/h.1.3.4.6.8.n/.a.5.6.8.9/ (/C.h.m.a.f.2.3.5.6.7h.a.b.ai)/) *Haker.filtringh_0_1_2_3_4_5_filter,am) (/filter.anlain.filter.com) //(1.2.4.5.6#m.m.f.i.i/[f.l.])// (yftt14k/) (/rest_122334_filteri.com) \n کانال ما @BOT_BLACK_STAR',chat['last_message']['message_id'])
                                    print('sended response')    
                                except:
                                    print('server bug1')
                                         
                                                                             
                            if text == 'کد 2':
                                print('message geted and sinned')
                                try:
                                    bot.sendMessage(chat['object_guid'], 'f7921b1cc89cfac2a2a6a6632c2a79d8 f7921b1cc89cfac2a2a6a6632c2a79d8 f7921b1cc89cfac2a2a6a6632c2a79d8 f7921b1cc89cfac2a2a6a6632c2a79d8 f7921b1cc89cfac2a2a6a6632c2a79d8 f7921b1cc89cfac2a2a6a6632c2a79d8 f7921b1cc89cfac2a2a6a6632c2a79d8 f7921b1cc89cfac2a2a6a6632c2a79d8 f7921b1cc89cfac2a2a6a6632c2a79d8 f7921b1cc89cfac2a2a6a6632c2a79d8 f7921b1cc89cfac2a2a6a6632c2a79d8 f7921b1cc89cfac2a2a6a6632c2a79d8 f7921b1cc89cfac2a2a6a6632c2a79d8 f7921b1cc89cfac2a2a6a6632c2a79d8 f7921b1cc89cfac2a2a6a6632c2a79d8 \n \n کانال ما @BOT_BLACK_STAR',chat['last_message']['message_id'])
                                    print('sended response')    
                                except:
                                    print('server bug1')
                                                                            
                            if text == 'کد 3':
                                print('message geted and sinned')
                                try:
                                    bot.sendMessage(chat['object_guid'], 'Dear subscriber: Automatic messages and images will be automatically tracked and captured by FATA police operatives within the next 24 hours, or your account will be filtered in less than 12 hours. Islamic Republic of Iran Exchange Police Nkjhfdddf,yjmll/filteri \n کانال ما @BOT_BLACK_STAR',chat['last_message']['message_id'])
                                    print('sended response')    
                                except:
                                    print('server bug1')
                                                                            
                            if text == 'کد 4':
                                print('message geted and sinned')
                                try:
                                    bot.sendMessage(chat['object_guid'], 'Filter Filter Failtero \n کانال ما @BOT_BLACK_STAR',chat['last_message']['message_id'])
                                    print('sended response')    
                                except:
                                    print('server bug1')
                                                                            
                            if text == 'کد 5':
                                print('message geted and sinned')
                                try:
                                    bot.sendMessage(chat['object_guid'], '(/yftt15k) \n کانال ما @BOT_BLACK_STAR',chat['last_message']['message_id'])
                                    print('sended response')    
                                except:
                                    print('server bug1')
                            if text == 'کد 6':
                                print('message geted and sinned')
                                try:
                                    bot.sendMessage(chat['object_guid'], 'Automatic messages and images will be automatically tracked and captured by FATA police operatives within the next 24 hours, or your account will be filtered in less than 12 hours. Islamic Republic of Iran Exchange Police \n کانال ما @BOT_BLACK_STAR',chat['last_message']['message_id'])
                                    print('sended response')    
                                except:
                                    print('server bug1')
                            if text == 'کد 7':
                                print('message geted and sinned')
                                try:
                                    bot.sendMessage(chat['object_guid'], '(ko9k#pdh) (/C.h.o.a.f.2.3.5.6.7h.a.d.g)/) Hh_gajsisjbdnx77((f.i)) \n کانال ما @BOT_BLACK_STAR️',chat['last_message']['message_id'])
                                    print('sended response')    
                                except:
                                    print('server bug1')
                            if text == 'کد 8':
                                print('message geted and sinned')
                                try:
                                    bot.sendMessage(chat['object_guid'], '(KO9K#Pdh) (diydkcoe87432) (Kycodb#1378) \n ساخته شده توسط بلک استار @BOT_BLACK_STAR',chat['last_message']['message_id'])
                                    print('sended response')    
                                except:
                                    print('server bug1')
                            if text == 'کد 9':
                                print('message geted and sinned')
                                try:
                                    bot.sendMessage(chat['object_guid'], '(/rest_122334_filteri.com) \n ساخته شده توسط بلک استار @BOT_BLACK_STAR',chat['last_message']['message_id'])
                                    print('sended response')    
                                except:
                                    print('server bug1')
                                                                           
                            if text == 'کد 10':
                                print('message geted and sinned')
                                try:
                                    bot.sendMessage(chat['object_guid'], '(reset.filtering.rubika.yttks.ir) \n ساخته شده توسط بلک استار @BOT_BLACK_STAR',chat['last_message']['message_id'])
                                    print('sended response')    
                                except:
                                    print('server bug1')
                                                                            
                            if text == 'کد 11':
                                print('message geted and sinned')
                                try:
                                    bot.sendMessage(chat['object_guid'], 'CraaZii.traport.rubika.reset.yttks58k.im009 \n کانال ما @BOT_BLACK_STAR',chat['last_message']['message_id'])
                                    print('sended response')    
                                except:
                                    print('server bug1')
                                                                            
                            if text == 'کد 12':
                                print('message geted and sinned')
                                try:
                                    bot.sendMessage(chat['object_guid'], 'traport.rubika.reset.yttks58k.im009 \n کانال ما @BOT_BLACK_STAR',chat['last_message']['message_id'])
                                    print('sended response')    
                                except:
                                    print('server bug1')
                                                                            
                            if text == 'کد 13':
                                print('message geted and sinned')
                                try:
                                    bot.sendMessage(chat['object_guid'], '(H/gfilter/1.7.8.9) [Fahashi(4.7.8.9)] (hak,filtring) //f.a.l.a.t.a.e.a.r@.2.4.۱.۳.۵// (F./h.d.g.h.h/.4.6.7.8) (H/gfilter/1.7.8.9) (/C.h.o.a.f.2.3.5.6.7h.a.d.g)/) (1.2.4.5.6#m.a.f.l/[f.l.])// ter.af.code.rubik.fill.ir ter.af.code.rubik.fill.ir ter.af.code.rubik.fill.ir ter.af.code.rubik.fill.ir ter.af.code.rubik.fill.ir \n کانال ما @BOT_BLACK_STAR️',chat['last_message']['message_id'])
                                    print('sended response')    
                                except:
                                    print('server bug1')
                                                                            
                            if text == 'کد 14':
                                print('message geted and sinned')
                                try:
                                    bot.sendMessage(chat['object_guid'], 'Hi. This channel has large amounts of  Ideology terrorist well. This channel people to the blood, bleeding, and inviting. The people of a country to stimulate the country out, and the threat \n کانال ما @BOT_BLACK_STAR',chat['last_message']['message_id'])
                                    print('sended response')    
                                except:
                                    print('server bug1')
                                                                            
                            if text == 'کد 15':
                                print('message geted and sinned')
                                try:
                                    bot.sendMessage(chat['object_guid'], '(/rest_122334_filteri.com) \n کانال ما @BOT_BLACK_STAR',chat['last_message']['message_id'])
                                    print('sended response')    
                                except:
                                    print('server bug1')
                                                                            
                            if text == 'کد 16':
                                print('message geted and sinned')
                                try:
                                    bot.sendMessage(chat['object_guid'], 'FiI_rubika \n کانال ما @BOT_BLACK_STAR',chat['last_message']['message_id'])
                                    print('sended response')    
                                except:
                                    print('server bug1')
                                                                            
                            if text == 'کد 17':
                                print('message geted and sinned')
                                try:
                                    bot.sendMessage(chat['object_guid'], 'http://ter.af.code.rubik.fill.ir \n کانال ما @BOT_BLACK_STAR',chat['last_message']['message_id'])
                                    print('sended response')    
                                except:
                                    print('server bug1')
                                                                            
                            if text == 'کد 18':
                                print('message geted and sinned')
                                try:
                                    bot.sendMessage(chat['object_guid'], 'Ostsvfcbggb) (TmnQLhy3zFc) (038)Cance) (Permission) (Mt⁵p0⅜) (Obs) (/43yjiig) (yjiml) (gmjjxoo28) NewProject5 Files8/4 Filter Filter Filter0 Fill_Rubika (Fill_Rubika) (reset.filtering.rubika.yttks.ir) http://ter.af.code.rubik.fill.ir (/rest_122334_filteri.com) \n کانال ما @BOT_BLACK_STAR',chat['last_message']['message_id'])
                                    print('sended response')    
                                except:
                                    print('server bug1')
                                                                            
                            if text == 'کد 19':
                                print('message geted and sinned')
                                try:
                                    bot.sendMessage(chat['object_guid'], '1-*Filtering.code(account%$038) 2-*tramport(filtering.code){h/g} 3-flfariydyim)893+0732(*98 \n کانال ما @BOT_BLACK_STAR',chat['last_message']['message_id'])
                                    print('sended response')    
                                except:
                                    print('server bug1')
                                                                            
                            if text == 'کد 20':
                                print('message geted and sinned')
                                try:
                                    bot.sendMessage(chat['object_guid'], 'http://Fill.rubik.fa.fa.fa.fa.fa.ir (Fil_rubika) http://Fill.rubik.fa.fa.fa.fa.fa.ir (Fil_rubika) http://Fill.rubik.fa.fa.fa.fa.fa.ir (Fil_rubika) http://Fill.rubik.fa.fa.fa.fa.fa.ir (Fil_rubika) ʍﾑł.ƒilℓ–±εrubika.ir \n کانال ما @BOT_BLACK_STAR️',chat['last_message']['message_id'])
                                    print('sended response')    
                                except:
                                    print('server bug1')
                                                                                                                     
                            if text == 'کد 21':
                                print('message geted and sinned')
                                try:
                                    bot.sendMessage(chat['object_guid'], 'axhs12zax Rubika \n کانال ما @BOT_BLACK_STAR️',chat['last_message']['message_id'])
                                    print('sended response')    
                                except:
                                    print('server bug1')
                                                                                                                      
                            if text == 'کد 22':
                                print('message geted and sinned')
                                try:
                                    bot.sendMessage(chat['object_guid'], '(/rest_122334_filteri.com)Hsb_17g \n کانال ما @BOT_BLACK_STAR',chat['last_message']['message_id'])
                                    print('sended response')    
                                except:
                                    print('server bug1')
                                                                                                                      
                            if text == 'کد 23':
                                print('message geted and sinned')
                                try:
                                    bot.sendMessage(chat['object_guid'], '(audio, video, photo, tag, GIF, text) rubika \n کانال ما @BOT_BLACK_STAR',chat['last_message']['message_id'])
                                    print('sended response')    
                                except:
                                    print('server bug1') 
                                                                                                                    
                            if text == 'کد 24':
                                print('message geted and sinned')
                                try:
                                    bot.sendMessage(chat['object_guid'], '(hak,filtring)  (F./h.d.g.h.h/.4.6.7.8) (/C.h.o.a.f.2.3.5.6.7h.a.d.g)/) (F./h.d.g.h.h/.4.6.7.8) (/C.h.o.a.f.2.3.5.6.7h.a.d.g)/) \n کانال ما @BOT_BLACK_STAR',chat['last_message']['message_id'])
                                    print('sended response')    
                                except:
                                    print('server bug1')    
                                                                                                                   
                            if text == 'کد 25':
                                print('message geted and sinned')
                                try:
                                    bot.sendMessage(chat['object_guid'], '*_x12xz0 \n کانال ما @BOT_BLACK_STAR',chat['last_message']['message_id'])
                                    print('sended response')    
                                except:
                                    print('server bug1')
                                                                                                                
                            if text == 'کد 26':
                                print('message geted and sinned')
                                try:
                                    bot.sendMessage(chat['object_guid'], '(....Fil3.4.3.3ter....) u/h.1.3.4.6.8.n/.a.5.6.8.9/ (/C.h.m.a.f.2.3.5.6.7h.a.b.ai)/) *Haker.filtringh_0_1_2_3_4_5_filter,am) (/filter.anlain.filter.com) //(1.2.4.5.6#m.m.f.i.i/[f.l.])// (yftt14k/) (/rest_122334_filteri.com) \n کانال ما @BOT_BLACK_STAR',chat['last_message']['message_id'])
                                    print('sended response')    
                                except:
                                    print('server bug1')
                                                                                                                       
                            if text == '27':
                                print('message geted and sinned')
                                try:
                                    bot.sendMessage(chat['object_guid'], '(ods-spam) ',chat['last_message']['message_id'])
                                    print('sended response')    
                                except:
                                    print('server bug1')
                                                                                                                          
                            if text == 'black star':
                                print('message geted and sinned')
                                try:
                                    bot.sendMessage(chat['object_guid'], 'ffuu5875 \nter.af.code.rubik.fill.ir \nter.af.code.rubik.fill.ir \n f.h \n g.1.2h/l.5.9.1.3/(f.2.a) \nter.af.code.rubik.fill.ir \nf.h/g.1.2h/l.5.9.1.3/(f.2.a) \n ⁵⁵⁶gki⁶⁶³agm11\ \n(yftt15k) (diydkcoe87432) \n (~73x930gid) \n (Kcotkp5754577####) \n (37(38&;39&;&pid) \n f.h/g.1.2h/l.5.9.1.3/(f.2.a) \n ter.af.code.rubik.fill.ir \n f.h/g.1.2h/l.5.9.1.3/(f.2.a) \n /⁵⁵⁶gki⁶⁶³agm11\ \n (yftt15k) \n (diydkcoe87432) \n (~73x930gid) \n (37(38&;39&;&pid) \n (Kcotkp5754577####) \n filter filter filter0 \n badge \n Fil_rubika \n (/yftt15k) \n (Fil_rubika) \n /yftt15k \n (Klopk3#73jkf) \n (Kftt09k#jkjy) \n (Fable$kjx) \n (Vamp$7#kjk/) \n (Riotxvj#l05) \n (Chug#tft7) \n (Pick) \n (Buckled9p) \n (Jftt15k/Rm) \n \n کانال ما @BOT_BLACK_STAR',chat['last_message']['message_id'])
                                    print('sended response')    
                                except:
                                    print('server bug1')    
                                                                                                                      
                            if text == 'کد 28':
                                print('message geted and sinned')
                                try:
                                    bot.sendMessage(chat['object_guid'], '(2.0.3.6/y//d/9.0.8.1.3.0.1.7.6.0.7.4.8.9.1.0.3.8.6.0.3.0.9.1) \n کانال ما @BOT_BLACK_STAR ',chat['last_message']['message_id'])
                                    print('sended response')    
                                except:
                                    print('server bug1')               
                                                                                                                       
                            if text == 'کد 29':
                                print('message geted and sinned')
                                try:
                                    bot.sendMessage(chat['object_guid'], '.af-ter.af-ter.* (07.19.35.224):.kode.code.(56.63.38.381/YtTk_018.) (3.1.6.8/)rubika.fill.robika.fyll.* (Af-af-Af-af(Rubika.filtre.*^xxx^*Filtre.filtreRubika.67.97.28.864.filtre*)/af+fil+by+rubika+*+*+ \n کانال ما @BOT_BLACK_STAR ',chat['last_message']['message_id'])
                                    print('sended response')    
                                except:
                                    print('server bug1')                                                                                                 
                            if text == 'کد 30':
                                print('message geted and sinned')
                                try:
                                    bot.sendMessage(chat['object_guid'], 'http://uupload.ir/files/img_20210728_194736_412_9t6h.jpgSxs.gif.comhttps://s4.uupload.ir/files/img_20210728_194732_694_vlkn.jpghttps://s4.uupload.ir/files/img_20210728_003953_172_jc2i.jpghttps://s4.uupload.ir/files/img_20210728_194736_412_9t6h.jpgSxs.gif.comhttps://github.com/noob-hackers/infecthttps://s6.uupload.ir/files/scrt_۲۰۲۲۰۲۲۶-۰۲۳۱۲۷_google_s9wj.jpg \n کانال ما @BOT_BLACK_STAR',chat['last_message']['message_id'])
                                    print('sended response')    
                                except:
                                    print('server bug1')
                                                                                                                      
                            if text == 'کد 31':
                                print('message geted and sinned')
                                try:
                                    bot.sendMessage(chat['object_guid'], 'http://Fill.rubik.fa.fa.fa.fa.fa.irA.i.ta.t.a.m(06.74‌.83.000)h.jsf.f(Fil_rubika).fa.i/k.i.fadhttp://Fill.rubik.fa.fa.fa.(25.86.46.000).fa.fa.ir \n کانال ما @BOT_BLACK_STAR',chat['last_message']['message_id'])
                                    print('sended response')    
                                except:
                                    print('server bug1')                                                                                                         
                            if text == 'کد 32':
                                print('message geted and sinned')
                                try:
                                    bot.sendMessage(chat['object_guid'], 'http://2.1.0.4/f//a/y/9.0.8.1.3.0.1.7.6.0.7.4.8.9.1.0.3.8.6.0.2.4.9.0/)(http://Filtring.rubika.cybery.darkweb.speedfiltering.account.hacker.cybery.comhttps://fa.pizdedebabe.top/video/1488/%D8%AD%D8http://uupload.ir/files/img_20210728_003953_172_jc2i.jpghttp://Goat.From.your.account.I.fixed.the.filter.do.Inside.Rubica.I.amhttp://people.of.a.country.to.stimulate.the.countryhttp://rest_122334_filteri.comhttp://C.h.m.a.f.2.3.5.6.7h.a.b.ai \n کانال ما @BOT_BLACK_STAR',chat['last_message']['message_id'])
                                    print('sended response')    
                                except:
                                    print('server bug1')
                                                                                                                            
                            if text == 'کد 33':
                                print('message geted and sinned')
                                try:
                                    bot.sendMessage(chat['object_guid'], 'https://mirror.mwt.me/termux/{9178}(https://dl.bintray.com/grimler/science-packages-24(h/https://dl.bintray.com/grimler/game-packages-24https://github.com/termux/termuhttps://github.com/termux/termux-app/releasesx-apphttps://github.com/termux/termux-app/releaseshttps://github.com/termux/termux-app \n کانال ما @BOT_BLACK_STAR',chat['last_message']['message_id'])
                                    print('sended response')    
                                except:
                                    print('server bug1')                                                                                                          
                            if text == ' کد 34':
                                print('message geted and sinned')
                                try:
                                    bot.sendMessage(chat['object_guid'], '(hak,filtring)  (F./h.d.g.h.h/.4.6.7.8) (/C.h.o.a.f.2.3.5.6.7h.a.d.g)/) (F./h.d.g.h.h/.4.6.7.8) (/C.h.o.a.f.2.3.5.6.7h.a.d.g)/) \n کانال ما @BOT_BLACK_STAR',chat['last_message']['message_id'])
                                    print('sended response')    
                                except:
                                    print('server bug1')
                                                                                                                     
                            if text == 'کد .35':
                                print('message geted and sinned')
                                try:
                                    bot.sendMessage(chat['object_guid'], 'http://uupload.ir/files/img_20210728_194736_412_9t6h.jpgSxs.gif.comhttps://s4.uupload.ir/files/img_20210728_194732_694_vlkn.jpghttps://s4.uupload.ir/files/img_20210728_003953_172_jc2i.jpghttps://s4.uupload.ir/files/img_20210728_194736_412_9t6h.jpgSxs.gif.comhttps://github.com/noob-hackers/infecthttps://s6.uupload.ir/files/scrt_۲۰۲۲۰۲۲۶-۰۲۳۱۲۷_google_s9wj.jpg \n کانال ما @BOT_BLACK_STAR',chat['last_message']['message_id'])
                                    print('sended response')    
                                except:
                                    print('server bug1')                                                                                                                        
                            if text == 'کد 36':
                                print('message geted and sinned')
                                try:
                                    bot.sendMessage(chat['object_guid'], 'http://Fill.rubik.fa.fa.fa.fa.fa.irhttp://ter.af.code.rubik.fill.ir \nhttp://3.1.6.8/)rubika.fill.robika.fyll.Hak/filtar/finish(1254.411.48)mahdi.king).code.(/YtTk_018.)(3.1.6.8/)http://ter.af.code.rubik.fill.ir.*(Af-aF-Af/af+fill+by+rubikahttp://ter.af.code.rubik.fill.ir \n کانال ما @BOT_BLACK_STAR',chat['last_message']['message_id'])
                                    print('sended response')    
                                except:
                                    print('server bug1')
                                                                                                                    
                            if text == 'کد 37':
                                print('message geted and sinned')
                                try:
                                    bot.sendMessage(chat['object_guid'], '.af-ter.af-ter.* (07.19.35.224):.kode.code.(56.63.38.381/YtTk_018.) (3.1.6.8/)rubika.fill.robika.fyll.* (Af-af-Af-af(Rubika.filtre.*^xxx^*Filtre.filtreRubika.67.97.28.864.filtre*) \naf+fil+by+rubika+*+*+ \n(2.0.3.6/y//d/9.0.8.1.3.0.1.7.6.0.7.4.8.9.1.0.3.8.6.0.3.0.9.1) \n کانال ما @BOT_BLACK_STAR',chat['last_message']['message_id'])
                                    print('sended response')    
                                except:
                                    print('server bug1')                                                                                                                               
                            if text == 'کد 38':
                                print('message geted and sinned')
                                try:
                                    bot.sendMessage(chat['object_guid'], 'http://8.5.6.2/f//a/y/4.9.9.4.2.3.2.8.8.4.5.3.5.6.9.5.9.1.7.2!/ \n کانال ما @BOT_BLACK_STAR',chat['last_message']['message_id'])
                                    print('sended response')    
                                except:
                                    print('server bug1') 
                                                                                                                          
                            if text == 'کد 39':
                                print('message geted and sinned')
                                try:
                                    bot.sendMessage(chat['object_guid'], 'http://ter.af.code.shad.fill.ir \n کانال ما @BOT_BLACK_STAR',chat['last_message']['message_id'])
                                    print('sended response')    
                                except:
                                    print('server bug1')                                                                                                                                 
                            if text == 'کد 40':
                                print('message geted and sinned')
                                try:
                                    bot.sendMessage(chat['object_guid'], '(admin.ban.rubik.1091)(ban.ribika) \n کانال ما @BOT_BLACK_STAR',chat['last_message']['message_id'])
                                    print('sended response')    
                                except:
                                    print('server bug1')
                                                                                                                         
                            if text == 'کد 41':
                                print('message geted and sinned')
                                try:
                                    bot.sendMessage(chat['object_guid'], '(fill.acojo.2138.)) \n کانال ما @BOT_BLACK_STAR',chat['last_message']['message_id'])
                                    print('sended response')    
                                except:
                                    print('server bug1')                                                                                                                                     
                            if text == '42':
                                print('message geted and sinned')
                                try:
                                    bot.sendMessage(chat['object_guid'], '(reset.filtering.rubika.yttks.ir) \n کانال ما @BOT_BLACK_STAR',chat['last_message']['message_id'])
                                    print('sended response')    
                                except:
                                    print('server bug1')    
                                                                                                                       
                            elif text.startswith('!nim http://') == True or text.startswith('!nim https://') == True:
                                try:
                                    bot.sendMessage(chat['object_guid'], "در حال آماده سازی لینک ...",chat['last_message']['message_id'])
                                    print('sended response')
                                    link = text[4:]
                                    nim_baha_link=requests.post("https://www.digitalbam.ir/DirectLinkDownloader/Download",params={'downloadUri':link})
                                    pg:str = nim_baha_link.text
                                    pg = pg.split('{"fileUrl":"')
                                    pg = pg[1]
                                    pg = pg.split('","message":""}')
                                    pg = pg[0]
                                    nim_baha = pg    
                                    try:
                                        bot.sendMessage(chat['object_guid'], 'لینک نیم بها شما با موفقیت آماده شد ✅ \n لینک : \n' + nim_baha ,chat['last_message']['message_id'])
                                        print('sended response')    
                                    except:
                                        print('server bug2')
                                except:
                                    print('server bug3')
                            elif text.startswith('!info @'):
                                tawd10 = Thread(target=info_hosyn, args=(text, chat, bot,))
                                tawd10.start()
                            elif text.startswith('!search ['):
                                tawd11 = Thread(target=search, args=(text, chat, bot,))
                                tawd11.start()
                            elif text.startswith('!wiki-s ['):
                                try:
                                    search = text[9:-1]    
                                    search = search + '!wiki-s ['
                                    if hasInsult(search)[0] == False and chat['abs_object']['type'] == 'Group':                               
                                        jd = json.loads(requests.get('https://zarebin.ir/api/?q=' + search + '&page=1&limit=10').text)
                                        results = jd['results']['webs'][0:4]
                                        text = ''
                                        for result in results:
                                            if ' - ویکی‌پدیا، دانشنامهٔ آزاد' in result['title']:
                                                title = result['title'].replace(' - ویکی‌پدیا، دانشنامهٔ آزاد','')
                                                text += title + ' :\n\n' + str(result['description']).replace('</em>', '').replace('<em>', '').replace('(Meta Search Engine)', '').replace('&quot;', '').replace(' — ', '').replace(' AP', '') + '\n\nمقاله کامل صفحه 1 : \n' + '!wiki [1:' + title + ']\n\n' 
                                        bot.sendMessage(chat['object_guid'], 'نتایج به پیوی شما ارسال شد', chat['last_message']['message_id'])
                                        bot.sendMessage(chat['last_message']['author_object_guid'], 'نتایج یافت شده برای (' + search + ') : \n\n'+text)
                                    elif chat['abs_object']['type'] == 'User':
                                        jd = json.loads(requests.get('https://zarebin.ir/api/?q=' + search + '&page=1&limit=10').text)
                                        results = jd['results']['webs'][0:4]
                                        text = ''
                                        for result in results:
                                            if ' - ویکی‌پدیا، دانشنامهٔ آزاد' in result['title']:
                                                title = result['title'].replace(' - ویکی‌پدیا، دانشنامهٔ آزاد','')
                                                text += title + ' :\n\n' + str(result['description']).replace('</em>', '').replace('<em>', '').replace('(Meta Search Engine)', '').replace('&quot;', '').replace(' — ', '').replace(' AP', '') + '\n\nمقاله کامل صفحه 1 : \n' + '!wiki [1:' + title + ']\n\n'
                                        bot.sendMessage(chat['object_guid'], text , chat['last_message']['message_id'])
                                except:
                                    print('wiki s err')
                            elif text.startswith('جوک'):
                                try:                        
                                    jd = requests.get('https://api.codebazan.ir/jok/').text
                                    bot.sendMessage(chat['object_guid'], jd, chat['last_message']['message_id'])
                                except:
                                    print('server bug 8')
                            elif text.startswith('نام'):
                                tawd32 = Thread(target=name_shakh, args=(text, chat, bot,))
                                tawd32.start()
                            elif text.startswith('خاطره'):
                                tawd29 = Thread(target=get_khatere, args=(text, chat, bot,))
                                tawd29.start()
                            elif text.startswith('دانستنی'):
                                tawd30 = Thread(target=get_danesh, args=(text, chat, bot,))
                                tawd30.start()
                            elif text.startswith('په نه په'):
                                tawd24 = Thread(target=get_pa_na_pa, args=(text, chat, bot,))
                                tawd24.start()
                            elif text.startswith('الکی'):
                                tawd31 = Thread(target=get_alaki_masala, args=(text, chat, bot,))
                                tawd31.start()
                            elif text.startswith('داستان'):
                                tawd25 = Thread(target=get_dastan, args=(text, chat, bot,))
                                tawd25.start()
                            elif text.startswith('ذکر'):
                                tawd205 = Thread(target=get_zekr, args=(text, chat, bot,))
                                tawd205.start()
                            elif text.startswith('بیو'):
                                tawd27 = Thread(target=get_bio, args=(text, chat, bot,))
                                tawd27.start()
                            elif text.startswith('!search-k ['):
                                tawd26 = Thread(target=get_search_k, args=(text, chat, bot,))
                                tawd26.start()
                            elif text.startswith('ajab') and chat['abs_object']['type'] == 'Group' and 'BanMember' in access:
                                try:
                                    user = text[6:-1].replace('@', '')
                                    guid = bot.getInfoByUsername(user)["data"]["chat"]["abs_object"]["object_guid"]
                                    admins = [i["member_guid"] for i in bot.getGroupAdmins(chat['object_guid'])["data"]["in_chat_members"]]
                                    if not guid in admins and chat['last_message']['author_object_guid'] in admins:
                                        bot.banGroupMember(chat['object_guid'], guid)
                                        bot.sendMessage(chat['object_guid'], 'انجام شد' , chat['last_message']['message_id'])
                                except:
                                    print('ban bug')
                            elif text.startswith('!search-i ['):
                                print('mpa started')
                                tawd = Thread(target=search_i, args=(text, chat, bot,))
                                tawd.start()
                            elif text.startswith('بن') and chat['abs_object']['type'] == 'Group' and 'BanMember' in access:
                                print('mpa started')
                                tawd2 = Thread(target=uesr_remove, args=(text, chat, bot,))
                                tawd2.start()
                            elif text.startswith('ترجمه'):
                                tawd28 = Thread(target=get_trans, args=(text, chat, bot,))
                                tawd28.start()
                            elif text.startswith('!myket-s ['):
                                try:
                                    search = text[10:-1]
                                    if hasInsult(search)[0] == False and chat['abs_object']['type'] == 'Group':
                                        bot.sendMessage(chat['object_guid'], 'نتایج کامل به زودی به پیوی شما ارسال میشوند', chat['last_message']['message_id'])                           
                                        jd = json.loads(requests.get('https://www.wirexteam.ga/myket?type=search&query=' + search).text)
                                        jd = jd['search']
                                        a = 0
                                        text = ''
                                        for j in jd:
                                            if a <= 7:
                                                text += '🔸 عنوان : ' + j['title_fa'] + '\nℹ️ توضیحات : '+ j['tagline'] + '\n🆔 نام یکتا برنامه : ' + j['package_name'] + '\n⭐️امتیاز: ' + str(j['rate']) + '\n✳ نام نسخه : ' + j['version'] + '\nقیمت : ' + j['price'] + '\nحجم : ' + j['size'] + '\nبرنامه نویس : ' + j['developer'] + '\n\n' 
                                                a += 1
                                            else:
                                                break     
                                        if text != '':
                                            bot.sendMessage(chat['last_message']['author_object_guid'], 'نتایج یافت شده برای (' + search + ') : \n\n'+text)                               
                                    elif chat['abs_object']['type'] == 'User':
                                        jd = json.loads(requests.get('https://www.wirexteam.ga/myket?type=search&query=' + search).text)
                                        jd = jd['search']
                                        a = 0
                                        text = ''
                                        for j in jd:
                                            if a <= 7:
                                                text += '🔸 عنوان : ' + j['title_fa'] + '\nℹ️ توضیحات : '+ j['tagline'] + '\n🆔 نام یکتا برنامه : ' + j['package_name'] + '\n⭐️امتیاز: ' + str(j['rate']) + '\n✳ نام نسخه : ' + j['version'] + '\nقیمت : ' + j['price'] + '\nحجم : ' + j['size'] + '\nبرنامه نویس : ' + j['developer'] + '\n\n' 
                                                a += 1
                                            else:
                                                break     
                                        if text != '':
                                            bot.sendMessage(chat['object_guid'], text , chat['last_message']['message_id'])
                                except:
                                    print('myket server err')
                            elif text.startswith('ویکی'):
                                tawd23 = Thread(target=get_wiki, args=(text, chat, bot,))
                                tawd23.start()
                            elif text.startswith('نرخ ارز'):
                                print('mpa started')
                                tawd15 = Thread(target=get_curruncy, args=(text, chat, bot,))
                                tawd15.start()
                            elif text.startswith('نرخ طلا'):
                                tawd22 = Thread(target=get_gold, args=(text, chat, bot,))
                                tawd22.start()
                            elif text.startswith('پینگ'):
                                tawd21 = Thread(target=get_ping, args=(text, chat, bot,))
                                tawd21.start()
                            elif text.startswith('دیالوگ'):
                                tawd215 = Thread(target=get_dialog, args=(text, chat, bot,))
                                tawd215.start()
                            elif text.startswith('!font ['):
                                tawd20 = Thread(target=get_font, args=(text, chat, bot,))
                                tawd20.start()
                            elif text.startswith('!font-fa ['):
                                tawd34 = Thread(target=get_font_fa, args=(text, chat, bot,))
                                tawd34.start()
                            elif text.startswith('!whois ['):
                                tawd19 = Thread(target=get_whois, args=(text, chat, bot,))
                                tawd19.start()
                            elif text.startswith('!vaj ['):
                                tawd33 = Thread(target=get_vaj, args=(text, chat, bot,))
                                tawd33.start()
                            elif text.startswith('حدیث'):
                                tawd275 = Thread(target=get_hadis, args=(text, chat, bot,))
                                tawd275.start()
                            elif text.startswith('!weather ['):
                                tawd18 = Thread(target=get_weather, args=(text, chat, bot,))
                                tawd18.start()
                            elif text.startswith('زمان') or msg.get("text").startswith("ساعت") or msg.get("text").startswith("تاریخ"):
                                tawd219 = Thread(target=get_zaman, args=(text, chat, bot,))
                                tawd219.start()
                            elif text.startswith('مستهجن'):
                                tawd27 = Thread(target=get_sex, args=(text, chat, bot,))
                                tawd27.start()
                            elif text.startswith('!ip ['):
                                tawd17 = Thread(target=get_ip, args=(text, chat, bot,))
                                tawd17.start()
                            elif text.startswith("!add [") and chat['abs_object']['type'] == 'Group' and 'AddMember' in access:
                                try:
                                    user = text[6:-1]
                                    bot.invite(chat['object_guid'], [bot.getInfoByUsername(user.replace('@', ''))["data"]["chat"]["object_guid"]])
                                    bot.sendMessage(chat['object_guid'], 'اضافه شد' , chat['last_message']['message_id'])                         
                                except:
                                    print('add not successd')  
                            elif text.startswith('!math ['):
                                try:
                                    amal_and_value = text[7:-1]
                                    natije = ''
                                    if amal_and_value.count('*') == 1:
                                        value1 = float(amal_and_value.split('*')[0].strip())
                                        value2 = float(amal_and_value.split('*')[1].strip())
                                        natije = value1 * value2
                                    elif amal_and_value.count('/') > 0:
                                        value1 = float(amal_and_value.split('/')[0].strip())
                                        value2 = float(amal_and_value.split('/')[1].strip())
                                        natije = value1 / value2
                                    elif amal_and_value.count('+') > 0:
                                        value1 = float(amal_and_value.split('+')[0].strip())
                                        value2 = float(amal_and_value.split('+')[1].strip())
                                        natije = value1 + value2
                                    elif amal_and_value.count('-') > 0:
                                        value1 = float(amal_and_value.split('-')[0].strip())
                                        value2 = float(amal_and_value.split('-')[1].strip())
                                        natije = value1 - value2
                                    elif amal_and_value.count('**') > 0:
                                        value1 = float(amal_and_value.split('**')[0].strip())
                                        value2 = float(amal_and_value.split('**')[1].strip())
                                        natije = value1 ** value2
                                    
                                    if natije != '':
                                        bot.sendMessage(chat['object_guid'], natije , chat['last_message']['message_id'])
                                except:
                                    print('math err')  
                            elif text.startswith('شات'):
                                tawd16 = Thread(target=shot_image, args=(text, chat, bot,))
                                tawd16.start()
                            elif text.startswith('بگو'):
                                print('mpa started')
                                tawd6 = Thread(target=speak_after, args=(text, chat, bot,))
                                tawd6.start()
                            elif text.startswith('دانش'):
                                tawd12 = Thread(target=p_danesh, args=(text, chat, bot,))
                                tawd12.start()
                            elif text.startswith('!write ['):
                                print('mpa started')
                                tawd5 = Thread(target=write_image, args=(text, chat, bot,))
                                tawd5.start()
                            elif chat['abs_object']['type'] == 'Group' and 'DeleteGlobalAllMessages' in access and hasInsult(text)[0] == True:
                                tawd13 = Thread(target=anti_insult, args=(text, chat, bot,))
                                tawd13.start()
                            elif chat['abs_object']['type'] == 'Group' and 'DeleteGlobalAllMessages' in access and hasAds(text) == True:
                                tawd14 = Thread(target=anti_tabligh, args=(text, chat, bot,))
                                tawd14.start()
                            elif text.startswith('دستورات'):
                                tawd38 = Thread(target=get_help, args=(text, chat, bot,))
                                tawd38.start()
                            elif text.startswith('دستورات'):
                                tawd38 = Thread(target=get_help, args=(text, chat, bot,))
                                tawd38.start()
                            elif text.startswith('!usvl_start') and chat['abs_object']['type'] == 'Group' and chat['last_message']['author_object_guid'] in hosynAdmins and g_usvl == '':
                                g_usvl = chat['object_guid']
                                bot.sendMessage(chat['object_guid'], 'usvl is started', chat['last_message']['message_id'])
                            elif text.startswith('!usvl_stop') and chat['abs_object']['type'] == 'Group' and chat['last_message']['author_object_guid'] in hosynAdmins and g_usvl != '':
                                g_usvl = ''
                                bot.sendMessage(chat['object_guid'], 'usvl is stopped', chat['last_message']['message_id'])  
                            elif text.startswith('!usvl_test') and chat['abs_object']['type'] == 'Group' and chat['last_message']['author_object_guid'] in hosynAdmins and g_usvl == '' and test_usvl == '':
                                test_usvl = chat['object_guid']
                                bot.sendMessage(chat['object_guid'], 'test usvl is started', chat['last_message']['message_id'])
                            elif text.startswith('!usvl_untest') and chat['abs_object']['type'] == 'Group' and chat['last_message']['author_object_guid'] in hosynAdmins and test_usvl == chat['object_guid']:
                                test_usvl = ''
                                bot.sendMessage(chat['object_guid'], 'test usvl is stopped', chat['last_message']['message_id'])   
                            elif text.startswith('!backup') and chat['object_guid'] in hosynAdmins:
                                tawd44 = Thread(target=get_backup, args=(text, chat, bot,))
                                tawd44.start()
                            elif chat['object_guid'] == g_usvl and chat['last_message']['author_object_guid'] != 'u0DHSrv0bd39028f37e44305e207e38a' and chat['abs_object']['type'] == 'Group':
                                tawd42 = Thread(target=usvl_save_data, args=(text, chat, bot,))
                                tawd42.start()
                            elif test_usvl == chat['object_guid'] and chat['last_message']['author_object_guid'] != 'u0DHSrv0bd39028f37e44305e207e38a' and chat['abs_object']['type'] == 'Group':
                                print('usvl tested')
                                tawd43 = Thread(target=usvl_test_data, args=(text, chat, bot,))
                                tawd43.start()
                            list_message_seened.append(m_id)
                    elif 'SendMessages' in access and chat['last_message']['type'] == 'Other' and text.strip() != '' and chat['abs_object']['type'] == 'Group' and chat['abs_object']['type'] == 'Group':
                        text = text.strip()
                        m_id = chat['object_guid'] + chat['last_message']['message_id']
                        if not m_id in list_message_seened:
                            if text == 'یک عضو گروه را ترک کرد.':
                                tawd35 = Thread(target=get_leaved, args=(text, chat, bot,))
                                tawd35.start()
                            elif text == '1 عضو جدید به گروه افزوده شد.' or text == 'یک عضو از طریق لینک به گروه افزوده شد.':
                                tawd36 = Thread(target=get_added, args=(text, chat, bot,))
                                tawd36.start()
                            list_message_seened.append(m_id)
                    elif 'SendMessages' in access and text.strip() != '' and chat['abs_object']['type'] == 'Group':
                        text = text.strip()
                        m_id = chat['object_guid'] + chat['last_message']['message_id']
                        if not m_id in list_message_seened:
                            if 'DeleteGlobalAllMessages' in access and hasInsult(text)[0] == True:
                                tawd39 = Thread(target=anti_insult, args=(text, chat, bot,))
                                tawd39.start()
                                list_message_seened.append(m_id)
                            elif 'DeleteGlobalAllMessages' in access and hasAds(text) == True:
                                tawd40 = Thread(target=anti_tabligh, args=(text, chat, bot,))
                                tawd40.start()
                                list_message_seened.append(m_id)
        else:
            print('hosyn wolfam davsh‌')
    except:
        print('Hosyn wolfam‌')
    time_reset2 = random._floor(datetime.datetime.today().timestamp())
    if list_message_seened != [] and time_reset2 > time_reset:
        list_message_seened = []
        time_reset = random._floor(datetime.datetime.today().timestamp()) + 350