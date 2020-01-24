from pymongo import MongoClient
from bson.json_util import dumps, loads
from pprint import pprint

client = MongoClient()
db = client['test_db']
master_coll = db['master']
records = master_coll.find({})
count = 0
for i in records:
    for j in i['albums']:
        for k in j['photos']:
            k['postId'] = count // 50 + 1
            count +=1
        master_coll.update_one({"albums.id":j['id']},{'$set':{"albums.$.photos":j['photos']}})