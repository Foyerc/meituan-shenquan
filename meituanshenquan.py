#!/usr/bin/env python
# -*- coding: utf-8 -*-
#author:fugui

from typing import Text
import urllib.request
import ssl
import json
import os
import sys
import datetime

#定义11点 17点 21点 用于开启server 酱推送
global d_time0,d_time1,d_time2,n_time
d_time0 = datetime.datetime.strptime(str(datetime.datetime.now().date()) + '11:00', '%Y-%m-%d%H:%M')
d_time1 = datetime.datetime.strptime(str(datetime.datetime.now().date()) + '17:00', '%Y-%m-%d%H:%M')
d_time2 = datetime.datetime.strptime(str(datetime.datetime.now().date()) + '21:00', '%Y-%m-%d%H:%M')
n_time = datetime.datetime.now()

 #关闭ssl校验，用于抓包调试请求
ssl._create_default_https_context = ssl._create_unverified_context

#定义短期(半年以上)不会变的量
parActivityId="Gh1tkq-wvFU2xEP_ZPzHPQ"
wm_ctype="mtandroid"
#以下portraitId参数含义未知，用于每日浏览天天神卷30s后可领30豆的请求
portraitId=498



#定义精简通用请求头部
head={"Host": "i.waimai.meituan.com","User-Agent":"MeituanGroup/11.9.208","x-requested-with": "XMLHttpRequest","content-type":"application/x-www-form-urlencoded"} 
#定义美团外卖服务器地址
baseurl=r"https://i.waimai.meituan.com"

#定义全局变量并初始化 以下初始化赋值的变量不要改！！！！
global  wm_latitude,wm_longitude,token,showPriceNumber
showPriceNumber = "1"
wm_latitude =1.0
wm_longitude=1.0
token =""
propId=1.0
exchangeCoinNumber=1.0
serverkey=""
yesornot = ""


#将print内容同步写到output.txt文件
class Logger(object):
    def __init__(self, fileN='Default.log'):
        self.terminal = sys.stdout
        self.log = open(fileN, 'w+')

    def write(self, message):
        '''print实际相当于sys.stdout.write'''
        self.terminal.write(message)
        self.log.write(message)

    def flush(self):
        pass






###获取serverkey
def getserverkey():
    global yesornot
    global serverkey
    if  os.path.exists(r"./serverkey.txt"):
        # file1 = open(r"./token.txt", mode='r',encoding="UTF-8")
        # token = file1.readline()
        # file1.close
        
        yesornot = "y"
        return -1
    else:
        while True:
            try:
                
                print("若您想🙏每天被移动端(如微信)通知，则建议开启通知\n")
                yesornot=input("y")
                print("获取serverkey请访问:https://sct.ftqq.com/\n")
                serverkey=input("SCT55691TNbrxjtkL5YfCegCc2aZNhpDc")
            except:
                pass
            if type(yesornot)==str and (yesornot =="n" or yesornot=='y') and type(serverkey)==str  and serverkey !="":
                break
            
        file =open(r"./serverkey.txt", mode='w+',encoding="UTF-8")
        file.write(serverkey)
        file.close
        return serverkey

#获取token
def gettoken():
    if  os.path.exists(r"./token.txt"):
        file1 = open(r"./token.txt", mode='r',encoding="UTF-8")
        token = file1.readline()
        file1.close
        return token
    else:
        while True:
            
            try:
                print("获取token方法参考readme.md!\n")
                token=input("请输入token:\n")
            except:
                pass
            if type(token)==str  and token !="":
                break
        file =open(r"./token.txt", mode='w+',encoding="UTF-8")
        file.write(token)
        file.close
        return token

#获取经纬度函数并存入当前目录文本(美团活动为随机地点固定半年以上,各地大额红包概率可能不同，若长期小额，可尝试换地址或换号)
def getlatlongitude():
    if os.path.exists(r"./wm_latitudewm_longitude.txt"):
        return -1
    else:
        while True:
            
            try:
                print("若您不知道🙏限时抢红包开放城市，可试各地省会,如成都(30657401,104065827)\n")
                wm_latitude=eval(input("30657401"))
                wm_longitude=eval(input("104065827"))
            except:
                pass
            if type(wm_latitude)==int and type(wm_longitude)==int :
                break
        file =open(r"./wm_latitudewm_longitude.txt", mode='w+',encoding="UTF-8")
        file.write(str(wm_latitude)+"\n"+str(wm_longitude))
        file.close

