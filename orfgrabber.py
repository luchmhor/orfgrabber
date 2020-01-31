#!/usr/bin/env python

from bs4 import BeautifulSoup
import urllib2
import datetime
import re
import os
import time

WRITE_FILE_PATH='/media/csabi/Elements/images/youtube/ORF/archive/dl.sh'
SOURCE_LOCAL=1
SOURCE_INTERNET=2

def generateDownloadFileGenres(fileNameOrURL,source):
    if source == SOURCE_LOCAL:
        file = open(fileNameOrURL, 'r')
    elif source == SOURCE_INTERNET:
        file = urllib2.urlopen(fileNameOrURL)

    wholeFile = file.read()
    file.close()        
    
    writeFile = open(WRITE_FILE_PATH,'a')
    bsObject=BeautifulSoup(wholeFile)
    externalLinks=bsObject.findAll("a",class_="html-attribute-value html-external-link")
    ulElements=bsObject.findAll("ul",class_="latest_episodes")
    
    writeString=''
    for ulElement in ulElements:
        if len(ulElement.findAll("a")):
            link=(ulElement.findAll("a")[0]).get('href')
            match=re.search("(\d{4})-(\d{2})-(\d{2})",(ulElement.findAll("time",class_="meta_headline")[0]).get("datetime"))
            newdate=match.group(1)+match.group(2)+match.group(3)
            match=re.search("http:\/\/tvthek.orf.at\/program\/(.*?)\/(\d+?)\/(.*?)\/((\d+))",link) #non-greedy machen # ? scheint zu funktionieren
            writeString+='#' + match.group(1)+' '+match.group(2)+' '+match.group(3)+' '+match.group(4)+'\n'
            writeString+='mkdir -p '+newdate+' ; cd '+newdate+' ; mkdir -p '+match.group(1)+' ; cd '+match.group(1)+' ; youtube-dl -t -i '+link+' ; wget '+link+' ; cd ../..\n'
    print writeString
    writeFile.write(writeString)
    writeFile.close()

def generateDownloadFileMostViewedTips(fileNameOrURL,source):
    if source == SOURCE_LOCAL:
        file = open(fileNameOrURL, 'r')
    elif source == SOURCE_INTERNET:
        file = urllib2.urlopen(fileNameOrURL)

    wholeFile = file.read()
    file.close()        
        
    writeFile = open(WRITE_FILE_PATH,'a')    
    bsObject=BeautifulSoup(wholeFile)
    articles=bsObject.findAll("article",class_="item")
    
    writeString=''
    for article in articles:
        link=(article.findAll("a")[0]).get('href')
        match=re.search("(\d{2}).(\d{2}).(\d{4})",(article.findAll("time",class_="meta_date")[0]).contents[0])
        newdate=match.group(3)+match.group(2)+match.group(1)
        match=re.search("http:\/\/tvthek.orf.at\/program\/(.*?)\/(\d+?)\/(.*?)\/((\d+))",link) #non-greedy machen # ? scheint zu funktionieren
        writeString+='#' + match.group(1)+' '+match.group(2)+' '+match.group(3)+' '+match.group(4)+'\n'
        writeString+='mkdir -p '+newdate+' ; cd '+newdate+' ; mkdir -p '+match.group(1)+' ; cd '+match.group(1)+' ; youtube-dl -t -i '+link+' ; wget '+link+' ; cd ../..\n'
    print writeString
    writeFile.write(writeString)
    writeFile.close()

if os.path.exists(WRITE_FILE_PATH):
    mtime=os.path.getmtime(WRITE_FILE_PATH)
    os.rename(WRITE_FILE_PATH,WRITE_FILE_PATH+time.strftime("%Y%m%d%H%M",time.localtime(mtime)))

generateDownloadFileGenres('http://tvthek.orf.at/programs/genre/Dokumentation/1173',SOURCE_INTERNET)
generateDownloadFileGenres('http://tvthek.orf.at/programs/genre/Comedy-DIENACHT/2703835',SOURCE_INTERNET)

generateDownloadFileMostViewedTips('http://tvthek.orf.at/most_viewed',SOURCE_INTERNET)
generateDownloadFileMostViewedTips('http://tvthek.orf.at/tips',SOURCE_INTERNET)