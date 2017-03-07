#!/usr/bin/env python
# coding: utf-8

from crawlerInfoq import *
import json

if __name__ == '__main__':
    crawler = crawlerInfoq()
    cnt = 0
    categoryIndex = 0
    category = crawler.category[categoryIndex]
    page = -1
    while (True):
        page = page + 1
        articles = crawler.getTargetItems(category,cnt)
        cnt += len(articles)
        if len(articles) <= 0:
            print('爬取%s结束！' % (category))
            if(categoryIndex < len(crawler.category)):
                categoryIndex = categoryIndex + 1
                category = crawler.category[categoryIndex]
                continue
            else:
                break;
            
        print('爬取%s类第%s页,当前页%s条，已爬取%s条数据' % (category, page, len(articles), cnt))
    
        jsonInfos,jsonErrorInfo = crawler.formatNewsInfo(articles)
        
        crawler.writeToFile(json.dumps(jsonInfos,ensure_ascii=False,indent=2),category)
        
        if len(jsonErrorInfo) > 0:
            crawler.writeToFile(json.dumps(jsonErrorInfo,ensure_ascii=False,indent=2),'errorInfo')
