#!/usr/bin/python
# encoding=utf-8
# Filename: arcgisdownloader.py
import math
import os
import urllib2
import multiprocessing
from time import sleep
maxthreads = 50;
maxlinksize = 500;
threads=[]
errors=[]
dir_path='G:/test_01/'
test_id=0
thread_num=0
linkQueue = multiprocessing.Queue(maxlinksize);
errorQueue = multiprocessing.Queue();

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
        f=urllib2.urlopen(image_url,timeout = 30).read()
        print image_url
    except Exception,e:
        print 'error:'+path
        return -1
    fw = open(path, 'wb')
    fw.write(f)
    fw.close()
    return 1

def DownloadTile(zoom,x,y,count):
        sourceurl=xyz2url(x,y,zoom)
        path=xyz2path(x,y,zoom)
        if (DownloadImage(sourceurl,path)!=-1):
            pass
        else:
            #errors.append({'zoom':zoom,'x':x,'y':y})
            errorQueue.put_nowait(dict(x=x,y=y,z=zoom,count=count+1));



def InsertURLInfo():
    for zoom in range(0,7):
        this_xy=2**(zoom)
        for x in range(0,this_xy):
            try:
                s_zoom='%d/'%zoom
                s_x='%d'%x
                os.makedirs(dir_path+s_zoom+s_x)
            except Exception,e:
                pass
            for y in range(0,this_xy):
                isWaiting = 0
                while isWaiting == 0:
                    try:
                        linkQueue.put_nowait(dict(x=x,y=y,z=zoom,count=0));
                        isWaiting=1
                    except:
                        sleep(10)


def downLoadImg(download_status):
    if download_status=='normal':
        current_Quene = linkQueue
    elif download_status=='error':
        current_Quene = errorQueue
    print current_Quene;
    print current_Quene.qsize();
    while current_Quene.qsize() > 0 :
        isWaiting = 0;
        while isWaiting == 0:
            try:
                urlInfo = current_Quene.get_nowait();
                if urlInfo['count'] >= max_downloadFrequency:
                    pass;
                    continue;
                print urlInfo;
                DownloadTile(urlInfo['z'],urlInfo['x'],urlInfo['y'],urlInfo['count']);
                isWaiting = 1;
            except:
                print "oops"
                sleep(0.5);
    if download_status=='normal':
        downLoadImg('error');

def main():
    cacheURL = multiprocessing.Process(target = InsertURLInfo)
    cacheURL.start();
    sleep(1);
    for i in range(50):
        download = multiprocessing.Process(target = downLoadImg,args = ('normal',))
        download.start();
    print "finish!!!!~~~"

if __name__ == '__main__':
    main()