#定义一个云端查询必中符库中所有的propId 和needNumber 的函数，并传给getpropId_Coninnumber()函数作为用户输入参考提示
def myredbean(token):
    wm_latitude = 1
    wm_longitude = 1
    print("开始执行从美团接口查询proid 和 needNumber参数脚本:\n")
    datas = "parActivityId="+parActivityId+"&wm_latitude="+str(wm_latitude)+"&wm_longitude="+str(wm_longitude)+"&token="+str(token)+"&userPortraitId="+str(portraitId)
    url_drawlottery = baseurl+r"/cfeplay/playcenter/batchgrabred/myRedBean"
    request =urllib.request.Request(url_drawlottery,headers=head,data=datas.encode("utf-8"),method="POST")
    try:
        response = urllib.request.urlopen(request,timeout=5)
        result = response.read().decode("utf-8")
        result2 = json.loads(result)
        cent = 1
        if(result2["code"]==0 and result2["subcode"]==0 and len(result2["data"]["propExchangeRuleInfos"])):
            for k in result2["data"]["propExchangeRuleInfos"]:
                print("第%d类必中符 所需设置propId参数为%d\t所需红包豆数量为:%d\t总量为%d\n"%(cent,k["propId"],k["needNumber"],k["amount"]))
                cent=cent+1
            print("一般这几类必中符金额依次为5元 8元 10元,大概率使用后兑换到20-5，25-8,30-10的红包，建议选择第二类即可\n")
        elif (result2["code"]==1 and result2["subcode"]==-1):
            print("%s,原因:输入token失效或错误 请继续运行程序并输入，脚本将在运行一遍后自动删除异常配置文件!!\n"%(result2["msg"]))
        else:
            print("请求接口失效或参数异常，建议🙏重置参数!\n")
            sys.exit(0)
    except urllib.error.URLError as e:
        if hasattr(e,"code"):
            print("脚本执行失败，错误代码如下:\n")
            print(e.code)
        if hasattr(e,"reason"):
            print(e,"reason")

#定义获得需要兑换的必中符道具类型和兑换所需的豆子
def getpropId_Coinnumber(token):
    if  os.path.exists(r"./propId_Coinnumbe.txt"):
        return -1
    else:
        while True:
            myredbean(token)
            try:
                propId=eval(input("请输入所需要兑换道具的porpId(如2):\n"))
                exchangeCoinNumber=eval(input("请输入propId对应某类必中符所需的豆子数量(如500):\n"))
            except:
                pass
            if type(propId)==int and type(exchangeCoinNumber)==int :
                break
        file =open(r"./propId_Coinnumbe.txt", mode='w+',encoding="UTF-8")
        file.write(str(propId)+"\n"+str(exchangeCoinNumber))
        file.close

#定义从文本文件中获取存入变量的函数,第二次运行时不用输入，若需改变经纬度和token，则直接删除文件即可
def getVar():
    if not os.path.exists(r"./wm_latitudewm_longitude.txt"):
        print("程序运行中配置文件异常,文件或者权限异常,已自动为您删除脚本目录下所有已生成的txt文档并停止程序!\n")
        os.remove(r"./wm_latitudewm_longitude.txt")
        os.remove(r"./token.txt")
        os.remove(r"./propId_Coinnumbe.txt")
        os.remove(r"./serverkey.txt")
        sys.exit(0)
    file1 = open(r"./wm_latitudewm_longitude.txt", mode='r',encoding="UTF-8")
    wm_latitude  = int(file1.readline())
    wm_longitude = int(file1.readline())  
    file1.close()

    file2 = open(r"./token.txt", mode='r',encoding="UTF-8")
    if not os.path.exists(r"./token.txt"):
        print("程序运行中配置文件异常,文件或者权限异常,已自动为您删除脚本目录下所有已生成的txt文档并停止程序!\n")
        os.remove(r"./wm_latitudewm_longitude.txt")
        os.remove(r"./token.txt")
        os.remove(r"./propId_Coinnumbe.txt")
        sys.exit(0)
    token  = file2.readline()
    file2.close()

    if not os.path.exists(r"./propId_Coinnumbe.txt"):
        print("程序运行中配置文件异常,文件或者权限异常,已自动为您删除脚本目录下所有已生成的txt文档并停止程序!\n")
        os.remove(r"./wm_latitudewm_longitude.txt")
        os.remove(r"./token.txt")
        os.remove(r"./propId_Coinnumbe.txt")
        os.remove(r"./serverkey.txt")
        sys.exit(0)
    file3 = open(r"./propId_Coinnumbe.txt", mode='r',encoding="UTF-8")
    propId  = int(file3.readline())
    exchangeCoinNumber = int(file3.readline())  
    file3.close()
    

    return wm_latitude,wm_longitude,token,propId,exchangeCoinNumber

