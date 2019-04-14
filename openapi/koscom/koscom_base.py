# coding=utf-8
import urllib.request
import urllib
import json
import http.client
import ast
import syslog
from dbconnect import connection,db_session,init_db
from models import TbReference
from config import BASE_URL,API_KEY,CLIENT_ID,CLIENT_SECRET,MARKET_CODE, SLACK_TOKEN
from koscom_list import StockList
# from koscom_list import StockListCtl


class Koscom:

    base_url = BASE_URL
    api_key = API_KEY
    client_id = CLIENT_ID
    client_secret = CLIENT_SECRET
    market_code = MARKET_CODE
    slack_token = SLACK_TOKEN

    def get_stock_list():
        process_name = "lists"
        try:
            url = "/v2/market/stocks/kospi/lists"
            body_response = Koscom.make_call_binary (url, "GET")
            return { process_name : body_response }
        except Exception as e:
            return {"error": e}

    def get_stock_bookkeeper(issue_code,DateFrom,DateTo):
        process_name = "bookkeeper"
        try:
            if (issue_code is None):
            
            url = "/v1/bookkeeper/fs/ifrs/" + issue_code + "?from=" + DateFrom + "&to=" + DateTo


            body_response = Koscom.make_call_dict(url, "GET")
            return { process_name : body_response }
        except Exception as e:
            return {"error": e}

    def get_stock_master(issue_code):
        process_name = "master"
        try:
            if (issue_code is None):
                return { }

            url =  "/v2/market/stocks/kospi/" + issue_code + "/master"

            body_response = Koscom.make_call_binary(url, "GET")
            return { process_name : body_response }
        except Exception as e:
            return {"error": e}

    def get_stock_orderbook(issue_code):
        process_name = "orderbook"
        try:
            if (issue_code is None):
                return { }
            url =  "/v2/market/stocks/kospi/" + issue_code + "/orderbook"

            body_response = Koscom.make_call_binary(url, "GET")
            return { process_name : body_response }
        except Exception as e:
            return {"error": e}

    def get_stock_history(issue_code,trnsmCycleTpCd=None,inqStrtDd=None,inqEndDd=None,reqCnt=None):
        process_name = "history"

        if trnsmCycleTpCd == None:
            trnsmCycleTpCd = "W"
        else:
            pass
        if inqStrtDd == None:
            inqStrtDd = "20160710"
        else:
            pass
        if inqEndDd == None:
            inqEndDd = "20161130"
        else:
            pass
        if reqCnt == None:
            reqCnt = "100"
        else:
            pass

        try:
            if (issue_code is None):
                return { }

            body_response = Koscom.make_call_binary(url, "GET")
            return { process_name : body_response }
        except Exception as e:
            return {"error" : e }


    def get_stock_price(issue_code):
        process_name = "price"
        try:
            if (issue_code is None):
                return { }

            url =  "/v2/market/stocks/kospi/" + issue_code + "/price"

            body_response = Koscom.make_call_binary(url, "GET")

            return { process_name : body_response }
        except Exception as e:
            return {"error" : e }
    def get_stock_price_kr(issue_code):
        process_name = "Stock(" + issue_code + ")"
        try:
            if (issue_code is None):
                return { }
            url =  "/v2/market/stocks/kospi/" + issue_code + "/price"

            body_response = Koscom.make_call_binary(url, "GET")
            body_response_kr = {}
            for k,v in body_response.items():
                try:
                    column_kr = Koscom.get_reference_3factor("koscomtable","tb_stock_price", k)
                except Exception as e:
                    column_kr = k
                if type(v) == int:
                    v = format(v,",")
                else:
                    pass

                if (k == "cmpprevddTpCd" or k=="lstAskbidTpCd"):
                    v = Koscom.get_reference_3factor("tb_stock_price",k, v)
                else:
                    pass

                dict_temp = {column_kr : v}
                body_response_kr.update(dict_temp)

            d=StockList("read")
            isuKorNm=d.get_name(issue_code)
            if isuKorNm == "" :
                pass
            else:
                process_name = isuKorNm + "(" + issue_code + ")"

            return { process_name : body_response_kr }
        except Exception as e:
            return {"error": e}

    def get_reference_3factor(factor_type=None, factor1=None, factor2=None):
        init_db()
        try:
            reference = db_session.query(TbReference).filter(TbReference.version == 999) \
                                                    .filter(TbReference.country_code == 'KR') \
                                                    .filter(TbReference.factor_type == factor_type) \
                                                    .filter(TbReference.factor1 == factor1) \
                                                    .filter(TbReference.factor2 == factor2).first()
            result = reference.result.rstrip()
            return result
        except Exception as e:
            return e

        finally:
            db_session.close()
    def make_call_binary (url,method):
        try:
            conn = http.client.HTTPSConnection(Koscom.base_url)
            headers = {
                'apikey': Koscom.api_key,
                'cache-control': "no-cache",
                'Content-Type': 'application/json;charset=UTF-8'
                }

            conn.request(method, url, headers=headers)
            res = conn.getresponse()
            body_res= res.read()
            body_res1= Koscom.binary_to_dict (body_res)

            if (body_res1.get('result') == None) :
                body_response = body_res1
            else:
                body_response = body_res1.get('result')
            return body_response
        except Exception as e:
            return e

    def make_call_dict (url,method):
        try:
            conn = http.client.HTTPSConnection(Koscom.base_url)
            headers = {
                'apikey': Koscom.api_key,
                'cache-control': "no-cache",
                'Content-Type': 'application/json;charset=UTF-8'
                }

            conn.request(method, url, headers=headers)
            res = conn.getresponse()
            body_response= res.read().decode('utf-8)')
            return body_response
        except Exception as e:
            return e

    def binary_to_dict(the_binary):
        the_binary1 = the_binary.decode("utf-8")
        str1 = the_binary1
        str2=str1.replace("\\","")
        d = ast.literal_eval(str2)
        return d



#try:

#body_response = Koscom.get_stock_price_kr("005930")
#print (body_response)
#except Exception as e:
#    print(e)
