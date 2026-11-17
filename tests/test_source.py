"""本地来源与基础收据的回归。"""
import tempfile
import threading
import unittest
from pathlib import Path
from urllib.request import urlopen
from app.site import DATA,start_server
from app.capture import read_catalog,read_detail
from app.records import save_catalog,save_detail,list_receipts

class SourceTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.server=start_server();cls.thread=threading.Thread(target=cls.server.serve_forever,daemon=True);cls.thread.start();cls.origin=f'http://127.0.0.1:{cls.server.server_port}'
    @classmethod
    def tearDownClass(cls):
        cls.server.shutdown();cls.server.server_close();cls.thread.join(timeout=2)
    def test_catalog_and_detail(self):
        items=read_catalog(self.origin)['items'];self.assertEqual(len(items),len(DATA['items']))
        for item in items:self.assertEqual(read_detail(self.origin,item['id'])['item']['id'],item['id'])
    def test_revision_and_page(self):
        key=DATA['items'][0]['id'];self.assertNotEqual(read_detail(self.origin,key,'1')['item']['detail'],read_detail(self.origin,key,'2')['item']['detail'])
        with urlopen(self.origin+'/catalog.html?edition=2') as response:self.assertIn(DATA['title'],response.read().decode('utf-8'))
    def test_receipts(self):
        with tempfile.TemporaryDirectory() as temporary:
            path=Path(temporary)/'records.sqlite3';catalog=read_catalog(self.origin)
            self.assertEqual(save_catalog(path,catalog),2);save_detail(path,read_detail(self.origin,catalog['items'][0]['id']))
            self.assertEqual(len(list_receipts(path)),1)
    def test_remote_rejected(self):
        with self.assertRaises(ValueError):read_catalog('https://example.com')
