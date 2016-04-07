import imgSave
from imgSave import Mongo
import bson
from cStringIO import StringIO
#import the imgSave module , the class Mongo is the one who runs database , the class's ctor requires four arguments
#stand for the database's ip , port , database you need to connect and the collection you need to reach.
#in the origin edition i just write it dead in the code. and we will save it in a config file in the furure.
mongo = Mongo("127.0.0.1",27017,"img","img");

if mongo.OpenConn():
    print "conn successful!"
else:
    print "conn error!"
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
        print "oops"
    
