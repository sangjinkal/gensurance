# coding=utf-8
import re
import urllib.request
import urllib
import json
import http.client
import ast
import syslog
import logging
from ..import app
from ..config import BASE_URL,API_KEY,CLIENT_ID,CLIENT_SECRET,MARKET_CODE, SLACK_TOKEN


def koscom_response(data):
    try:
        mode = data.get("mode","")
        inputdata = data.get("input", "")

        if (mode is None):
            body_response = { }
        else:
            # body_response = make_call_binary(url, "GET")
            get_resp_func = msg_type_resp[mode]

            body_response = get_resp_func(inputdata)

    except Exception as e:
        body_response = {"error" : e }
    finally:
        return body_response

def make_call_binary (url,method):
    try:
        conn = http.client.HTTPSConnection(BASE_URL)
        headers = {
            'apikey': API_KEY,
            'cache-control': "no-cache",
            'Content-Type': 'application/json;charset=UTF-8'
            }

        conn.request(method, url, headers=headers)
        res = conn.getresponse()
        body_res= res.read()
        body_res1= binary_to_dict (body_res)

        if (body_res1.get('result') == None) :
            body_response = body_res1
        else:
            body_response = body_res1.get('result')
        return body_response
    except Exception as e:
        return e

def binary_to_dict(the_binary):
    the_binary1 = the_binary.decode("utf-8")
    str1 = the_binary1
    str2=str1.replace("\\","")
    d = ast.literal_eval(str2)
    return d

msg_type_resp = {}

def make_call(mode):
    def decorator (func):
        msg_type_resp[mode] = func
        return func
    return decorator


@make_call('price')
def make_call_price(inputdata):
    issue_code = inputdata.get("issue_code", "005930")
    url =  "/v2/market/stocks/kospi/" + issue_code + "/price"
    body_response = make_call_binary(url, "GET")
    return body_response
