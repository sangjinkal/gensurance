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
from koscom_list import StockList
import multiprocessing
import sys

THREADS = 3
GLOBALLOCK = multiprocessing.Lock()

class Book_details:
    def __init__(self, **kwargs):
        self.mode = kwargs.get("mode","read")
        self.l_bookkeeper = kwargs.get("l_bookkeeper","")
        self.sheet_name = kwargs.get("sheet_name","")
        self.list_name = kwargs.get("list_name",[])
        self.issue_code = kwargs.get("issue_code","")
        self.market_code = kwargs.get("market_code","")

    def set_value(self):
        c, conn = connection()
        list_name = self.list_name
        if list_name == []:
            return  {'flag': 'fail', 'desc': 'no list' }
        else:
            try:


                for dict_item in list_name:

                    book_depth = dict_item.get("depth", 0)
                    book_code = dict_item.get("code", "")
                    book_name = dict_item.get("name", "")
                    book_value = dict_item.get("value", 0)
                    if mode == "write":
                        max_id = getID("tb_stock_book_details")
                    else:
                        max_id = "000"
                    cmd = "insert into gensurance.tb_stock_book_details (id, marketcode, issuecode, l_bookkeeper, sheet_name, book_depth,   book_code, book_name, book_value) "
                    cmd = cmd + " values('{id}', '{marketcode}','{issuecode}', '{l_bookkeeper}', '{sheet_name}', {book_depth}, '{book_code}', '{book_name}', {book_value}) "
                    sql = cmd.format (id=max_id, marketcode=self.market_code, issuecode=self.issue_code, l_bookkeeper=self.l_bookkeeper, sheet_name=self.sheet_name, book_depth=book_depth, book_code=book_code, book_name = book_name, book_value=book_value )
                    if self.mode == "write":
                        c.execute(sql)
                        conn.commit()
                    else:
                        pass
                return {'flag':'success', 'desc': ''}
            except Exception as e:
                return {'flag': 'fail', 'desc': ''}


def main():
    issue_code = "005930"
    pool = multiprocessing.Pool(THREADS)
    try:

        stocklists = StockList("read")
        stocklistall = stocklists.get_value_all()
        pool.map(process_run, stocklistall)

    except Exception as e:
        print(e)
    finally:
        pool.close()

def process_run(stocklistall):

    try:
        cnt = 0
        totalcnt = len(stocklistall)
        for stockdict in stocklistall:
            cnt = cnt + 1
            isuSrtCd = stockdict.get("isuSrtCd", issue_code)
            print (isuSrtCd + " : " + str(cnt) + "out of " + str(totalcnt) + "......")
            process(stockdict)

    except Exception as e:
        print(e)

def process(stockdict):
    mode = "read"
    issue_code = "005930"
    market_code = "kospi"
    start_date = "20160601"
    end_date = "20161231"
    isuSrtCd = stockdict.get("isuSrtCd", issue_code)
    GLOBALLOCK.acquire()
    try:
        body_response = Koscom.get_stock_bookkeeper(isuSrtCd,start_date, end_date)

        body_res1 = body_response.get("bookkeeper", "")
        body_res1 = json.loads(body_res1)
        body_res1 = body_res1.get("data","")[0]
        body_blank = {'data': []}
        if body_res1 == body_blank :
            pass
        else:
            market_id = body_res1.get("market_id","")
            exchange = body_res1.get("exchange", "")
            business_type = body_res1.get("business_type", "")
            consolidated = body_res1.get("consolidated", "")
            symbol = body_res1.get("symbol", "")
            fiscal_year = body_res1.get("fiscal_year", "")
            income_list = body_res1.get("income", [])
            cash_flow_list = body_res1.get("cash_flow", [])
            balance_sheet_list = body_res1.get ("balance_sheet", [])
            equity_changes_list = body_res1.get("equity_changes", [])
            if mode == "write":
                max_id = getID("tb_stock_bookkeeper")
            else:
                max_id = "000"
            c, conn = connection()
            cmd = "insert into gensurance.tb_stock_bookkeeper (id, marketcode, issuecode, market_id, exchange, business_type, consolidated, symbol, fiscal_year) "
            cmd = cmd + "values ('{id}', '{marketcode}', '{issuecode}', '{market_id}', '{exchange}', '{business_type}', '{consolidated}', '{symbol}', '{fiscal_year}')"
            sql = cmd.format(id=max_id,marketcode=market_code, issuecode=issue_code, market_id=market_id, exchange=exchange, business_type=business_type, consolidated=consolidated, symbol=symbol, fiscal_year=fiscal_year)
            if mode == "write":
                c.execute(sql)
                conn.commit()
            else:
                pass
            # balance_sheet

            sheet_name = "balance_sheet"
            print(sheet_name)
            list_name = balance_sheet_list
            kwargs = { "mode":mode, "l_bookkeeper": max_id, "issue_code" : issue_code, "market_code":market_code, "sheet_name" : sheet_name, "list_name" : list_name }

            d = Book_details(**kwargs)
            d.set_value()

            #income
            sheet_name = "income"
            print(sheet_name)
            list_name = income_list
            kwargs = {  "mode":mode, "l_bookkeeper": max_id, "issue_code" : issue_code, "market_code":market_code, "sheet_name" : sheet_name, "list_name" : list_name }
            d = Book_details(**kwargs)
            d.set_value()

            #cash_flow
            sheet_name = "cash_flow"
            print(sheet_name)
            list_name = income_list
            kwargs= {  "mode":mode, "l_bookkeeper": max_id, "issue_code" : issue_code, "market_code":market_code, "sheet_name" : sheet_name, "list_name" : list_name }
            d = Book_details(**kwargs)
            d.set_value()

            #equity_changes
            sheet_name = "equity_changes"
            print(sheet_name)
            list_name = equity_changes_list
            kwargs = {  "mode":mode, "l_bookkeeper": max_id, "issue_code" : issue_code, "market_code":market_code, "sheet_name" : sheet_name, "list_name" : list_name }
            d = Book_details(**kwargs)
            d.set_value()

    except Exception as e:
        print(e)
        print(body_res1)
    finally:
        GLOBALLOCK.release()


if __name__ == "__main__":

    main()
