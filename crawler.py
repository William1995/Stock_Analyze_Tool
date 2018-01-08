#!/usr/bin/python
# -*- coding: UTF-8 -*-

import requests
import csv
import time, datetime, os
import sqlite3
from getProxyip_3 import getRes

dt = datetime.datetime.now()
dt.year
dt.month

#standard web crawing process
def get_webmsg (year, month, stock_id):
    date = str (year) + "{0:0=2d}".format(month) +'01' ## format is yyyymmdd
    sid = str(stock_id)
    link = 'http://www.twse.com.tw/exchangeReport/STOCK_DAY_AVG?response=json&date='+date+'&stockNo='+stockid
    print( link )
    res = getRes( link )
    # print( res.json() )
    return res.json()

def write_csv(stock_id,directory,filename,smt) :
    writefile = directory + filename               #set output file name
    outputFile = open(writefile,'w')
    outputWriter = csv.writer(outputFile)
    smt['data'].pop()
    for data in (smt['data']):
        writeIntoDB( stockid, data )
        outputWriter.writerow(data)

    outputFile.close()


def writeIntoDB( stockId, data ) :
    conn = sqlite3.connect( 'Stock.db' )
    cursor = conn.cursor()
    data[0] = str(int(data[0][0:3])+1911) + '/' + data[0][4:]
    data[0] = data[0][0:4] + '-' + data[0][5:7] + '-' + data[0][8:]
    
    try:
        sql = 'INSERT INTO stock VALUES( %s, \'%s\', \'%s\');' % ( stockId, data[0], data[1] )
        # print( sql )
        cursor.execute( sql )
    #except Exception as e:
        #print( type(e), e )
    except:
        print "重複資料"

    finally:
        conn.commit()
        conn.close()



#create a directory in the current one doesn't exist
def makedirs (year, month, stock_id):
    stockid = str(stock_id)
    yy      = str(year)
    mm       = str(month)
    directory = 'Dataset/'+stockid +'/'+ yy
    if not os.path.isdir(directory):
        os.makedirs (directory)  # os.makedirs able to create multi folders

#id_list = ['2303'] #inout the stock IDs
id_list = []
id_in = raw_input('輸入股票代碼：\n')
id_list = id_in.split(" ")
start_year = raw_input('輸入開始年份：\n')
end_year = raw_input('輸入結束年份：\n')
start_month = raw_input('輸入開始月份：\n')
end_month = raw_input('輸入結束月份：\n')
#now = datetime.datetime.now()
year_list = range (int(start_year),int(end_year)+1)
month_list = range(int(start_month),int(end_month)+1)  # 12 months

for stock_id in id_list:
    for year in year_list:
        for month in month_list:
            if (dt.year == year and month > dt.month) :
                break  # break loop while month over current month
            stockid = str(stock_id)
            yy  = str(year)
            mm  = month
            directory = 'Dataset/'+stockid +'/'+yy +'/'       #setting directory
            filename = str(yy)+str("%02d"%mm)+'.csv'          #setting file name
            smt = get_webmsg(year ,month, stock_id)           #put the data into smt

            makedirs (year, month, stock_id)                  #create directory function
            write_csv (stock_id,directory, filename, smt)    # write files into CSV
            # time.sleep(1)




####http://www.twse.com.tw/exchangeReport/STOCK_DAY_AVG?response=json&date=20171225&stockNo=1234&_=1514190981740




