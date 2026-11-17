"""从本地来源获取目录和单项详情。"""
import json
from urllib.parse import urlencode,urlsplit
from urllib.request import urlopen
from .domain import interpret_catalog,interpret_detail

def get(origin,path,query):
    url=urlsplit(origin)
    if url.scheme!='http' or url.hostname not in ('127.0.0.1','localhost'):raise ValueError('只允许本地演练来源')
    address=origin.rstrip('/')+path+'?'+urlencode(query)
    with urlopen(address,timeout=5) as response:data=json.load(response)
    return address,data

def read_catalog(origin,edition='1'):
    address,data=get(origin,'/catalog',{'edition':edition})
    return {'url':address,'edition':data['edition'],'items':[dict(item,identity=interpret_catalog(item)) for item in data['items']]}

def read_detail(origin,item_id,edition='1'):
    address,data=get(origin,'/detail',{'id':item_id,'edition':edition})
    return {'url':address,'edition':data['edition'],'item':dict(data,identity=interpret_detail(data))}
