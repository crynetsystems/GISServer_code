import imgSave
from imgSave import Mongo
import bson
from cStringIO import StringIO

#so this is the function that client invoke to upload images into mongodb.
#the arguments the function take is the longitude and the latitude the image stand for
#, x , y , z ,and the img_path is image's path in your computer.https://cnodejs.org/topic/56dfa16ff5d830306e2f0f04
def UploadImg(x,y,z,img_path):
    try:
        img = open(img_path,'rb');
        buff = StringIO(img.read());
    except Exception, e:
        print e
    #convert to buffer
    img={"x":x,"y":y,"z":z,"buffer":bson.binary.Binary(buff.getvalue())}
    if mongo.SaveImgSingular(img):
        print "insert successful"
    else:
        print "oops,fucking error~"
dir_path="G:/test"
def xyz2path(x,y,zoom):
    s_zoom='%d/'%zoom
    s_x='%d/'%x
    s_y='%d'%y
    return dir_path+s_zoom+s_x+s_y+'.jpg'


#Upload images from (x1,y1,z1)to(x2,y2,z2)
def upLoadImages(z1,z2,x1=0,x2=-1,y1=0,y2=-1):
    if x2==-1:
        x2=2**(z2)
        y2=2**(z2)
    for zoom in range(z1,z2+1):
        this_zoom_xy=2**(zoom)
        x_begin=0
        x_end=this_zoom_xy
        if zoom==z1:
            x_begin=x1
        elif zoom==z2:
            x_end=x2
        for x in range(x_begin,this_zoom_xy):
            y_begin=0
            y_end=this_zoom_xy
            if zoom==z1 and x==x1:
                y_begin=y1
            elif zoom==z2:
                y_end=y2
            for y in range(0,this_zoom_xy):
                pass
def main():
    #import the imgSave module , the class Mongo is the one who runs database , the class's ctor requires four arguments
    #stand for the database's ip , port , database you need to connect and the collection you need to reach.
    #in the origin edition i just write it dead in the code. and we will save it in a config file in the furure.
    mongo = Mongo("127.0.0.1",27017,"img","img");
    
    if mongo.OpenConn():
        print "conn successful!"
    else:
        print "conn error!"


if __name__ == '__main__':
    main()