##获得serverkey
def serverkeyvar():
    file = open(r"./serverkey.txt", mode='r',encoding="UTF-8")
    if not os.path.exists(r"./serverkey.txt"):
        print("程序运行中配置文件异常,文件或者权限异常,已自动为您删除脚本目录下所有已生成的txt文档并停止程序!\n")
        os.remove(r"./wm_latitudewm_longitude.txt")
        os.remove(r"./token.txt")
        os.remove(r"./propId_Coinnumbe.txt")
        os.remove(r"./serverkey.txt")
        sys.exit(0)
    serverkey  = file.readline()
    file.close()
    return serverkey

    
#定义获取batchId的函数
def getbatchId(token):
    wm_latitude = getVar()[0]
    wm_longitude = getVar()[1]
    print("### *开始执行获取batchId脚本:* ###\n")
    datas = "parActivityId="+parActivityId+"&wm_ctype="+wm_ctype+"&wm_latitude="+str(wm_latitude)+"&wm_longitude="+str(wm_longitude)+"&token="+token
    url_getbatchId = baseurl+r"/cfeplay/playcenter/batchgrabred/corepage"
    request =urllib.request.Request(url_getbatchId,headers=head,data=datas.encode("utf-8"),method="POST")
    try:
        response = urllib.request.urlopen(request,timeout=5)
        result = response.read().decode("utf-8")
        result2 = json.loads(result)
        # print(result2)
        # print(result2["code"])
        if(result2["code"]==0):
            if "batchId" in result2["data"]:
                print("batchId:%s\n"%(result2["data"]["batchId"]))
                return result2["data"]["batchId"]
            else:
                print("获取batchId失败👀，当前非限时抢红包时间段,无法进行下一步，但已为您签到完毕🙏!\n")
                sys.exit(0)

        elif (result2["code"]==1):
            print("%s,接口需提交的token参数已改变👀,请重新运行一遍脚本！\n"%(result2["msg"]))
            os.remove(r"./wm_latitudewm_longitude.txt")
            os.remove(r"./token.txt")
            os.remove(r"./propId_Coinnumbe.txt")
            os.remove(r"./serverkey.txt")
            sys.exit(0)
        else:
            print("获取batchId错误👀，请检查网络，否则为接口失效！\n")
            sys.exit(0)
        


    except urllib.error.URLError as e:
        if hasattr(e,"code"):
            print(e.code)
        if hasattr(e,"reason"):
            print(e,"reason")



#定义每天七次签到领豆的函数，需传入获取的token
def signForBeans(token):
    print("### *开始执行签到领豆脚本:* ### \n")
    datas = "token="+token
    url_signforbeans = baseurl+r"/cfeplay/playcenter/batchgrabred/drawPoints/v2"
    request =urllib.request.Request(url_signforbeans,headers=head,data=datas.encode("utf-8"),method="POST")
    try:
        response = urllib.request.urlopen(request,timeout=5)
        result = response.read().decode("utf-8")
        result2 = json.loads(result)
        # print(result2)
        # print(result2["code"])
        if(result2["code"]==0):
            print("👴%s\n"%(result2["msg"]))
        elif (result2["code"]==1):
            print("👴未到领取时间或已经领取完了(每天可领7次,每次间隔需半小时\n)！")
        elif (result2["code"]==7):
            print("token已失效，请检查是否已自动删除所有配置文件，若未自动删除，请手动🙏删除所有配置文件并重新运行脚本，最后温馨提示:建议接入server酱通知！\n")
        else:
            print("请求接口失效或网络不佳，请稍后再试!\n")


    except urllib.error.URLError as e:
        if hasattr(e,"code"):
            print("脚本执行失败👀，错误代码如下:\n")
            print(e.code)
        if hasattr(e,"reason"):
            print(e,"reason")


