from pymongo import MongoClient
from bson.json_util import dumps,loads
import json
import pprint

from pop_db import get_data_and_populate
def join():
    client = MongoClient()

    db = client['test_db']

    to_coll = db['todos']
    u_coll = db['users']
    p_coll = db['photos']
    po_coll = db['posts']
    a_coll = db['albums']
    c_coll = db['comments']



    users = loads(dumps(u_coll.find({})))
    for i in users:
        todos_user_i = loads(dumps(to_coll.find({'userId':i['id']})))
        i['todos'] = todos_user_i
        albums_user_i = loads(dumps(a_coll.find({'userId':i['id']})))
        i['albums'] = albums_user_i
        for j in albums_user_i:
            photos_album_j = loads(dumps(p_coll.find({'albumId': j['id']})))
            j['photos'] = photos_album_j
        posts_user_i = loads(dumps(po_coll.find({'userId':i['id']})))
        i['posts'] = posts_user_i
        for k in posts_user_i:
            comments_post_k = loads(dumps(c_coll.find({'postId':k['id']})))
            k['comments'] = comments_post_k


    master = db['master']
    master.drop()
    master.insert_many(users)
    #op = open('output.txt','w')
    #op.write(json.dumps(users[:2],indent=4))


def get_and_update_data():
    get_data_and_populate()
    join()

if __name__=='__main__':
    join()