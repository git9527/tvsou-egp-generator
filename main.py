#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from bs4 import BeautifulSoup
import requests
import datetime
from pytz import timezone
import os

def writeLine(lines):
    with open("/tmp/epg.xml", "a") as file:
        file.writelines(lines)
        file.write("\n")


def generateChannel(channelId, channelName):
    writeLine('<channel id="' + channelId + '"><display-name lang="zh">' + channelName + '</display-name></channel>')


def generateProgram(channelId, channelName):
    url = "https://tvsou.com/epg/" + channelId
    r = requests.get(url)
    html = r.text
    bf = BeautifulSoup(html, features="html.parser")
    firstTable = bf.findAll('table')[0]
    contents = [a.contents[0] for a in firstTable.findAll('a')]
    shows = []
    for index in range(0, len(contents) // 2):
        shows.append([contents[index * 2].replace(':', ''), contents[index * 2 + 1]])
    today = datetime.datetime.now(timezone('Asia/Shanghai')).strftime('%Y%m%d')
    print('Channel:', channelName, 'shows:', shows)
    for index, val in enumerate(shows):
        stop = shows[index + 1][0] if (index + 1 != len(shows)) else '2359'
        writeLine('<programme start="' + today + val[
            0] + '00 +0800" stop="' + today + stop + '00 +0800" channel="' + channelId + '">')
        writeLine('<title lang="zh">' + val[1] + '</title>')
        writeLine('<desc lang="zh">  </desc>')
        writeLine('</programme>')

if __name__ == "__main__":
    pairs = os.getenv('PAIRS').split(',')
    open("/tmp/epg.xml", "w").close()
    writeLine('<?xml version="1.0" encoding="UTF-8"?>')
    writeLine('<tv generator-info-name="git9527" generator-info-url="https://github.com/git9527/tvsou-epg-generator">')
    print('current time in Shanghai:', datetime.datetime.now(timezone('Asia/Shanghai')).strftime('%Y%m%d-%H%M%S'))
    print('generate epg for pairs:', pairs)
    for pair in pairs:
        channel = pair.split(':')
        generateChannel(channel[0], channel[1])
        generateProgram(channel[0], channel[1])
    writeLine('</tv>')
