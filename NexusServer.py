import shutil
import os
import errno
import json
import logging
import sys
from logging.handlers import RotatingFileHandler
from gevent import monkey; monkey.patch_all()
from bottle import route, run, post, request, get

@post('/file')
def postFile():
    if request.json is None:
        abort(500)
    else:
        data = request.json
        global gHandler
        gHandler.handleData(data)

        return { "success" : True, "data" : { }, "code" : -1 }

@post('/opt')
def postOptions():
    if request.json is None:
        abort(500)
    else:
        data = request.json
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
        logger = kwargs.get('logger')
        self.getRoutesFromConfig(config) 
        self.logger = logger

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
        
        self.logger.debug('Begin handling download item {downloadItem!r}'.format(
                                downloadItem=downloadItem ))

        source = downloadItem['url']
        dest = downloadItem['filename']
        destPath = Handler.fixPath(dest)
        (head, tail) = os.path.split(destPath)
        for k,v in self.routes.iteritems():
            if v['enabled']:    

                self.logger.debug('Attempting to find match in {source!r} with {match!r}'.format(
                                        source=source,
                                        match=v['match'] ))

                o = re.search(v['match'], source)

                if o is not None:

                    self.logger.info('Found match with {match!r} in {source!r}: {group!r}'.format(
                                            group=o.group(0),
                                            source=source,
                                            match=v['match'] ))

                    tarDir = Handler.fixPath(v['route']) 
                    mkdir_p(tarDir)
                    targetDir = os.path.join(tarDir, tail) 

                    self.logger.info('Moving {source!r} to {dest!r}'.format(
                                            source=destPath,
                                            dest=targetDir ))

                    shutil.move(destPath, targetDir)
                    break
                else:

                    self.logger.debug('Failed to find matches in {source!r} with match criteria {match!r}'.format(
                                            source=source,
                                            match=v['match'] ))

    @staticmethod
    def fixPath(path):
        arrayDir = path.split(os.sep)
        if os.name == 'nt':
            arrayDir[0] = arrayDir[0] + '\\' if arrayDir[0][1] == ':' else arrayDir[0]
        destPath = os.path.join(*arrayDir)
        return destPath

    def getOptions(self):
        return self.routes

gHandler = None

def mkdir_p(path):
    try:
        os.makedirs(path)
    except OSError as exc: # Python >2.5
        if exc.errno == errno.EEXIST:
            pass
        else: raise

def getLoggingLevel(verbosity):
    logLevel = logging.WARNING
    if options.verbosity >= 3:
        logLevel = logging.DEBUG
    elif options.verbosity >=2:
        logLevel = logging.INFO
    elif options.verbosity >=1:
        logLevel = logging.WARNING
    else:
        logLevel = None
    return logLevel 

if __name__ == "__main__":
    from optparse import OptionParser

    parser = OptionParser()
    parser.add_option('-v', action='count', dest='verbosity', default=1)
    parser.add_option('-q', action='store_const', const=0, dest='verbosity')
    parser.add_option('-c', '--config', action='store', type='string', dest='config', default=os.path.join('config','config.ini'))

    (options,args) = parser.parse_args()

    loggingLevel = getLoggingLevel(options.verbosity)

    logger = logging.getLogger(__name__)
    logger.setLevel(logging.DEBUG)
 
    handler = RotatingFileHandler('logs/nexusserver.log',maxBytes=500000,backupCount=10)
    handler.setLevel(logging.DEBUG)
    logger.addHandler(handler)
    
    if loggingLevel is not None:
        consoleHandler = logging.StreamHandler(sys.stdout)
        consoleHandler.setLevel(loggingLevel)
        logger.addHandler(consoleHandler)
    

    gHandler = Handler(logger=logger, config=options.config)

    run(host='localhost', port=24900, server='gevent')
