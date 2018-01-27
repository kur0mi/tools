#-*- coding: utf-8 -*-
import os
import sys
from qiniu import Auth, put_file
import hashlib

def md5(str):
    m = hashlib.md5()
    m.update(str)
    return m.hexdigest()

access_key = "YdZHoJKiq1RdOz5XkUoWdPUBLYKxZKhRs4AhOOey" # 填入你的AK
secret_key = "pdahDV4Cudpqk0AozbCFqEgaBWnZbCaN9EU4vSOy" # 填入你的SK
bucket_name = "kurumi" # 填入你的七牛空间名称
url = "store.nightmare.xin" # 填入你的域名地址
qiniu = Auth(access_key, secret_key)

def upload_qiniu(path):
    dirname, filename = os.path.split(path)
    s = filename.split('.')
    key = md5(s[0]) + '.' + s[-1]
    policy = {
        "scope" : "%s:%s" % (bucket_name, key)
    }
    token = qiniu.upload_token(bucket_name, key = key, policy = policy)
    ret, info = put_file(token, key, path)
    return ret != None and ret['key'] == key

def addToClipBoard(text):
    command = 'echo ' + text.strip() + '| clip'
    os.system(command)

if __name__ == '__main__':
    path = sys.argv[1]
    name = os.path.split(path)[1]
    s = name.split('.')
    markdown_url = "![](%s/%s)" % ('http://' + url, md5(s[0]) + '.' + s[-1])
    # make it to clipboard
    addToClipBoard(markdown_url)
    print markdown_url
    
    ret = upload_qiniu(path)
    if ret:
        print "upload_succeed"
    else:
        print "upload_failed"
    