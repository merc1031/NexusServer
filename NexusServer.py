from gevent import monkey; monkey.patch_all()
from bottle import route, run, post


@post('/file')
def postFile():
    if request.json is None:
        abort(500)
    else:
        data = request.json
        src = data.get('source', None)
        dest = data.get('destination', None)

if __name__ == "__main__":
    run(host='localhost', port=24900, server='gevent')
