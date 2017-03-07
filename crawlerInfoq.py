#!/usr/bin/env python
# coding: utf-8

import requests
from bs4 import BeautifulSoup

class crawlerInfoq:
    def __init__(self):
        self.baseUrl = 'http://www.infoq.com/cn'
        self.category = ['news','articles','presentations','interviews','minibooks']
        self.categoryClassName = {
            'news': 'news_type_block',
            'articles': ['news_type1','news_type2'],
            'presentations': 'news_type_video',
            'interviews': 'news_type_video',
            'minibooks': 'ebook_list',
        }
    
    def getTargetItems(self,category,cnt=0):
        res = requests.get( '%s/%s/%s' % (self.baseUrl, category, cnt))
        htmlSoup = BeautifulSoup(res.text,'html5lib')
        
        curClass = self.categoryClassName.get(category)
        
        items = []
        if isinstance(curClass,list):
            items = items + sum([htmlSoup.findAll(class_= klass) for klass in curClass],[])
        else:
            items = htmlSoup.findAll(class_=curClass)
        
        return items
    
    # 解析
    def formatNewsInfo(self,infosSoup):
        jsonInfos = []
        jsonErrorInfo = []
        for item in infosSoup:
            try:
                jsonItem = {}
                # 标题
                titleSoup = item.select('h2 > a')
                jsonItem['title'] = titleSoup[0]['title']
                jsonItem['titleLink'] = titleSoup[0]['href']
                # 作者
                authorSoup = item.find(class_='f_taxonomyEditor')
                jsonItem['author'] = authorSoup.string.strip()
                jsonItem['authorLink'] = authorSoup['href']
                # 译者
                authorTransSoup = item.find(class_='f_taxonomyTranslator')
                if authorTransSoup:
                    jsonItem['authorTrans'] = authorTransSoup.string.strip()
                    jsonItem['authorTransLink'] = authorTransSoup['href']
                # 发布时间
                timeSoup = item.find(class_='author')
                jsonItem['time'] = timeSoup.getText().strip().split('\n')[-1].strip()
                # 摘要
                descSoup = item.find('p')
                jsonItem['description'] = descSoup.getText().strip()
                
                jsonInfos.append(jsonItem)
            except Exception as e:
                print(e)
                jsonErrorInfo.append(item) 
        return (jsonInfos,jsonErrorInfo)
    
    def writeToFile(self,data,fileName):
        with open('%s.json' % (fileName), 'a') as f:
            f.write(data)
        
        
        
        
        
        
        
        
        