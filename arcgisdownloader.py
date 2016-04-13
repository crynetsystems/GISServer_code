#!/usr/bin/python
# encoding=utf-8
# Filename: arcgisdownloader.py
import math
import os
import urllib2
import multiprocessing.dummy
from time import sleep
from conn import Mongo;
maxthreads = 1000;
maxlinksize = 3000;
dir_path='/var/usb/download_tiles/'

def num2deg(xtile, ytile, zoom):
    n = 2.0 ** zoom
    lon_deg = xtile / n * 360.0 - 180.0
    lat_rad = math.atan(math.sinh(math.pi * (1 - 2 * ytile / n)))
    lat_deg = math.degrees(lat_rad)
    return (lat_deg, lon_deg)

def deg2num(lat_deg, lon_deg, zoom):
    lat_rad = math.radians(lat_deg)
    n = 2.0 ** zoom
    xtile = int((lon_deg + 180.0) / 360.0 * n)
    ytile = int((1.0 - math.log(math.tan(lat_rad) + (1 / math.cos(lat_rad))) / math.pi) / 2.0 * n)
    return (xtile, ytile)

def lla2url(lat,lon,zoom):
    (x,y)=deg2num(lat,lon,zoom)
    map_level='&level=%d'%zoom
    map_row='&row=%d'%y
    map_column='&column=%d'%x
    source='http://services.arcgisonline.com/ArcGIS/services/World_Imagery/MapServer\?mapname=Layers&layer=_alllayers'+map_level+map_row+map_column
    return source

#google tile
def xyz2url(x,y,zoom):
    map_level='&level=%d'%zoom
    map_row='&row=%d'%y
    map_column='&column=%d'%x
    source='http://services.arcgisonline.com/ArcGIS/services/World_Imagery/MapServer\?mapname=Layers&layer=_alllayers'+map_level+map_row+map_column
    return source

def xyz2path(x,y,zoom):
    s_zoom='%d/'%zoom
    s_x='%d/'%x
    s_y='%d'%y
    return dir_path+s_zoom+s_x+s_y+'.jpg'


def DownloadImage(image_url,path):
    try:
        f=urllib2.urlopen(image_url,timeout = 5).read()
    except:
        return -1
    fw = open(path, 'wb')
    fw.write(f)
    fw.close()
    return 1

def DownloadTile(zoom,x,y,count):
        sourceurl=xyz2url(x,y,zoom)
        path=xyz2path(x,y,zoom)
        if (DownloadImage(sourceurl,path)==-1):
            retrun 0;
        else:
            retrun 1;

def InsertURLInfo(linkQueue):
    for zoom in range(0,10):
        this_xy=2**(zoom)
        for x in range(0,this_xy):
            try:
                s_zoom='%d/'%zoom
                s_x='%d'%x
                os.makedirs(dir_path+s_zoom+s_x)
            except:
                pass
            for y in range(0,this_xy):
                
                isWaiting = 0;
                while isWaiting == 0:
                    try:
                        linkQueue.put_nowait(dict(x=x,y=y,z=zoom,count=0))
                        isWaiting = 1;
                    except:
                        sleep(1);


def downLoadImg(linkQueue):
    while linkQueue.qsize() > 0 or errorQueue.qsize() > 0 :
        if isErrorFull:
            current_Quene = errorQueue;
        else:
            current_Quene = linkQueue;
        isGet = 0;
        while isGet == 0:
            try:
                urlInfo = current_Quene.get_nowait();
                if urlInfo['count'] == 5:
                    mongo.SaveURLInfo(urlInfo);
                    continue;
                if DownloadTile(urlInfo['z'],urlInfo['x'],urlInfo['y'],urlInfo['count']) == 0:
                    errorQueue.put(dict(x=x,y=y,z=zoom,count=count+1));
                isGet = 1;
            except:
                sleep(1);

def ProcError():
    while True:
        if errorQueue.qsize >= 10000:
            isErrorFull = True;
        if errorQueue.qsize == 0:
            isErrorFull = False;
        sleep(30);

if __name__ == '__main__':
    mongo = Mongo('127.0.0.1','errorInfos','errorInfo');
    if mongo.OpenConn() != True:
        print "connect initialize failed."
    linkQueue = multiprocessing.dummy.Queue(maxlinksize);
    errorQueue = multiprocessing.dummy.Queue();
    isErrorFull = False;
    cacheURL = multiprocessing.dummy.Process(target = InsertURLInfo,args = (linkQueue,))
    cacheURL.start();
    sleep(10);
    print "begin download."
    for i in range(0,maxthreads):
        download = multiprocessing.dummy.Process(target = downLoadImg,args = (linkQueue,))
        download.start();
        sleep(0.1);
    sleep(60);
    procErrorQueue = multiprocessing.dummy.Process(target = ProcError)
    procErrorQueue.start();
    print "finish."
