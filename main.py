#!/usr/bin/env python3

import json
import time
import requests
from flask import Flask
from flask import request, Response
from requests.exceptions import ReadTimeout, ConnectionError, RequestException
from config import *

app = Flask(__name__)

def getstate(entity_id):
    headers = {
        "x-ha-access": password,
        "Content-Type": "application/json"
    }
    url = 'http://{}:{}/api/states/{}'.format(host, port, entity_id)
    try:
        response = requests.get(url, headers=headers, timeout=1)
        response_result = response.json()
        app.logger.debug('getstate url: {}, result: {}'.format(url, json.dumps(response_result)))
    except ReadTimeout:
        response_result = "连接超时"
    except ConnectionError:
        response_result = "连接错误"
    except RequestException:
        response_result = "发生未知错误"
    return response_result


def setstate(entity_id, domain, service, **kwargs):
    headers = {
        "x-ha-access": password,
        "Content-Type": "application/json"
    }
    postdata = {'entity_id': entity_id}
    postdata.update(kwargs)
    postdata = json.dumps(postdata)
    url = 'http://{}:{}/api/services/{}/{}'.format(host, port, domain, service)
    try:
        response = requests.post(url, headers=headers,
                                 data=postdata, timeout=1)
        response_result = response.status_code
        app.logger.debug('setstate url: {}, data: {}, result: {}'.format(url, postdata, response_result))        
    except ReadTimeout:
        response_result = "连接超时"
    except ConnectionError:
        response_result = "连接错误"
    except RequestException:
        response_result = "发生未知错误"
    return response_result


def has_any(query, keywords):
    if type(keywords) == list:
        for kw in keywords:
            if kw in query:
                return (True, kw)
    elif type(keywords) == dict:
        for k,v in keywords.items():
            if k in query:
                return (True, (k, v))
    return (False, None)


def get_tts_text_by_setstate(entity_id, domain, service, action_name, entity_name, **kwargs):
    call_result = setstate(entity_id, domain, service, **kwargs)
    if call_result == 200:
        return '好的，为你' + action_name + entity_name
    else:
        return '与控制中心' + call_result

tts_word = ""
open_mic = True
is_session_end = False


