"""读取本地演练来源的公开资料。"""
import json
from .capture import read_catalog,read_detail

def main():
    origin='http://127.0.0.1:8765';catalog=read_catalog(origin)
    print(json.dumps(catalog,ensure_ascii=False,indent=2))
    print(json.dumps(read_detail(origin,catalog['items'][0]['id']),ensure_ascii=False,indent=2))

if __name__=='__main__':main()