#def 限时抢红包函数
def drawlottery(batchId,token):
    wm_latitude = getVar()[0]
    wm_longitude = getVar()[1]
    print("### *开始执行限时抢天天神券脚本🧧:* ###\n")
    datas = "parActivityId="+parActivityId+"&wm_latitude="+str(wm_latitude)+"&wm_longitude="+str(wm_longitude)+"&token="+token+"&batchId="+batchId+"&isShareLink=true"+"&propType=1"+"&propid=4"
    url_drawlottery = baseurl+r"/cfeplay/playcenter/batchgrabred/drawlottery"
    request =urllib.request.Request(url_drawlottery,headers=head,data=datas.encode("utf-8"),method="POST")
    try:
        response = urllib.request.urlopen(request,timeout=5)
        result = response.read().decode("utf-8")
        result2 = json.loads(result)
        # print(result2)
        # print(result2["code"])
        if(result2["code"]==0):
            print("领取成功!\n提示信息:%s\n红包属性:%s\n使用限制:%s\n红包价值:%s\n红包立即生效时间:%s\n红包剩余有效期:%s分钟\n"%(result2["msg"],result2["data"]["name"],result2["data"]["priceLimitdesc"],result2["data"]["showTitle"],result2["data"]["endTimeDesc"],str(float(result2["data"]["leftTime"])/60000)))
            global showPriceNumber
            showPriceNumber = result2["data"]["showPriceNumber"]
            if int(showPriceNumber)<500:
                print("**当前红包面值为%d元，小于5元，👴将自动执行小额红包转红包豆脚本!!**\n"%(int(showPriceNumber)/100))
            else:
                print("**当前红包面值为%d元，大于等于5元，👴将不会执行小额红包转红包豆脚本!!**\n"%(int(showPriceNumber)/100))
        elif (result2["code"]==1 and result2["subcode"]==3):
            print("%s😅\n"%(result2["msg"]))
        elif(result2["code"]==1 and result2["subcode"]==-1):
            print("token错误或已失效,%s\n"%(result2["msg"]))
        elif (result2["code"]==7):
            print("token已失效，请手动🙏删除所有自动生成的配置文件，并建议接入server酱通知！\n")
        else:
            print("请求接口失效或参数异常，请稍后再试!\n")
    except urllib.error.URLError as e:
        if hasattr(e,"code"):
            print("脚本执行失败，错误代码如下:\n")
            print(e.code)
        if hasattr(e,"reason"):
            
            print(e,"reason")


#定义接受红包函数，获得红包小于5元时，不执行此函数，并调用redtobean函数自动将红包转为红包豆，若两个函数都不执行，在抢红包成功5分钟左右红包会自动发放到账户
def acceptRed(batchId,token):
    wm_latitude = getVar()[0]
    wm_longitude = getVar()[1]
    print("### *开始执行发放天天神券🧧到红包库脚本:* ###\n")
    datas = "parActivityId="+parActivityId+"&wm_latitude="+str(wm_latitude)+"&wm_longitude="+str(wm_longitude)+"&token="+token+"&batchId="+batchId
    url_acceptRed = baseurl+r"/cfeplay/playcenter/batchgrabred/acceptRed"
    request =urllib.request.Request(url_acceptRed,headers=head,data=datas.encode("utf-8"),method="POST")
    try:
        response = urllib.request.urlopen(request,timeout=5)
        result = response.read().decode("utf-8")
        result2 = json.loads(result)
        # print(result2)
        # print(result2["code"])
        if(result2["code"]==0):
            print("👴抢到的红包已经领取成功啦，快去使用吧!\n")
        elif (result2["code"]==1):
            print("%s\n"%(result2["msg"]))
        elif (result2["code"]==7):
            print("token已失效，请手动🙏删除所有自动生成的配置文件，并建议接入server酱通知！\n")
        else:
            print("请求接口失效或参数异常，请稍后再试!\n")
    except urllib.error.URLError as e:
        if hasattr(e,"code"):
            print("脚本执行失败👀，错误代码如下:\n")
            print(e.code)
        if hasattr(e,"reason"):
            
            print(e,"reason")

