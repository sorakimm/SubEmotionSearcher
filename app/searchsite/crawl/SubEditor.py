# -*- coding:utf-8 -*-
import re
from searchsite.crawl.mylogging import MyLogger

tokenizer = None
tagger = None

subEditorLogFile = 'log/subEditor.log'
subEditorLogger = MyLogger(subEditorLogFile)

pStyle1 = re.compile('<br>', re.IGNORECASE | re.MULTILINE | re.DOTALL)
pStyle2 = re.compile('<font color=.*?>', re.IGNORECASE)
pStyle3 = re.compile('</font>', re.IGNORECASE)
pStyle4 = re.compile('<HEAD(.*?)>(.*?)</HEAD>', re.IGNORECASE | re.MULTILINE | re.DOTALL)
pStyle5 = re.compile('<!--(.*?)-->', re.IGNORECASE | re.MULTILINE | re.DOTALL)
pStyle6 = re.compile('<br>', re.IGNORECASE | re.MULTILINE | re.DOTALL)
pStyle7 = re.compile('<SAMI>', re.IGNORECASE | re.MULTILINE | re.DOTALL)
pStyle8 = re.compile('<BODY>', re.IGNORECASE | re.MULTILINE | re.DOTALL)
pStyle9 = re.compile('</SAMI>', re.IGNORECASE | re.MULTILINE | re.DOTALL)
pStyle10 = re.compile('</BODY>', re.IGNORECASE | re.MULTILINE | re.DOTALL)
pStyle11 = re.compile('<i>', re.IGNORECASE | re.MULTILINE | re.DOTALL)
pStyle12 = re.compile('</i>', re.IGNORECASE | re.MULTILINE | re.DOTALL)
pStyle13 = re.compile(r'<SYNC Start=\d+><P Class=KR.*>&nbsp;')
pStyle14 = re.compile(r'<SYNC Start=\d+><P Class=EN.*>&nbsp;')
pStyle15 = re.compile(r'&nbsp;', re.IGNORECASE | re.MULTILINE | re.DOTALL)
pStyle16 = re.compile(r' \r\n{1}$\r\n', re.IGNORECASE | re.MULTILINE | re.DOTALL)
pStyle17 = re.compile(r' \r\n{2,}', re.IGNORECASE | re.MULTILINE | re.DOTALL)
pStyle18 = re.compile(r'\n$', re.IGNORECASE | re.MULTILINE | re.DOTALL)
pStyle19 = re.compile(r'[ ]{2,}', re.MULTILINE | re.DOTALL)
pStyle20 = re.compile(r'\r\n', re.IGNORECASE | re.MULTILINE | re.DOTALL)
pStyle21 = re.compile(r'\w+: ', re.IGNORECASE | re.MULTILINE | re.DOTALL)
pStyle22 = re.compile(r'[_-]', re.IGNORECASE | re.MULTILINE | re.DOTALL)
pStyle23 = re.compile(r'\(\w+\)', re.IGNORECASE | re.MULTILINE | re.DOTALL)


def checkKREN(contents):
    "다운받은 smi 파일이 정상인지 체크"
    subEditorLogger.debug("checkKREN")

    pKRCC = re.compile(r'<P Class=K(R.*|OR)>', re.IGNORECASE)
    pENCC = re.compile(r'<P Class=EN.*>', re.IGNORECASE)

    try:
        if (bool(re.search(pKRCC, contents))):
            if (bool(re.search(pENCC, contents))):
                return True

    except Exception as e:
        subEditorLogger.error(e)
        return False

def dictIntersect(dict1, dict2):
    comm_keys = dict1.keys()
    comm_keys &= dict2.keys()

    result = {key:(dict1[key], dict2[key]) for key in comm_keys}
    return result



def sortTXT(contents):
    "smi파일내용 정렬"
    subEditorLogger.debug("sortTXT")

    contents = pStyle1.sub(' ', contents)
    contents = pStyle2.sub(' ', contents)
    contents = pStyle3.sub(' ', contents)
    contents = pStyle4.sub('', contents)
    contents = pStyle5.sub('', contents)
    contents = pStyle6.sub(' ', contents)
    contents = pStyle7.sub('', contents)
    contents = pStyle8.sub('', contents)
    contents = pStyle9.sub('', contents)
    contents = pStyle10.sub('', contents)
    contents = pStyle11.sub('', contents)
    contents = pStyle12.sub('', contents)
    contents = pStyle13.sub('', contents)
    contents = pStyle14.sub('', contents)
    contents = pStyle15.sub('', contents)
    contents = pStyle16.sub('', contents)
    contents = pStyle17.sub(r'\r\n', contents)
    contents = pStyle18.sub('', contents)
    contents = pStyle19.sub(' ', contents)
    contents = pStyle20.sub(' ', contents)
    contents = pStyle21.sub('', contents)
    contents = pStyle22.sub('', contents)
    contents = pStyle23.sub('', contents)

    contentsEN = {}
    contentsKR = {}
    pStyleEN = re.compile(r'<SYNC Start=(\d+)><P Class=EN.*?>(.+?)<', re.IGNORECASE | re.MULTILINE | re.DOTALL)
    pStyleKR = re.compile(r'<SYNC Start=(\d+)><P Class=K.*?>(.+?)<', re.IGNORECASE | re.MULTILINE | re.DOTALL)
    contentsEN = dict(pStyleEN.findall(contents))
    contentsKR = dict(pStyleKR.findall(contents))

    contentsDict = {}
    contentsDict = dictIntersect(contentsEN, contentsKR)

    return list(contentsDict.values())


