#! /usr/bin/python3

import os
import random
import requests
import shutil
import stat
import string

from contactlib import logger

HOME = os.getenv("HOME")
DATA = os.path.join(HOME, ".cache", "contactlib")
TMP = os.path.join(DATA, "tmp")

# For Python2 compatibility
def mkdirp(path):
    if not os.path.exists(path):
        os.makedirs(path)

mkdirp(DATA)
shutil.rmtree(TMP, ignore_errors=True)
mkdirp(TMP)

class Assest(object):
    def __init__(self, url, executable=False):
        self.url = url
        self.executable = executable

ASSETS = {
    "contactlib-l4-g0-c2-d7.db": Assest("https://pppublic.oss-cn-beijing.aliyuncs.com/tmp-server/contactlib-l4-g0-c2-d7.db"),

    "encoder.data-00000-of-00001": Assest("https://pppublic.oss-cn-beijing.aliyuncs.com/tmp-server/encoder.data-00000-of-00001"),
    "encoder.index": Assest("https://pppublic.oss-cn-beijing.aliyuncs.com/tmp-server/encoder.index"),
    "encoder.meta": Assest("https://pppublic.oss-cn-beijing.aliyuncs.com/tmp-server/encoder.meta"),

    "filter33.lst": Assest("https://pppublic.oss-cn-beijing.aliyuncs.com/tmp-server/filter33.lst"),
    "pca-coef.pickle": Assest("https://pppublic.oss-cn-beijing.aliyuncs.com/tmp-server/pca-coef.pickle"),

    "dssp-2.0.4-linux-amd64": Assest("https://pppublic.oss-cn-beijing.aliyuncs.com/tmp-server/dssp-2.0.4-linux-amd64", executable=True),
    "dssp-2.0.4-macOS": Assest("https://pppublic.oss-cn-beijing.aliyuncs.com/tmp-server/dssp-2.0.4-macOS", executable=True),
    "libsearch-2.0-macOS.so": Assest("https://pppublic.oss-cn-beijing.aliyuncs.com/tmp-server/libsearch-2.0-macOS.so"),
    "libsearch-2.0-linux-amd64.so": Assest("https://pppublic.oss-cn-beijing.aliyuncs.com/tmp-server/libsearch-2.0-linux-amd64.so"),

    "3aa0a.pdb": Assest("https://pppublic.oss-cn-beijing.aliyuncs.com/tmp-server/test_assests/3aa0a.pdb")
}

# copyright: https://stackoverflow.com/a/2030081
def randomword(len=10):
   letters = string.ascii_lowercase
   return ''.join(random.choice(letters) for i in range(len))

# TODO: check integrity
# copyright: https://stackoverflow.com/a/16696317
def download(p, url):
    tmp_p = os.path.join(os.path.join(TMP), randomword(10))
    r = requests.get(url, stream=True)
    with open(tmp_p, 'wb') as f:
        for chunk in r.iter_content(chunk_size=1024):
            if chunk: # filter out keep-alive new chunks
                f.write(chunk)
    shutil.move(tmp_p, p)

def asset_path(name):
    if name not in ASSETS:
        raise KeyError()
    a = ASSETS[name]

    p = os.path.join(DATA, name)
    if not os.path.isfile(p):
        logger.info("%s does not exist, downloading it..." % name)
        download(p, a.url)
    if a.executable:
        st = os.stat(p)
        os.chmod(p, st.st_mode | stat.S_IEXEC)
    
    return p