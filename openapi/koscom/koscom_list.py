# coding=utf-8
import urllib.request
import urllib
import json
from webclient import WebClient
import http.client
import ast
import syslog
from insuranceCommon import getID, getDobConvert
import MySQLdb
import time
from dbconnect import connection,init_db,db_session
from MySQLdb import escape_string as thwart
from models import KoscomList

class StockList:

    def __init__(self,mode = None):
        self.mode = mode
        self.id = ''
        self.trdDd = ''
        self.isuCd = ''
        self.isuKorAbbrv = ''
        self.isuSrtCd = ''
        self.isuKorNm = ''

    def update_valid(self):
        c, conn = connection()
        try:
            cmd_temp = "update gensurance.tb_stock_lists set valid = 'N' where valid ='Y'"
            if self.mode == "write":

                c.execute(cmd_temp)
            else:
                pass
            return {"flag": "success","desc":"ok"}

        except Exception as e :

            return {"flag": "fail", "desc": e}
        finally:
            c.close()
            conn.close()


    def set_value(self, kwargs):
        try:

            if (self.mode == "write"):
                self.id = getID("tb_stock_lists")
            else:
                self.id = "001"
            self.trdDd = kwargs.get('trdDd','')
            self.isuCd = kwargs.get('isuCd','')
            self.isuKorAbbr = kwargs.get('isuKorAbbr','')
            self.isuSrtCd = kwargs.get('isuSrtCd','')
            self.isuKorNm = kwargs.get('isuKorNm','')

            cmd = "insert into gensurance.tb_stock_lists (id, trdDd, isuCd, isuKorAbbrv, isuSrtCd, isuKorNm) "
            cmd = cmd + "values( '{id}' , '{trdDd}', '{isuCd}', '{isuKorAbbrv}', '{isuSrtCd}','{isuKorNm}' )"
            sql = cmd.format(id=self.id, trdDd=self.trdDd,isuCd=self.isuCd, isuKorAbbrv=self.isuKorAbbr, isuSrtCd=self.isuSrtCd, isuKorNm=self.isuKorNm)
            if (self.mode == "write"):
                c, conn = connection()
                c.execute(sql)
            else:
                print(sql)
        except Exception as e:
            print(e)

    def get_value_all(self):
        List = []
        try:
            c,conn = connection()
            sql ="SELECT id, trdDd, isuCd, isuKorAbbrv, isuSrtCd, isuKorNm FROM gensurance.tb_stock_lists WHERE valid = 'Y'"
            c.execute(sql)
            rows = c.fetchall()

            for row in rows:
                maxID=row[0]
                trdDd=row[1]
                isuCd=row[2]
                isuKorAbbrv=row[3]
                isuSrtCd=row[4]
                isuKorNm=row[5]
                kwargs = {"id":maxID, "trdDd":trdDd, "isuKorAbbr":isuKorAbbrv, "isuSrtCd":isuSrtCd, "isuKorNm":isuKorNm}
                List.append(kwargs)
            return List

        except Exception as e:
            return List
    def get_value_by_issuecode(self,issuecode):

        c,conn = connection()
        try:

            cmd ="SELECT id, trdDd, isuCd, isuKorAbbrv, isuSrtCd, isuKorNm FROM gensurance.tb_stock_lists WHERE valid = 'Y' and isuSrtCd = '{issuecode}'"
            sql = cmd.format (issuecode = issuecode)
            c.execute(sql)
            row = c.fetchone()
            maxID=row[0]
            trdDd=row[1]
            isuCd=row[2]
            isuKorAbbrv=row[3]
            isuSrtCd=row[4]
            isuKorNm=row[5]
            kwargs = {"id":maxID, "trdDd":trdDd, "isuKorAbbr":isuKorAbbrv, "isuSrtCd":isuSrtCd, "isuKorNm":isuKorNm}

            return kwargs

        except Exception as e:
            return e


    def get_value_by_isuKorNm(self,isuKorNm):

        init_db()
        try:

            koscom=db_session.query(KoscomList).filter(KoscomList.isuKorNm == isuKorNm).first()
            maxID = koscom.id
            trdDd = koscom.trdDd
            isuKorAbbrv = koscom.isuKorAbbrv
            isuSrtCd = koscom.isuSrtCd
            isuKorNm = koscom.isuKorNm
            kwargs = {"id":maxID, "trdDd":trdDd, "isuKorAbbr":isuKorAbbrv, "isuSrtCd":isuSrtCd, "isuKorNm":isuKorNm}

            return kwargs

        except Exception as e:
            return e
    def is_integer(string_or_integer):
        try:
            int(string_or_integer)
            return True
        except Exception as e:
            return False
    def get_value(self,name_or_issuecode):
        b = StockList("read")

        try:
            if StockList.is_integer(name_or_issuecode) == True :

                c = b.get_value_by_issuecode(name_or_issuecode)
            else:

                c = b.get_value_by_isuKorNm(name_or_issuecode)
        except Exception as e:
                return e

        kwargs={"stock_list": c }
        return kwargs
    def get_name(self,name_or_issuecode):
        b = StockList("read")
        try:

            Temp_Dict=b.get_value(name_or_issuecode).get("stock_list",{})
            isuKorNm = Temp_Dict.get("isuKorNm", "")
            return isuKorNm
        except Exception as e:
            return ""
