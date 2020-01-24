from pymongo import MongoClient
from bson.json_util import dumps,loads
from pprint import pprint

client = MongoClient()
db = client['test_db']
master_coll = db['master']

#Fetch posts for a photo
def fetch_posts(idi):
    user_rec = loads(dumps(master_coll.find({'albums.photos.id':idi})))
    for i in user_rec[0]['albums']:
        for j in i['photos']:
            if(j['id']==idi):
                post_id = j['postId']

    user_rec = loads(dumps(master_coll.find({'posts.id':post_id})))
    for i in user_rec[0]['posts']:
        if(i['id']==post_id):
            return i

#Fetch comments for a photo
def fetch_comments(idi):
    post = fetch_posts(idi)
    return loads(dumps(post['comments']))

if __name__=='__main__':
    #pprint(fetch_posts(850))
    pprint(fetch_comments(850))