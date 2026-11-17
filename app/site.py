"""供采集程序读取的本地演练来源。"""
import json
from html import escape
from http.server import BaseHTTPRequestHandler,ThreadingHTTPServer
from pathlib import Path
from urllib.parse import parse_qs,urlsplit

DATA=json.loads((Path(__file__).resolve().parents[1]/'fixtures'/'source.json').read_text(encoding='utf-8'))

def catalog(edition):
    return {'edition':edition,'items':[{'id':x['id'],'name':x['name'],'group':x['group'],'summary':x['detail']} for x in DATA['items']]}

def detail(item,edition):
    return {'id':item['id'],'name':item['name'],'group':item['group'],'edition':edition,'revision':edition,'detail':item['detail'] if edition=='1' else item['changed_detail']}

def catalog_page(edition):
    cards=''.join('<article data-id="'+escape(x['id'])+'"><h2>'+escape(x['name'])+'</h2><a href="/detail.html?id='+escape(x['id'])+'&edition='+edition+'">查看详情</a></article>' for x in DATA['items'])
    return '<html lang="zh"><meta charset="utf-8"><h1>'+escape(DATA['title'])+'</h1><main data-edition="'+edition+'">'+cards+'</main></html>'

def detail_page(item,edition):
    info=detail(item,edition)
    return '<html lang="zh"><meta charset="utf-8"><h1>'+escape(item['name'])+'</h1><main data-id="'+escape(item['id'])+'" data-edition="'+edition+'"><label>'+escape(DATA['choice'])+'<select id="choice"><option>甲</option><option>乙</option></select></label><button id="show">查看'+escape(DATA['detail_label'])+'</button><section id="result"></section><p>'+escape(DATA['revision'])+' '+edition+'</p></main><script>const c=document.querySelector("#choice"),r=document.querySelector("#result");c.onchange=()=>r.textContent="";document.querySelector("#show").onclick=()=>{r.textContent="读取中";let selected=c.value;setTimeout(()=>r.textContent=selected+":"+'+json.dumps(info['detail'],ensure_ascii=False)+',50)}</script></html>'

class Handler(BaseHTTPRequestHandler):
    def do_GET(self):
        url=urlsplit(self.path);args=parse_qs(url.query);edition=args.get('edition',['1'])[0]
        if edition not in ('1','2'):self.send_error(400);return
        if url.path in ('/catalog','/catalog.html'):
            body=catalog_page(edition) if url.path.endswith('.html') else json.dumps(catalog(edition),ensure_ascii=False)
        elif url.path in ('/detail','/detail.html'):
            item=next((x for x in DATA['items'] if x['id']==args.get('id',[''])[0]),None)
            if item is None:self.send_error(404);return
            body=detail_page(item,edition) if url.path.endswith('.html') else json.dumps(detail(item,edition),ensure_ascii=False)
        else:self.send_error(404);return
        raw=body.encode('utf-8');self.send_response(200);self.send_header('Content-Type',('text/html' if url.path.endswith('.html') else 'application/json')+'; charset=utf-8');self.send_header('Content-Length',str(len(raw)));self.end_headers();self.wfile.write(raw)
    def log_message(self,*args):pass

def start_server():return ThreadingHTTPServer(('127.0.0.1',0),Handler)

if __name__=='__main__':
    server=ThreadingHTTPServer(('127.0.0.1',8765),Handler);print('本地来源：http://127.0.0.1:8765/catalog',flush=True);server.serve_forever()
