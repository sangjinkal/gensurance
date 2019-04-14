import MySQLdb
import time
from dbconnect import connection
from MySQLdb import escape_string as thwart
import json
import datetime
import gc


def getDobConvert(str):
	try:
		if len(str) == 6:
			year_temp = str[0:2]
			if year_temp <= '30':
				year_str = '20' + year_temp
			else:
				year_str = '19' + year_temp

			month_str = str[2:4]
			day_str = str[4:6]
			date_str = year_str + '-' + month_str + '-' + day_str
			date = datetime.datetime.strptime(date_str , '%Y-%m-%d')
			return date

		else:
			return "nok"
	except Exception as e:
		print (e)
		return "nok"
def getInsuranceAge(when, on=None):
    if on is None:
        on = datetime.date.today()
    on_unix = time.mktime(on.timetuple())
    when_unix = time.mktime(when.timetuple())
    return int(round((on_unix - when_unix) / 3.15569e7,0))

def getID(tablename):
	c, conn = connection()
	try:
		format_sql ="""SELECT table_surfix, table_next_seq +1 FROM tb_table_seq WHERE table_name = '{table_name}';"""
		sql= format_sql.format(table_name = tablename)
		c.execute(sql)
		row = c.fetchone()
		table_surfix = row[0]
		table_next = int(row[1])
		table_next_str = str(table_next)
		cnt = 8
		table_next_str1 = table_next_str.rjust(cnt,'0')
		table_id = table_surfix + table_next_str1
		cmd = """UPDATE tb_table_seq SET table_next_seq = {table_next_seq} WHERE table_name = '{table_name}'"""
		sql = cmd.format(table_next_seq = table_next, table_name = tablename)
		c.execute(sql)

		conn.commit()
		return table_id

	except Exception as e:
		status= "nok"
		conn.rollback()
		return status
	finally:
		c.close()
		conn.close()
		gc.collect()
# x = getDobConvert ("700303")
# Age = getInsuranceAge(x)
# print (Age)
# x = getID("tb_client")
# print x

#print(getAge(datetime.date(1970, 3, 3)) )