#定义红包转红包豆函数，将小于5元的红包转为红包豆
def redtobean(batchId,token):
    wm_latitude = getVar()[0]
    wm_longitude = getVar()[1]
    print("### *默认尝试执行面值小于5元🧧自动转红包豆脚本:* ###\n")
    datas = "parActivityId="+parActivityId+"&wm_latitude="+str(wm_latitude)+"&wm_longitude="+str(wm_longitude)+"&token="+token+"&batchId="+batchId
    url_drawlottery = baseurl+r"/cfeplay/playcenter/batchgrabred/redToBean"
    request =urllib.request.Request(url_drawlottery,headers=head,data=datas.encode("utf-8"),method="POST")
    try:
        response = urllib.request.urlopen(request,timeout=5)
        result = response.read().decode("utf-8")
        result2 = json.loads(result)
        # print(result2)
        # print(result2["code"])
        if(result2["code"]==0):
            print("👴小额红包转红包豆成功!\n")
        elif (result2["code"]==1 and result2["subcode"]==12):
            # print("%s😅\n"%(result2["msg"]))
            print("没有待转换的红包😅\n")
        elif (result2["code"]==7):
            print("token已失效，请手动🙏删除所有自动生成的配置文件，并建议接入server酱通知！\n")
        else:
            print("请求接口失效或参数异常，请稍后再试!\n")
    except urllib.error.URLError as e:
        if hasattr(e,"code"):
            print("脚本执行失败，错误代码如下:\n")
            print(e.code)
        if hasattr(e,"reason"):
            
            print(e,"reason")
    



#查询已领取到的天天神券
def querymyreward(token):
    wm_latitude = getVar()[0]
    wm_longitude = getVar()[1]
    print("### *开始执行查询已领天天神券🧧脚本:* ###\n")
    datas = "parActivityId="+parActivityId+"&token="+token
    url_querymyreward = baseurl+r"/cfeplay/playcenter/batchgrabred/myreward"
    request =urllib.request.Request(url_querymyreward,headers=head,data=datas.encode("utf-8"),method="POST")
    try:
        response = urllib.request.urlopen(request,timeout=5)
        result = response.read().decode("utf-8")
        result2 = json.loads(result)
        # print(result2)
        # print(result2["code"])
        if(result2["code"]==0 and len(result2["data"]["myawardInfos"])):
            print("👴开始遍历红包库:\n")
            print("红包库详细信息:\n")
            print("红包库中共有%d个红包\n"%(len(result2["data"]["myawardInfos"])))
            cent=0
            count = 0
            for k in result2["data"]["myawardInfos"]:
                if not k["status"]:
                    print("### *第%d个红包有效!!!!* ###\n红包属性:%s\n使用限制:%s\n红包价值:%s元\n红包剩余有效期%s分钟\n"%(cent+1,k["name"],k["priceLimitdesc"],k["showPriceNumberYuan"],str(float(k["leftTime"])/60000)))
                    print("\n")
                else:
                    count=count+1
                    if cent == 0:
                        print("### *过期红包详情:* ###\n")
                    
                cent=cent+1
            print("总计已领取%d个红包,已过期%d个😅,有效%d个\n"%(cent,count,cent-count))
                
            print("\n")
        elif (result2["code"]==1):
            print("%s\n"%(result2["msg"]))
        elif (result2["code"]==7):
            print("token已失效，请手动🙏删除所有自动生成的配置文件，并建议接入server酱通知！\n")
        else:
            print("请求接口失效或参数异常，请稍后再试!\n")
    except urllib.error.URLError as e:
        if hasattr(e,"code"):
            print("脚本执行失败👀，错误代码如下:\n")
            print(e.code)
        if hasattr(e,"reason"):
            
            print(e,"reason")


#获取每日浏览天天神券奖励的30豆
def sendTaskRedBean(token):
    wm_latitude = getVar()[0]
    wm_longitude = getVar()[1]
    print("### *开始执行领取每日30豆的脚本:* ###\n")
    datas = "parActivityId="+parActivityId+"&wm_latitude="+str(wm_latitude)+"&wm_longitude="+str(wm_longitude)+"&token="+token+"&portraitId="+str(portraitId)
    url_sendTaskRedBean = baseurl+r"/cfeplay/playcenter/batchgrabred/sendTaskRedBean"
    request =urllib.request.Request(url_sendTaskRedBean,headers=head,data=datas.encode("utf-8"),method="POST")
    try:
        response = urllib.request.urlopen(request,timeout=5)
        result = response.read().decode("utf-8")
        result2 = json.loads(result)
        if(result2["status"]==0):
            print("%s\n今天领取成功%d个红包豆，请明日再来！\n"%(result2["msg"],result2["sendBeanCount"]))
        elif (result2["status"]==1):
            print("您今日已领取过😅,%s\n"%(result2["msg"]))
        elif (result2["status"]==-1):
            print("portraitId已失效,%s\n"%(result2["msg"]))
        else:
            print("请求接口失效或参数异常，请稍后再试!\n")
    except urllib.error.URLError as e:
        if hasattr(e,"code"):
            print("脚本执行失败👀，错误代码如下:\n")
            print(e.code)
        if hasattr(e,"reason"):
            print(e,"reason")


