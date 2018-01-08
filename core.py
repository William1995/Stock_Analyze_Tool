#!/usr/bin/python
# -*- coding: UTF-8 -*-
import sqlite3
import numpy as np
import datetime
import math
import random
from numpy import *
from random import gauss
from random import gammavariate

def searchDB (stock_id,start_time,end_time):
    temp_list = []
    temp_list = stock_id.split(" ")
    temp3 = []
    conn = sqlite3.connect( 'test.db' )
    cursor = conn.cursor()
    for temp in temp_list:
        test = 'SELECT Price FROM stock WHERE ID =' + temp + ' AND Time >=' + "'" + start_time + "'" + ' AND Time <=' + "'" + end_time + "'" + ';'
        temp2=[]
        for row in cursor.execute(test):
            temp2 = np.append(temp2,row)
        #print temp2
        temp3.append(temp2)
    return temp3
    del temp2
    del temp3
    del temp_list

def student_t(nu): # nu equals number of degrees of freedom
    x = 0
    x = gauss(0.0, 1.0)
    y = 2.0 * gammavariate(0.5*nu, 2.0)
    return x / (math.sqrt(y/nu))

def generate_st(dataset):
    temp_st = 0
    temp_st_list = []
    for i in range(0,dataset):
        temp = student_t(1)
        temp_st_list.append(temp)
    return temp_st_list
    del temp_st_list

def costf(M,w,vc,dataset):
    rf=0.0104   #free risk(year)
    r=0
    #年化報酬
    for i in range(0,dataset):
        r = r + w[i] * M[i]
    r = (r+1) ** 250 -1
    #年化標準差
    temp_w=0
    for j in range(0,dataset):
        temp_w = temp_w + w[j] * w[j]
    risk = temp_w * sum(vc) * sqrt(250)

    sharpe = (r-rf)/sqrt(risk)
    target = -sharpe
    return target

def gen_wmin(dataset):
    x = 1 / dataset
    temp_wmin = []
    for i in range(0,dataset):
        temp_wmin.append(x)
    return temp_wmin

command = '0'


while (command != '-1') :

    search_result = []
    time_period = 0
    dataset = 0
    flaot_rate = []
    temp_rate = 0

    command = raw_input('選擇要執行的動作：\n (1) 分析最佳投資組合 (2) 離開\n')
    if command == '1':
        stock_id = raw_input('輸入要分析之股票代碼：\n')
        start_time = raw_input('輸入分析起始時間：\n')
        end_time = raw_input('輸入分析結束時間：\n')
        
        #search data#
        
        search_result = searchDB(stock_id,start_time,end_time)
        
        dataset = len(search_result)
        time_period = len(search_result[0])
        search_result = np.array(search_result)
        #print time_period
        
        #stock return#

        for i in range(0,dataset):
            temp_rate2 = []
            for day in range(1,time_period):
                if ',' in str(search_result[i][day]):
                    search_result[i][day] = search_result[i][day].replace(',','')
                    search_result[i][day-1] = search_result[i][day-1].replace(',','')
                if search_result[i][day] == "--":
                    search_result[i][day] = search_result[i][day-1]
                temp_rate = (float(search_result[i][day]) - float(search_result[i][day-1])) / float(search_result[i][day-1])
                temp_rate2.append(temp_rate)
            flaot_rate.append(temp_rate2)
            del temp_rate2
        
        #print flaot_rate

        #計算平均股票報酬與風險#
        flaot_rate_avg = []
        avg_temp = 0
        sigma = []
        sigma_temp = 0
        for i in range(0,dataset):
            avg_temp = np.mean(flaot_rate[i])
            flaot_rate_avg.append(avg_temp)
            sigma_temp = np.std(flaot_rate[i])
            sigma.append(sigma_temp)
        #print flaot_rate_avg
            
        #variance-covariance#
        vc = []
        rho = []
        vc_temp = 0
        rho = np.corrcoef(flaot_rate)
        for i in range(0,dataset):
            for j in range(0,dataset):
                vc_temp = rho[i][j] * sigma[i] * sigma[j]
                vc.append(vc_temp)

        #-----#
        T = 10000
        fk = 1000
        fk2 = 0
        fmin = 1000
        #wmin = [0.8,0.1,0.1]
        wmin = []
        wmin = gen_wmin(dataset)
        count_fire = 0
        w = zeros(dataset)
        
        while T > 0.1:
            z = []
            w1 = []
            sum_w = 0
            div_w = []
            
            for i in range(0,10000):
                z = generate_st(dataset)
                w1 = w + z
                
                #保證權重大於零#
                for k in range(0,dataset):
                    if w1[k] < 0:
                        w1[k] = 0
            
                sum_w = sum(w1)
                div_w = w1 / sum_w
                fk2 = costf(flaot_rate_avg,div_w,vc,dataset)
                
                if fk2 <= fk or exp(-(fk2 - fk ) / T) > random.random():
                    w = w1
                    fk = fk2

                if fk < fmin:
                    wmin = div_w
                    fmin = fk

            count_fire = count_fire +1
            T = T * 0.95
        
        print "======================"
        print "fmin = " + str(-(fmin))
        print "======================"
        print "最佳組合:"
        print stock_id
        print wmin
        print "======================"
        
    
    elif command == '2':
        command = '-1'
