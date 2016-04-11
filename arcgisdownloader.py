#!/usr/bin/python
# encoding=utf-8
# Filename: arcgisdownloader.py
import math
import os
import urllib2
import multiprocessing.dummy
from time import sleep
maxthreads = 500;
maxlinksize = 2000;
dir_path='/var/usb/download_tiles/'
test_id=0
thread_num=0
max_downloadFrequency = 20

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
    if os.path.isfile(path):
        return 1
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
        retry_time=max_downloadFrequency
        while (DownloadImage(sourceurl,path)==-1):
            retry_time-=1
            print zoom,x,y,'redownload',max_downloadFrequency-retry_time
            if retry_time==0:
                print zoom,x,y,'redownload'
                return 0



def InsertURLInfo(linkQueue):
    for zoom in range(0,13):
        this_xy=2**(zoom)
        for x in range(0,this_xy):
            try:
                s_zoom='%d/'%zoom
                s_x='%d'%x
                os.makedirs(dir_path+s_zoom+s_x)
            except:
                pass
            for y in range(0,this_xy):
                linkQueue.put(dict(x=x,y=y,z=zoom,count=0))


def downLoadImg(linkQueue):
    current_Quene = linkQueue
    while current_Quene.qsize() > 0 :
        isWaiting = 0;
        sleep_time=100
        while isWaiting == 0:
            try:
                urlInfo = current_Quene.get_nowait();
                if urlInfo['count'] >= max_downloadFrequency:
                    print "oh,just download fall..."
                    continue;
                DownloadTile(urlInfo['z'],urlInfo['x'],urlInfo['y'],urlInfo['count']);
                isWaiting = 1;
            except:
                sleep_time=sleep_time-1
                if sleep_time == 0:
                    isWaiting=1
                sleep(0.01);

if __name__ == '__main__':
    linkQueue = multiprocessing.dummy.Queue(maxlinksize);
    errorQueue = multiprocessing.dummy.Queue();
    cacheURL = multiprocessing.dummy.Process(target = InsertURLInfo,args = (linkQueue,))
    cacheURL.start();
    sleep(1);

    for i in range(0,maxthreads):
        download = multiprocessing.dummy.Process(target = downLoadImg,args = (linkQueue,))
        download.start();
        sleep(0.001)
    print "start!!!!~~~"