#定义每日签到得必中符函数
def doAction(token):
    wm_latitude = getVar()[0]
    wm_longitude = getVar()[1]
    print("### *开始执行每日签到领必中符🧧的脚本:* ###\n")
    datas = "parActivityId="+parActivityId+"&wm_latitude="+str(wm_latitude)+"&wm_longitude="+str(wm_longitude)+"&token="+token+"&action=SiginInGetProp"
    url_doaction = baseurl+r"/cfeplay/playcenter/batchgrabred/doAction"
    request =urllib.request.Request(url_doaction,headers=head,data=datas.encode("utf-8"),method="POST")
    try:
        response = urllib.request.urlopen(request,timeout=5)
        result = response.read().decode("utf-8")
        result2 = json.loads(result)
        if(result2["code"]==0 and result2["data"]["signDays"]!=0):
            print("签到%s\n,截止今日这周已签到%d天"%(result2["msg"],result2["data"]["signDays"]))
        elif (result2["code"]==0 and result2["data"]["signDays"]==0):
            print("您今日已签到，请明天再来!")
        elif (result2["code"]==7):
            print("参数异常或接口已失效")
        else:
            print("请求接口失效或参数异常，请稍后再试!\n")
    except urllib.error.URLError as e:
        if hasattr(e,"code"):
            print("脚本执行失败👀，错误代码如下:\n")
            print(e.code)
        if hasattr(e,"reason"):
            print(e,"reason")


#查看道具库中的必中符记录
def querymyProps(token):
    wm_latitude = getVar()[0]
    wm_longitude = getVar()[1]
    print("### *开始执行查询道具库中必中符🧧详情的脚本:* ###\n")
    datas = "parActivityId="+parActivityId+"&wm_latitude="+str(wm_latitude)+"&wm_longitude="+str(wm_longitude)+"&token="+token
    url_querymyprops = baseurl+r"/cfeplay/playcenter/batchgrabred/myProps"
    request =urllib.request.Request(url_querymyprops,headers=head,data=datas.encode("utf-8"),method="POST")
    try:
        response = urllib.request.urlopen(request,timeout=5)
        result = response.read().decode("utf-8")
        result2 = json.loads(result)
        if(result2["code"]==0 and len(result2["data"])):
            print("👴开始遍历道具库:\n")
            print("道具库详细信息:\n")
            print("红包库中共有%d个必中符道具\n"%(len(result2["data"])))
            cent=0
            count = 0
            for k in result2["data"]:
                if k["status"]==1:
                    print("第%d个必中符道具有效!!!!\n必中符道具id号:%s\n必中符道具属性:%s\n过期时间:%s\n"%(cent+1,k["recordNo"],k["propName"],k["expireTime"]))
                    print("\n")
                else:
                    count=count+1   
                cent=cent+1
            if (count!=0):
                 print("总计%d个必中符道具,已过期%d个😅,有效%d个\n"%(cent,count,cent-count))

            print("\n")
        elif (result2["code"]==7):
            print("参数异常或接口已失效，请手动🙏删除所有自动生成的配置文件，并建议接入server酱通知！")
        else:
            print("必中符道具库为空，👴未帮您领取过道具!\n")
    except urllib.error.URLError as e:
        if hasattr(e,"code"):
            print("脚本执行失败👀，错误代码如下:\n")
            print(e.code)
        if hasattr(e,"reason"):
            print(e,"reason")

#已废弃，直接发送兑换请求即可，不在兑换时间段 subcode 为13
#定义运行时是否能兑换豆子成必中符,目前一直为14点至16点，故不定义此函数，采取每天14点至16点运行此程序时直接尝试兑换
#若需自行获取当前时间段是否可换豆子为道具，则post以下请求即可
# POST /cfeplay/playcenter/batchgrabred/canExchangeCheck HTTP/1.1
# Host: i.waimai.meituan.com
# Content-Length: 82
# User-Agent:MeituanGroup/11.9.208
# x-requested-with: XMLHttpRequest
# content-type: application/x-www-form-urlencoded


# parActivityId=Gh1tkq-wvFU2xEP_ZPzHPQ&wm_latitude=30657401&wm_longitude=104065827







