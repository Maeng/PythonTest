
# coding: utf-8

import xml.etree.ElementTree as ET
from datetime import datetime, date, time
import re
import pandas as pd
import random

def refineDate(strIn) :
    strOut = ''
    if len(strIn) == 4 :
        #to YYYY-MM-DD
        return date(int(strIn[1]), int(strIn[2]), int(strIn[3])).isoformat()
    else :
        if "[[" in strIn :
            strIn.replace("[[", "").replace("]]", "")
            digitList = [int(s) for s in strIn.split() if s.isdigit()]
            year = digitList[0]
            month = digitList[1]
            day = digitList[2]
            
            return date(year, month, day).isoformat()
        else : 
            year = ''.join(strIn[0:4])
            month = ''.join(strIn[4:6])
            day = ''.join(strIn[6:8])
            
            return date(year, month, day).isoformat()
                
    return strOut

def refineHeight(strIn) :
    if strIn :
        return int(strIn.replace("cm", ""))
    else :
        return 0
    
#if value have <ref ~ split if
def removeRef(value) :
    return value.split("<ref", 1)[0]

#check page Element include text with "축구 선수 정보"
def checkTmplName(buf):
    root = ET.fromstring(buf)
    
    #no text tag in page
    if root.find("revision").find("text") == None :
        return False
    else :
        getTxt = root.find("revision").find("text").text
        if getTxt is None :
            return False
        
        if "{{축구 선수 정보" in getTxt :
            return True
        else : return False

#only get Date of Birth, Height, Team
def makeBrckDict(txt):
    rtnDic = {}
    
    key = ""
    value = ""
    startBrck = False
    cntCheck = 0
    
    for line in txt.splitlines() :
        if not startBrck :
            if line.startswith("{{축구 선수 정보") :
                startBrck = True
            else : 
                continue
        
        #information of soccer player bracket started
        else :
            if line.startswith("|"): 
                if line[1:].startswith("출생일") :
                    key = "출생일"
                    value = line[1:].split("=", 1)[1]
                    
                    value = value.replace("{{","").replace("}}","")
                    value = removeRef(value)
                    value = value.split("|")
                    rtnDic[key] = value
                    
                    key = None
                    value = None
                    cntCheck += 1
                    
                elif line[1:].startswith("키") :
                    key = "키"
                    value = line[1:].split("=", 1)[1]
                    value = removeRef(value)
                    rtnDic[key] = value
                    
                    key = None
                    value = None
                    cntCheck += 1
                
                elif line[1:].startswith("현 소속팀") :
                    key = "현 소속팀"
                    if "=" in line[1:] : 
                        value = line[1:].split("=", 1)[1]

                        value = value.replace("[[","").replace("]]","")
                        value = value.split("|")
                        rtnDic[key] = value[0]

                    else : 
                        rtnDic[key] = line[1:]
                    
                    key = None
                    value = None
                    cntCheck += 1
                
                else : 
                    continue
                    
            if cntCheck == 3 :
                return rtnDic
                
    return rtnDic
        
    
def outRndPlayer(data) :
    df = pd.DataFrame(data)
    writer = pd.ExcelWriter('output_test3.xlsx', engine='xlsxwriter')
    df.to_excel(writer, sheet_name='Sheet1')
    writer.save()

inputbuf = ''
with open('kowiki-20180401-pages-articles-multistream.xml','r', encoding="UTF8") as inputfile:
    append = False
    totalList = []
    totalNum = 0
    for line in inputfile:
        if '<page>' in line:
            inputbuf = line
            append = True
        elif '</page>' in line:
            inputbuf += line
            append = False
            
            if checkTmplName(inputbuf) :
                
                #get page as root
                root = ET.fromstring(inputbuf)
                pageTitle = root.find("title").text
                pageId = root.find("id").text
                revision = root.find("revision")
                
                dic = makeBrckDict(revision.find("text").text)
                if dic:
                    totalList.insert(totalNum, [pageId, pageTitle, dic.get("출생일"), dic.get("키"), dic.get("현 소속팀")])
                    totalNum += 1
                    
            else : 
                pass
            
            inputbuf = None
            del inputbuf
                
        elif append:
            inputbuf += line
    
    #random pick 10 players
    numList = random.sample(range(len(totalList)), 10)

    #lists
    teamList = []
    heightList = []
    birthList = []
    tempNameList = ["축구 선수 정보"] * 10
    titleList = []
    idList = []
    
    for i in numList:
        print(list[i])
        idList.append(list[i][0])
        titleList.append(list[i][1])
        birthList.append(refineDate(list[i][2]))
        heightList.append(refineHeight(list[i][3]))
        teamList.append(list[i][4])
    
    data = {"Team" :teamList, "Height" :heightList, "Date of Birth" :birthList,
            "Template Name" :tempNameList, "Page Title" :titleList, "Page ID" :idList}
    
    outRndPlayer(data)
            



