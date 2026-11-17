"""保存基础资料与最近访问页面的收据。"""
import json
import sqlite3
from pathlib import Path

def connect(path):
    path=Path(path);path.parent.mkdir(parents=True,exist_ok=True);db=sqlite3.connect(path)
    db.execute('CREATE TABLE IF NOT EXISTS catalog (source_id TEXT PRIMARY KEY,edition TEXT NOT NULL,payload TEXT NOT NULL)')
    db.execute('CREATE TABLE IF NOT EXISTS details (receipt INTEGER PRIMARY KEY,source_id TEXT NOT NULL,edition TEXT NOT NULL,payload TEXT NOT NULL)')
    db.execute('CREATE TABLE IF NOT EXISTS progress (name TEXT PRIMARY KEY,last_page TEXT NOT NULL)')
    return db

def save_catalog(path,result):
    with connect(path) as db:
        for item in result['items']:db.execute('INSERT OR REPLACE INTO catalog VALUES (?,?,?)',(item['id'],result['edition'],json.dumps(item,ensure_ascii=False)))
        db.execute('INSERT OR REPLACE INTO progress VALUES (?,?)',('catalog',result['url']))
    return len(result['items'])

def save_detail(path,result):
    item=result['item']
    with connect(path) as db:
        db.execute('INSERT INTO details (source_id,edition,payload) VALUES (?,?,?)',(item['id'],result['edition'],json.dumps(result,ensure_ascii=False)))
        db.execute('INSERT OR REPLACE INTO progress VALUES (?,?)',('detail',result['url']))
    return item['id']

def list_receipts(path):
    db=connect(path)
    try:return [json.loads(row[0]) for row in db.execute('SELECT payload FROM details ORDER BY receipt')]
    finally:db.close()
