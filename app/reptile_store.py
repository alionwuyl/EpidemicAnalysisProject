#!/usr/bin/env python
# coding: utf-8

# In[7]:


# 引入需要的库
import requests
import re
from bs4 import BeautifulSoup
import json
import time
import pymysql
from datetime import datetime, date, timedelta


db = pymysql.connect('localhost', 'root', 'wyl5683wyl', 'epidemicdb')
cursor = db.cursor()

tempsql = "select * from home_realtime_datas order by id desc"
cursor.execute(tempsql)
tempUpdatedTime = cursor.fetchall()[0][16]
print(tempUpdatedTime)

dateNow = (date.today() + timedelta(days=-1)).strftime("%Y-%m-%d")

if tempUpdatedTime[0:10] == dateNow:
    print('当前数据为最新数据')
else:
    print('爬取数据中')
    # 爬取的目标网址
    url="https://voice.baidu.com/act/newpneumonia/newpneumonia"
    # 请求头
    headers = {
        'user-agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.149 Safari/537.36'
    }
    # 响应对象
    reponse=requests.get(url, headers=headers)
    #print(reponse.status_code)
    # 转码
    data=reponse.content.decode("utf8")

    #构建soup对象
    soup=BeautifulSoup(data, 'html.parser')
    # 找到所需要数据所在的位置
    tag=soup.find('script', attrs={'type':"application/json", 'id':"captain-config"})
    # 转换成字符串
    tagstr=str(tag)
    # 进行分割
    results=re.findall(r'\{["confirmed","died"].*?"subList":\[.*?\]\}', tagstr)
    #数据的第一条和最后一条进行特殊处理
    totalInfo = []
    temp=re.findall(r'\{"confirmed".*?"subList":\[.*?\]\}', results[0])
    totalInfo.append(temp[0])
    #  将中间内容加入
    lenOfList = len(results)-1
    for i in range(1, lenOfList):
        totalInfo.append(results[i])

    # 国内数据
    for i in range(0, 34):
        print('--------------' * 3)
        temp = json.loads(totalInfo[i])
        localt = time.localtime(float(temp['relativeTime']))
        timestr = time.strftime("%Y-%m-%d %H:%M:%S", localt)
        print(temp)
        if 'asymptomatic' not in temp.keys():
            tempasymptomatic='0'
        else:
            tempasymptomatic=temp['asymptomatic']
        if 'asymptomaticRelative' not in temp.keys() or len(temp['asymptomaticRelative']) == 0:
            tempasymptomaticRelative='0'
        else:
            tempasymptomaticRelative=temp['asymptomaticRelative']
        #print('%d  %s 累积确诊:%s 累积死亡:%s 累积治愈:%s 更新时间:%s 新增:%s' % (i+1, temp['area'], temp['confirmed'], temp['died'], temp['crued'], timestr, temp['confirmedRelative']))
        tempsql='insert into province_daily_datas(curConfirm, curConfirmRelative, confirmed, confirmedRelative, died, diedRelative, cured, curedRelative, area, asymptomatic, asymptomaticRelative, pub_date) values (%s, %s, %s, %s, %s, %s, %s, %s, "%s", %s, %s, "%s"' % (temp['curConfirm'], temp['curConfirmRelative'], temp['confirmed'], temp['confirmedRelative'], temp['died'], temp['diedRelative'], temp['crued'], temp['curedRelative'], temp['area'], tempasymptomatic, tempasymptomaticRelative, timestr) + ')'
        print(tempsql)
        cursor.execute(tempsql)

        tempstr = temp['subList']
        #print(len(tempstr))
        #print(type(tempstr))
        print('++++++++++++++' * 3)
        if len(tempstr) == 0:
            print('空')
        else:
            for j in range(0, len(tempstr)):
                #print(type(tempstr[j]))
                tempcity = tempstr[j]
                if tempcity['city'] == '待确认' or tempcity['city'] == '境外输入':
                    continue
                print(tempstr[j])
                #print('%s 累积确诊:%s 累积死亡:%s 累积治愈:%s 新增:%s ' % (tempcity['city'], tempcity['confirmed'], tempcity['died'], tempcity['crued'], tempcity['confirmedRelative']), end='')
                if  'curConfirm' not in tempcity.keys() or len(tempcity['curConfirm']) == 0:
                    tempcitycurConfirm='0'
                else:
                    tempcitycurConfirm=tempcity['curConfirm']
                if 'died' not in tempcity.keys() or len(tempcity['died']) == 0:
                    tempcitydied = '0'
                else:
                    tempcitydied = tempcity['died']
                if 'confirmedRelative' not in tempcity.keys() or len(tempcity['confirmedRelative']) == 0:
                    tempcityconfirmedRelative='0'
                else:
                    tempcityconfirmedRelative=tempcity['confirmedRelative']
                if 'crued' not in tempcity.keys() or len(tempcity['crued']) == 0:
                    tempcitycrued='0'
                else:
                    tempcitycrued=tempcity['crued']
                tempsql='insert into city_daily_datas(city, confirmedRelative, curConfirm, confirmed, died, cured, pub_date, province) values ("%s", %s, %s, %s, %s, %s, "%s", "%s"' % (tempcity['city'], tempcityconfirmedRelative, tempcitycurConfirm, tempcity['confirmed'], tempcitydied, tempcitycrued, timestr, temp['area']) + ')'
                print(tempsql)
                cursor.execute(tempsql)
                print()
        print('++++++++++++++' * 3)

    # 国内国外数据分隔符    
    print('--------------' * 3)
    print('--------------' * 3)
    print('--------------' * 3)
    print('国外疫情数据：')

    for i in range(34, len(totalInfo)):
        temp = json.loads(totalInfo[i])
        localt = time.localtime(float(temp['relativeTime']))
        timestr = time.strftime("%Y-%m-%d %H:%M:%S", localt)
        print(temp)
        #print('%d  %s 累积确诊:%s 累积死亡:%s 累积治愈:%s 更新时间:%s 新增:%s' % (i+1, temp['area'], temp['confirmed'], temp['died'], temp['crued'], timestr, temp['confirmedRelative']))
        tempsql = 'insert into foreign_daily_datas(died, confirmed, crued, area, curConfirm, confirmedRelative, pub_date) values (%s, %s, %s, "%s", %s, %s, "%s"' % (temp['died'], temp['confirmed'], temp['crued'], temp['area'], temp['curConfirm'], temp['confirmedRelative'], timestr) + ')'
        print(tempsql)
        cursor.execute(tempsql)



    # 已经存入
    # 获得国内国外总体数据
    summaryDataIn = re.findall(r'"summaryDataIn":.*?\}', results[lenOfList])
    summaryDataOut = re.findall(r'"summaryDataOut":.*?\}', results[lenOfList])
    tempdata = re.findall(r'\{"confirmed".*?\}', summaryDataIn[0])
    tempjson = json.loads(tempdata[0])
    temptime=time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(float(tempjson['relativeTime'])))
    tempsql = 'insert into home_realtime_datas(curConfirm, curConfirmRelative, asymptomatic,asymptomaticRelative,unconfirmed,unconfirmedRelative, icu,icuRelative, confirmed,confirmedRelative, overseasInput,overseasInputRelative, cured, curedRelative,died, diedRelative,updatedTime) values (%s, %s, %s, %s, %s, %s, %s, %s, %s,     %s, %s, %s, %s, %s, %s, %s, "%s"' % (tempjson['curConfirm'], tempjson['curConfirmRelative'], tempjson['asymptomatic'], tempjson['asymptomaticRelative'], tempjson['unconfirmed'], tempjson['unconfirmedRelative'], tempjson['icu'], tempjson['icuRelative'], tempjson['confirmed'], tempjson['confirmedRelative'], tempjson['overseasInput'], tempjson['overseasInputRelative'], tempjson['cured'], tempjson['curedRelative'], tempjson['died'], tempjson['diedRelative'], temptime) + ')'
    print(tempsql)
    cursor.execute(tempsql)

    tempdata=re.findall(r'\{"confirmed".*?\}', summaryDataOut[0])
    tempjson = json.loads(tempdata[0])
    temptime=time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(float(tempjson['relativeTime'])))
    tempsql = 'insert into foreign_realtime_datas(confirmed,curConfirm, confirmedRelative, cured, curedRelative, died, diedRelative, updatedTime) values (%s, %s, %s, %s, %s, %s, %s, "%s"' % (tempjson['confirmed'], tempjson['curConfirm'], tempjson['confirmedRelative'], tempjson['cured'], tempjson['curedRelative'], tempjson['died'], tempjson['diedRelative'], temptime) + ')'
    print(tempsql)
    cursor.execute(tempsql)
    db.commit()
    db.close()
    print(tempjson['confirmed'])
    print(tempdata)
    print(summaryDataIn)
    print(summaryDataOut)





# In[33]:





# In[34]:





# In[ ]:




