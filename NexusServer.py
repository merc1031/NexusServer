import shutil
import os
import errno
import json
from gevent import monkey; monkey.patch_all()
from bottle import route, run, post, request, get


@post('/file')
def postFile():
    if request.json is None:
        abort(500)
    else:
        data = request.json
        print data
        global gHandler
        gHandler.handleData(data)

        return { "success" : True, "data" : { }, "code" : -1 }

@post('/opt')
def postOptions():
    if request.json is None:
        abort(500)
    else:
        data = request.json
        print data
        print 'where my data'
        global gHandler
        gHandler.handleOptions(data)

        return { "success" : True, "data" : { }, "code" : -1 }

@get('/opt')
def getOptions():
    global gHandler
    return gHandler.getOptions()

class Handler(object):
    def __init__(self,*args,**kwargs):
        config = kwargs.get('config', os.path.join('config', 'config.ini'))
        self.getRoutesFromConfig(config) 

    @staticmethod
    def convertFromJS(options):
        for option, value in options.iteritems():
            value['enabled'] = True if value['enabled'] == 'on' else False

        return options 

    def getRoutesFromConfig(self, config):
        if os.path.exists(config):
            with open(config, 'r') as f:
                self.routes = json.loads(f.read())
        else:
            self.routes = {}

    def handleOptions(self, options):
        self.routes = Handler.convertFromJS(options)
        with open(os.path.join('config', 'config.ini'), 'w+') as f:
            f.write(json.dumps(self.routes))

    def handleData(self, downloadItem):
        import re
        source = downloadItem['url']
        dest = downloadItem['filename']
        destPath = Handler.fixPath(dest)
        (head, tail) = os.path.split(destPath)
        for k,v in self.routes.iteritems(): 
            o = re.search(k, source)
            if o is not None:
                tarDir = Handler.fixPath(v['route']) 
                mkdir_p(tarDir)
                shutil.move(destPath, os.path.join(tarDir, tail) )
                break

    @staticmethod
    def fixPath(path):
        arrayDir = path.split(os.sep)
        if os.name == 'nt':
            arrayDir[0] = arrayDir[0] + '\\' if arrayDir[0][1] == ':' else arrayDir[0]
        destPath = os.path.join(*arrayDir)
        return destPath

    def getOptions(self):
        print self.routes
        return self.routes

gHandler = None

def mkdir_p(path):
    try:
        os.makedirs(path)
    except OSError as exc: # Python >2.5
        if exc.errno == errno.EEXIST:
            pass
        else: raise

if __name__ == "__main__":
    gHandler = Handler()

    run(host='localhost', port=24900, server='gevent')
