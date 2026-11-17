"""解释目录与详情的业务身份。"""
def interpret_catalog(row):
    if not row['id'] or not row['name']:raise ValueError('目录身份不完整')
    return {'source_id':row['id'],'group':row['group'],'name':row['name']}

def interpret_detail(row):
    if not row['id'] or row['revision'] not in ('1','2'):raise ValueError('详情身份不完整')
    return {'source_id':row['id'],'group':row['group'],'revision':row['revision']}
