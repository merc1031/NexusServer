import shutil
import os
import errno

from gevent import monkey; monkey.patch_all()
from bottle import route, run, post, request


@post('/file')
def postFile():
    if request.json is None:
        abort(500)
    else:
        data = request.json
        print data
        handleData(data)

        return { "success" : True, "data" : { }, "code" : -1 }

def handleData(downloadItem):
    import re
    source = downloadItem['url']
    dest = downloadItem['filename']
    arrayDir = dest.split(os.sep)
    if os.name == 'nt':
        arrayDir[0] = arrayDir[0] + '\\' if arrayDir[0][1] == ':' else arrayDir[0]
    destPath = os.path.join(*arrayDir)
    (head, tail) = os.path.split(destPath)
    for i in ['google','sourceforge']: 
        o = re.search(i, source)
        if o is not None:
            tarDir = os.path.join(head, i)
            mkdir_p(tarDir)
            shutil.move(destPath, os.path.join(tarDir, tail) )
            break

def mkdir_p(path):
    try:
        os.makedirs(path)
    except OSError as exc: # Python >2.5
        if exc.errno == errno.EEXIST:
            pass
        else: raise

if __name__ == "__main__":
    run(host='localhost', port=24900, server='gevent')