@app.route(route_path, methods=['POST'])
def index():
    datax = request.get_json()
    app.logger.debug(datax)
    if datax["request"]["type"] == 0:
        open_mic = True
        is_session_end = False
        tts_word = "您好，我能为你做什么呢？"
    elif datax["request"]["type"] == 2:
        open_mic = False
        is_session_end = True
        tts_word = "再见，我在这里等你哦!"
    elif datax["request"]["type"] == 1:
        # user hasn't action for a while
        if 'no_response' in datax["request"]:
            open_mic = True
            is_session_end = False
            tts_word = '主人，您还在吗？'
        else:
            query = datax.get('query', '')
            open_mic = True
            is_session_end = False
            tts_word = '对不起, {}暂时不支持{}这种操作'.format(skill_name, query)

            if datax["request"]["intent"]["is_direct_wakeup"] == True:
                open_mic = False
                is_session_end = True

            while True:
                # match cover setpos
                find, kw = has_any(query, cmd_words_cover_setpos)
                find2, item = has_any(query, covers)
                if find and find2:
                    app.logger.debug('match cmd_words_cover_setpos, the query is: {}'.format(query))
                    if kw == '一半':
                        tts_word = get_tts_text_by_setstate(item[1], "cover", "set_cover_position", '打开'+kw, item[0], position=50)
                        break
                    tts_word = '{}还不会处理这个请求'.format(skill_name)
                    break
                elif find:
                    tts_word = '对不起,然而帘子并不存在'
                    break

                # match cover open
                find, kw = has_any(query, cmd_words_cover_open)
                find2, item = has_any(query, covers)
                if find and find2:
                    app.logger.debug('match cmd_words_cover_open, the query is: {}'.format(query))
                    cover_state = getstate(item[1])
                    if type(cover_state) == str:
                        tts_word = '与控制中心' + cover_state
                        break
                    if cover_state.get('state','') == 'open':
                        tts_word = '已经打开了'
                    else:
                        tts_word = get_tts_text_by_setstate(item[1], "cover", "open_cover", kw, item[0])
                    break

                # match cover close
                find, kw = has_any(query, cmd_words_cover_close)
                find2, item = has_any(query, covers)
                if find and find2:
                    app.logger.debug('match cmd_words_cover_close, the query is: {}'.format(query))
                    cover_state = getstate(item[1])
                    if type(cover_state) == str:
                        tts_word = '与控制中心' + cover_state
                        break
                    if cover_state.get('state','') == 'closed':
                        tts_word = '已经关闭了'
                    else:
                        tts_word = get_tts_text_by_setstate(item[1], "cover", "close_cover", kw, item[0])
                    break

                # match cover stop
                find, kw = has_any(query, cmd_words_cover_stop)
                find2, item = has_any(query, covers)
                if find and find2:
                    app.logger.debug('match cmd_words_cover_stop, the query is: {}'.format(query))
                    tts_word = get_tts_text_by_setstate(item[1], "cover", "stop_cover", kw, item[0])
                    break
                elif find:
                    tts_word = '对不起,然而帘子并不存在'
                    break

                # match turn on
                find, kw = has_any(query, cmd_words_turnon)
                find2, item = has_any(query, onoffs)
                if find and find2:
                    app.logger.debug('match cmd_words_turnon, the query is: {}'.format(query))
                    entity_state = getstate(item[1])
                    if type(entity_state) == str:
                        tts_word = '与控制中心' + entity_state
                        break
                    if entity_state.get('state','') == 'on':
                        tts_word = '已经打开了'
                    else:
                        tts_word = get_tts_text_by_setstate(item[1], "homeassistant", "turn_on", kw, item[0])
                    break
                elif find:
                    tts_word = '对不起,您想要打开的神器不存在'
                    break

                # match turn off
                find, kw = has_any(query, cmd_words_turnoff)
                find2, item = has_any(query, onoffs)
                if find and find2:
                    app.logger.debug('match cmd_words_turnoff, the query is: {}'.format(query))
                    entity_state = getstate(item[1])
                    if type(entity_state) == str:
                        tts_word = '与控制中心' + entity_state
                        break
                    if entity_state.get('state','') == 'off':
                        tts_word = '已经关闭了'
                    else:
                        tts_word = get_tts_text_by_setstate(item[1], "homeassistant", "turn_off", kw, item[0])
                    break
                elif find:
                    tts_word = '对不起,您想要关闭的神器不存在'
                    break

                # query read-only variables
                find, kw = has_any(query, cmd_words_query)
                find2, item = has_any(query, read_onlys)
                if find and find2:
                    app.logger.debug('match cmd_words_query, the query is: {}'.format(query))
                    entity_state = getstate(item[1][0])
                    if type(entity_state) == str:
                        tts_word = '与控制中心' + entity_state
                        break
                    tts_word = '当前'+ item[0] +'为' + entity_state['state'] + item[1][1]
                    break
                elif find:
                    tts_word = '对不起,您要查询的项目没有找到'
                    break

                # nothing matched
                # tts_word the default answer

                break # break the while True

            
    say_text = {'version': '1.0', 'session_attributes': {'sessi_id': '12345'}, 'response': {'open_mic': open_mic, 'to_speak': {
        'type': 0, 'text': tts_word}, 'to_display': {'type': 0, 'text': tts_word}}, 'directives': [], 'is_session_end': is_session_end}
    return Response(json.dumps(say_text), mimetype='application/json')

if ssl_fullchain_pem_path and ssl_private_pem_path:
    app.run('0.0.0.0', debug=flask_debug, port=serve_port, ssl_context=(ssl_fullchain_pem_path, ssl_private_pem_path))
else:
    app.run('0.0.0.0', debug=flask_debug, port=serve_port)
    