#定义豆子兑换成必中符函数:
def exchange(token):
    wm_latitude = getVar()[0]
    wm_longitude = getVar()[1]
    wm_actual_latitude = str(wm_latitude)
    wm_actual_longitude =str(wm_longitude)
    propId = getVar()[3]
    exchangeCoinNumber = getVar()[4]
    print("### *开始执行每日豆子兑换必中符脚本* ###:\n")
    datas = "wm_actual_longitude="+wm_actual_longitude+"&wm_actual_latitude="+wm_actual_latitude+"&exchangeRuleId=&propId="+str(propId)+"&exchangeCoinNumber="+str(exchangeCoinNumber)+"&parActivityId="+parActivityId+"&wm_ctype="+wm_ctype+"&wm_latitude="+str(wm_latitude)+"&wm_longitude="+str(wm_longitude)+"&token="+token
    url_exchange = baseurl+r"/cfeplay/playcenter/batchgrabred/exchange"
    request =urllib.request.Request(url_exchange,headers=head,data=datas.encode("utf-8"),method="POST")
    try:
        response = urllib.request.urlopen(request,timeout=5)
        result = response.read().decode("utf-8")
        result2 = json.loads(result)
        if(result2["code"]==0 and result2["subcode"]==0):
            print("%s,您设置的兑换成功!😄\n"%(result2["msg"]))
        elif (result2["code"]==1 and result2["subcode"]==13):
            print("%s\n"%(result2["msg"]))
        elif (result2["code"]==1 and result2["subcode"]==-1):
            print("%s\n"%(result2["msg"]))
        elif (result2["code"]==7):
            print("参数异常或接口已失效")
        else:
            print("请求接口失效或参数异常，请稍后再试!\n")
    except urllib.error.URLError as e:
        if hasattr(e,"code"):
            print("脚本执行失败👀，错误代码如下:\n")
            print(e.code)
        if hasattr(e,"reason"):
            print(e,"reason")

###定义查询豆子详情的函数
def myRedBeanRecords(token):
    wm_latitude = getVar()[0]
    wm_longitude = getVar()[1]
    print("### *开始执行查询豆子变化详情参数脚本* ###:\n")
    datas = "parActivityId="+parActivityId+"&wm_latitude="+str(wm_latitude)+"&wm_longitude="+str(wm_longitude)+"&token="+str(token)+"&userPortraitId="+str(portraitId)+"&pageNum=1"
    url_myredbeanRecords = baseurl+r"/cfeplay/playcenter/batchgrabred/myRedBeanRecords"
    request =urllib.request.Request(url_myredbeanRecords,headers=head,data=datas.encode("utf-8"),method="POST")
    try:
        response = urllib.request.urlopen(request,timeout=5)
        result = response.read().decode("utf-8")
        result2 = json.loads(result)
        cent=1
        if(result2["code"]==0 and result2["subcode"]==0 and len(result2["data"]["redBeanRecordInfos"])):
            leftdou= result2["data"]["totalObtainAmount"]-result2["data"]["usedAmount"]-result2["data"]["expiredAmount"]
            print("**总获得红包豆:%d,已使用红包豆:%d,已过期红包豆:%d,剩余可用红包豆:%d**\n"%(result2["data"]["totalObtainAmount"],result2["data"]["usedAmount"],result2["data"]["expiredAmount"],leftdou))
            for k in result2["data"]["redBeanRecordInfos"]:
                print("exchangeTime:%s\texchangeMessage:%s\texchangeNumber:%s\n"%(k["exchangeTime"],k["exchangeMessage"],k["exchangeNumber"]))
                cent=cent+1
                if(cent>10):
                    break  
            print("*只显示最近十条红包豆的变化* \n")
        elif (result2["code"]==1 and result2["subcode"]==-1):
            print("%s\n"%(result2["msg"]))
        else:
            print("请求接口失效或参数异常，建议🙏重置参数!\n")
    except urllib.error.URLError as e:
        if hasattr(e,"code"):
            print("脚本执行失败👀，错误代码如下:\n")
            print(e.code)
        if hasattr(e,"reason"):
            print(e,"reason")    

