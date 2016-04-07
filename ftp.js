var http = require('http');
var mongoose = require('mongoose');
#make sure the dbdriver mongoose you require is at the vision of 2.8 
mongoose.connect('mongodb://localhost/img');
var regex = /.*\/(.+?)\/(.+?)\/(.+?)\.((jpg)|(png))/g; 
var matches;
var dataType = {
	'jpg':'image/jpeg',
	'png':'image/png'
};
http.createServer(function(req,res){
	if(req.method == "GET")
	{
        matches = regex.exec(req.url);
    	if(matches == null)
    	{
    		res.end();
    		return;
    	}
    	//matches[1-4]
    	imgModel.find()
    	.where('x').equals(matches[1])
    	.where('y').equals(matches[2])
    	.where('z').equals(matches[3]).exec(function(err,img){
    		if(err)
    		{
    			res.writeHead(404);
    			res.end();
    			return;
    		}
            var imgs = img[0].buffer;
            var buf = new Buffer(imgs,'base64');
    		res.writeHead(200,{'Content-Type':dataType[matches[4]]});
            res.write(buf,'binary');
            res.end();
    	});
	}
}).listen(8000,'127.0.0.1');


var Schema = mongoose.Schema;
//骨架模版
var image = new Schema({
    x   : Number,
    y    : Number,
    z : Number,
    buffer  : Buffer
})

var imgModel = mongoose.model('img', image,"img");


