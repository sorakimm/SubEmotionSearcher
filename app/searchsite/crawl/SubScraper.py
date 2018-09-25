# -*- coding:utf-8 -*-
from bs4 import BeautifulSoup
import re
import requests
from requests.compat import urljoin
from searchsite.crawl.mylogging import MyLogger
from searchsite.crawl import SubEditor

subScrapLogFile = 'log/subScrap.log'
subScrapLogger = MyLogger(subScrapLogFile)


gomBaseUrl = 'http://gom.gomtv.com'



def getHtml(url):
   html = ""
   resp = requests.get(url)
   if resp.status_code == 200:
      html = resp.text
   return html


class gomSubScraper():
    def __init__(self):
        self.lastPage = 1
        self.dbTuple = tuple()
        self.gomKorEnBoardUrl = "http://gom.gomtv.com/main/index.html?ch=subtitles&pt=l&menu=subtitles&lang=3&page="

    def getLastPage(self):
        self.getGomLastBoard()
        return self.lastPage


    def getGomLastBoard(self):
        subScrapLogger.debug("getGomLastBoard")
        try:
            gomFirstBoardHtml = getHtml(self.gomKorEnBoardUrl)
            firstPageBSObj = BeautifulSoup(gomFirstBoardHtml, "html.parser")
            self.lastPage = int(firstPageBSObj.find('a', {'class' : 'next_last'}).get('onclick'))
        except Exception as e:
            subScrapLogger.error(e)


    def getTitlesOfPage(self, _pageNum):
        subScrapLogger.debug("getTitlesOfPage")
        gomPageHtml = getHtml(self.gomKorEnBoardUrl + _pageNum)
        bsObj = BeautifulSoup(gomPageHtml, "html.parser")
        titleList = []
        for titleLink in bsObj.findAll("a", href=re.compile("/main/index.html\?ch=subtitles&pt=v&menu=subtitles&seq=\d+&prepage=\d&md5key=&md5skey=")):
            titleList.append(urljoin(gomBaseUrl, titleLink.get('href')))

        return titleList


    def getSortSmiList(self, _pageNum):
        subScrapLogger.debug("getSortSmiList")

        downPattern = re.compile("\'(.+?)\'")
        gom_boardUrl = 'http://gom.gomtv.com/main/index.html/'
        gom_DownCHPT_Url = 'ch=subtitles&pt=down&'
        titleUrlList = self.getTitlesOfPage(_pageNum)
        sortSmiList = []

        for titleUrl in titleUrlList:
            downHtml = getHtml(titleUrl)
            bsObj= BeautifulSoup(downHtml, 'html.parser')
            downSeq = downPattern.findall(bsObj.find('a', {'class' : 'btn_type3 download'}).get('onclick'))

            intSeq = downSeq[0]
            capSeq = downSeq[1]
            fileName = downSeq[2]

            downCommand = fileName + '?' + gom_DownCHPT_Url + 'intSeq=' + intSeq + '&capSeq=' + capSeq
            fullDownUrl = urljoin(gom_boardUrl, downCommand)
            smi = getHtml(fullDownUrl)

            smiDict = {}
            if SubEditor.checkKREN(smi) == True:
                subScrapLogger.info(fileName + " sortTXT start")
                smiDict[fileName] = SubEditor.sortTXT(smi)
                sortSmiList.append(smiDict)
            else:
                subScrapLogger.info(fileName + " is wrong file")

        return sortSmiList
        