#定义查询红包池函数
def queryredpool(token):
    wm_latitude = getVar()[0]
    wm_longitude = getVar()[1]
    print("### *开始执行查询红包池详情脚本* ###:\n")
    datas = "parActivityId="+parActivityId+"&wm_latitude="+str(wm_latitude)+"&wm_longitude="+str(wm_longitude)+"&token="+str(token)+"&wm_ctype="+wm_ctype
    url_myredbeanRecords = baseurl+r"/cfeplay/playcenter/batchgrabred/corepage"
    request =urllib.request.Request(url_myredbeanRecords,headers=head,data=datas.encode("utf-8"),method="POST")
    try:
        response = urllib.request.urlopen(request,timeout=5)
        result = response.read().decode("utf-8")
        result2 = json.loads(result)

        if(result2["code"]==0 and result2["subcode"]==0 and len(result2["data"]["awardInfos"])):
            for k in result2["data"]["awardInfos"]:
                print("**%s元红包池总量:%d,剩余%s张**\n"%(k["showPriceNumberYuan"],k["sendStock"],k["leftStock"]))
        elif (result2["code"]==1 and result2["subcode"]==-1):
            print("token失效,导致获取活动信息失败！%s\n"%(result2["msg"]))
        else:
            print("请求接口失效或参数异常，建议🙏重置参数!\n")
    except urllib.error.URLError as e:
        if hasattr(e,"code"):
            print("脚本执行失败👀，错误代码如下:\n")
            print(e.code)
        if hasattr(e,"reason"):
            print(e,"reason")    
   


#定义server 酱的消息推送方法
def serverjiang():
    serverkey = serverkeyvar()
    if not os.path.exists(r"./output.txt"):
        print("output.txt文件异常,推送退出！🙌")
        return -1
    file4= open(r"./output.txt", mode='r',encoding="UTF-8")
    pp =''
    message = str(file4.read())

    file4.close
    

    pushurl="https://sctapi.ftqq.com/"
    head_server = head={"Host": "sctapi.ftqq.com","User-Agent":"Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/94.0.4606.81 Mobile Safari/537.36","content-type":"application/x-www-form-urlencoded"}
    url_serverkey = pushurl+serverkey+".send"
    print("### *开始执行server酱推送脚本:* ###\n")
    datas=bytes(urllib.parse.urlencode({"title":"天天神券推送","desp":message}),encoding="UTF-8")
    request =urllib.request.Request(url_serverkey,headers=head,data=datas,method="POST")
    try:
        response = urllib.request.urlopen(request,timeout=30)
        result = response.read().decode("utf-8")
        result2 = json.loads(result)
        if(result2["code"]==0) :
            pushid = result2["data"]["pushid"]
            readkey = result2["data"]["readkey"]
            url_checkurl = pushurl+"push?id="+pushid+"&readkey="+readkey
            request2 = urllib.request.Request(url_checkurl,headers=head_server,data=datas)
            try:
                response2 = urllib.request.urlopen(request2,timeout=10)
                text=json.loads(response2.read().decode("utf-8"))
                if(text["data"]["title"] =="天天神券推送"):
                    print("server酱推送成功😄！请在移动设备端查看\n")
                else:
                    print("server酱推送失败👀，请检查serverkey是否正确！\n")

            except urllib.error.URLError as e2:
                if hasattr(e2,"code"):
                    print("脚本执行失败👀，错误代码如下:\n")
                print(e2.code)
                if hasattr(e2,"reason"):
                    print(e2,"reason") 
        else:
            print("请求接口失效或参数异常，建议重置参数!\n")
    except  urllib.error.URLError as e:
        if  hasattr(e,"code"):
            print("脚本执行失败，错误代码如下:\n")
            print(e.code)
        if hasattr(e,"reason"):
            print(e,"reason") 



def main():
    temp = sys.stdout
    getserverkey()
    token = gettoken()
    getlatlongitude()
    getpropId_Coinnumber(token)
    sys.stdout = Logger('./output.txt')
    token = getVar()[2]
    signForBeans(token)
    queryredpool(token)
    batchId = getbatchId(token)
    drawlottery(batchId,token)
    if(int(showPriceNumber)<500):
        redtobean(batchId,token)
    else:
        acceptRed(batchId,token)
    querymyreward(token)
    sendTaskRedBean(token)
    doAction(token)
    querymyProps(token)
    exchange(token)
    myRedBeanRecords(token)
    sys.stdout = temp
    if(yesornot == "y"):
        if ((n_time >d_time2)) or ((n_time<d_time2) and (n_time>d_time1)) or ((n_time<d_time1) and (n_time>d_time0)):
            serverjiang()
        else:
            print("当前时间段非抢红包时间,默认关闭server酱推送以节约server酱每日5条推送的限额！")
    else:
        print("您已默认关闭开启server酱推送！\n温馨小提示:微信团队已放弃甜糖推送接口！\n建议把server酱推送方式配置为企业微信推送！\n")
    


if __name__ == "__main__":
    main()
