import imgSave
from imgSave import Mongo
import bson
from cStringIO import StringIO

mongo = Mongo("127.0.0.1",27017,"img","img");

if mongo.OpenConn():
    print "conn successful!"
else:
    print "conn error!"


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
        print "oops"
    