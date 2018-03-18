import flask
import base64
import hmac
import hashlib
import urllib
import time
import os
import argparse

from flask import request
app = flask.Flask(__name__)

S3PROXY_AWS_ACCESS_KEY = ""
S3PROXY_AWS_SECRET_KEY = ""

if os.environ.get('S3PROXY_AWS_ACCESS_KEY') is not None:
    S3PROXY_AWS_ACCESS_KEY = os.environ['S3PROXY_AWS_ACCESS_KEY']

if os.environ.get('S3PROXY_AWS_SECRET_KEY') is not None:
    S3PROXY_AWS_SECRET_KEY = os.environ['S3PROXY_AWS_SECRET_KEY']


@app.route('/')
def welcome_():
    return 'Try to provide a file that you would like encoding such as /mybucket/myfile'


@app.route('/<path:path>')
def transform_path(path):
    print "\n\n\n***Generating the encoded url"
    try:
        bucket, file_path = _split_paths(path)
        expire = int(request.args.get('expire', '60'))
        print "Expiring after {expire}".format(expire=expire)
        expiration = _calculate_expiration(expire)
        return _calculate(bucket, file_path, expiration)
    except AttributeError:
        return "The path is not long enough, did we miss the bucket?"


def _split_paths(path):
    paths = path.split("/")
    if len(paths) < 2:
        raise AttributeError

    bucket = paths[0]
    paths.remove(bucket)
    file_path = '/'.join(paths)

    return bucket, file_path


def _calculate_expiration(expire, current_time=-1):
    if current_time == -1:
        current_time = int(time.time())
    expiration = current_time + expire
    print "Expiring after {expiration}, calculated from {current_time} and {expire}"\
        .format(expiration=expiration, current_time=current_time, expire=expire)
    return expiration


def _calculate(bucket, file_path, expiration):
    url = "GET\n\n\n{expiration}\n/{bucket}/{file_path}".format(expiration=str(expiration), bucket=bucket, file_path=file_path)
    print "Generated {url} from {expiration} and {file_path}".format(url=url, expiration=expiration, file_path=file_path)
    print "Encoding url with {S3PROXY_AWS_SECRET_KEY}".format(S3PROXY_AWS_SECRET_KEY=S3PROXY_AWS_SECRET_KEY)
    h = hmac.new(S3PROXY_AWS_SECRET_KEY, url, hashlib.sha1)
    signature = urllib.quote_plus(base64.encodestring(h.digest()).strip())
    s3_url = "https://{bucket}.s3.amazonaws.com/{file_path}?AWSAccessKeyId={S3PROXY_AWS_ACCESS_KEY}" \
             "&Expires={expiration}&Signature={signature}"
    return s3_url.format(bucket=bucket, file_path=file_path, S3PROXY_AWS_ACCESS_KEY=S3PROXY_AWS_ACCESS_KEY,
                         expiration=expiration, signature=signature)


def _arg_parse():
    parser = argparse.ArgumentParser(description='Generate your own public, time limited S3 urls.')
    parser.add_argument('-a', '--ACCESS_KEY', type=str, help='Your AWS access key',
                        dest='AWS_ACCESS_KEY', required='True')
    parser.add_argument('-s', '--SECRET_KEY', type=str, help='Your AWS secret key',
                        dest='AWS_SECRET_KEY', required='True')

    _parsed_args = parser.parse_args()
    global S3PROXY_AWS_ACCESS_KEY, S3PROXY_AWS_SECRET_KEY
    S3PROXY_AWS_ACCESS_KEY = _parsed_args.AWS_ACCESS_KEY
    S3PROXY_AWS_SECRET_KEY = _parsed_args.AWS_SECRET_KEY


if __name__ == '__main__':
    _arg_parse()
    app.run()
