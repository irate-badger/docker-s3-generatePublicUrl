import flask
import base64
import hmac
import hashlib
import urllib
import time
import os
from flask import request
app = flask.Flask(__name__)

S3PROXY_AWS_ACCESS_KEY = os.environ['S3PROXY_AWS_ACCESS_KEY']
S3PROXY_AWS_SECRET_KEY = os.environ['S3PROXY_AWS_SECRET_KEY']

@app.route('/')
def welcome_():
    return 'Try to provide a file that you would like encoding such as /mybucket/myfile'


@app.route('/<path:path>')
def transform_path(path):
    try:
        bucket, file_path = _splitPaths(path)
        expire = int(request.args.get('expire', '600'))
        import time
        time = _calculate_expiration(expire)
        return _calculate(bucket, file_path, time)
    except AttributeError:
        return "The path is not long enough, did we miss the bucket?"


def _splitPaths(path):
    paths = path.split("/")
    if len(paths) < 2:
        raise AttributeError

    bucket = paths[0]
    paths.remove(bucket)
    file_path = '/'.join(paths)

    return bucket, file_path


def _calculate_expiration(expire, current_time=int(time.time())):
    return current_time + expire


def _calculate(bucket, file_path, time):
    url = "GET\n\n\n{time}\n/{file_path}".format(time=str(time), file_path=file_path)
    print "Generated {url} from {time} and {file_path}".format(url=url, time=time, file_path=file_path)
    print "Encoding url with {S3PROXY_AWS_SECRET_KEY}".format(S3PROXY_AWS_SECRET_KEY=S3PROXY_AWS_SECRET_KEY)
    h = hmac.new(S3PROXY_AWS_SECRET_KEY, url, hashlib.sha1)
    signature = urllib.quote_plus(base64.encodestring(h.digest()).strip())
    s3_url = "https://{bucket}.s3.amazonaws.com/{file_path}?AWSAccessKeyId={S3PROXY_AWS_ACCESS_KEY}" \
             "&Expires={time}&Signature={signature}"
    return s3_url.format(bucket=bucket, file_path=file_path, S3PROXY_AWS_ACCESS_KEY=S3PROXY_AWS_ACCESS_KEY,
                         time=time, signature=signature)


if __name__ == '__main__':
    app.run()
