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
from dbconnect import connection,init_db,db_session
from MySQLdb import escape_string as thwart
from models import KoscomList
from koscom_list import StockList

class StockListCtl:
    def __init__(self, mode):
        self.mode = mode

    def process_run(self):

        try:

            body_dict = Koscom.get_stock_list()
            for k, v in body_dict.items():
                temp_trdDd = v.get("trdDd")

            if temp_trdDd == None:
                trdDd = "None"
            else:
                trdDd = temp_trdDd

            for k1,v1 in body_dict.items():
                list_items= v1.get('isuLists')

                for dict_item in list_items :

                    dict_item.update({"trdDd":trdDd})
                    b = StockList(self.mode)
                    b.update_valid()
                    b.set_value(dict_item)


        except Exception as e:
            print(e)

    def get_value_all(self):
        b = StockList("read")
        List= b.get_value_all()
        kwargs={"stock_list": List }
        return kwargs



if __name__ == "__main__":
    name_or_issuecode = "005010"
    c,conn = connection()
    mode = "read"
    d=StockList(mode)
    #d.process_run()
    #a=d.get_value_all()
    a=d.get_name(name_or_issuecode)
    c.close()
    conn.close()
    print(a)
