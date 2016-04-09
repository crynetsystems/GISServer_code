#!/usr/bin/python
# encoding=utf-8
# Filename: arcgisdownloader.py
import math
import os
import urllib2
import threading
import sqlite3

threads=[]
errors=[]
dir_path='G:/test/'
test_id=0

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
    except Exception,e:
        print 'error:'+path
        return -1
    fw = open(path, 'wb')
    fw.write(f)
    fw.close()
    return 1

def DownloadTile(zoom,x,y):
        sourceurl=xyz2url(x,y,zoom)
        path=xyz2path(x,y,zoom)
        if (DownloadImage(sourceurl,path)!=-1):
            pass
        else:
            errors.append({'zoom':zoom,'x':x,'y':y})

thread_num=0
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
            th = threading.Thread(target=DownloadTile, args=(zoom,x,y))
            th.start()
            threads.append(th)
            thread_num+=1
            if thread_num==50:
                print "OK"
                for th in threads:
                    th.join()
                thread_num=0


print len(errors)
while len(errors)>0:
    print 'now errors=',len(errors)
    current_errors=errors
    del errors[:]
    for error in current_errors:
        th = threading.Thread(target=DownloadTile, args=(error['zoom'],error['x'],error['y']))
        th.start()
        threads.append(th)
    for th in threads:
        th.join()
