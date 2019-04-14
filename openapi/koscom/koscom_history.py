# coding=utf-8
import urllib.request
import urllib
import json
from webclient import WebClient
import http.client
import ast
import syslog
from koscom_base import Koscom
from insuranceCommon import getID, getDobConvert
import MySQLdb
import time
from dbconnect import connection
from MySQLdb import escape_string as thwart
import pandas as pd

try:
    issue_code = "005930"
    market_code = "kospi"
    numOfAverage = 5
    body_dict_temp = Koscom.get_stock_history(issue_code,"W","20160710","20161120","100")

    body_dict = body_dict_temp.get("history", "{}")
    temp_isuSrtCd = body_dict.get("isuSrtCd", "")
    list_items= body_dict.get("hisLists", "")
    c, conn = connection()
    List = []
    List.append(['marketcode', 'issuecode','trdDd', 'trdPrc', 'opnprc', 'hgprc', 'lwprc','accTrdvol','accTrdval', 'cmpprevddPrc'])

    for dict_item in list_items :

        #Commented Temporary to prevent updating table id
        #maxID = getID("tb_stock_history")
        maxID  = "0001"
        trdDd= dict_item.get("trdDd","")
        trdPrc = dict_item.get("trdPrc","")
        opnprc = dict_item.get("opnprc",0)
        hgprc = dict_item.get("hgprc",0)
        lwprc = dict_item.get("lwprc",0)
        accTrdvol = dict_item.get("accTrdvol",0)
        accTrdval = dict_item.get("accTrdval",0)
        cmpprevddPrc = dict_item.get("cmpprevddPrc",0)
        List_temp = [market_code, issue_code, trdDd, trdPrc,opnprc,hgprc,lwprc,accTrdvol, accTrdval, cmpprevddPrc]
        List.append(List_temp)

    headers = List.pop(0)

    df = pd.DataFrame(List, columns=headers)
    df1 = df.iloc[::-1]
    df = df1


    CntAverage = len(df.index) - numOfAverage
    print ("CntAverage: " + str(CntAverage))
    if CntAverage <= 0 :
        CntAverage = 0
    else:
        pass

    df['MA5'] = pd.stats.moments.rolling_mean(df['trdPrc'], numOfAverage)
    df_final = df.loc[CntAverage:0,['trdDd','trdPrc','MA5']]


    print(df_final)

except Exception as e:
    print(e)
