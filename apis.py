from flask import Flask, request, jsonify
from pymongo import MongoClient
from bson.json_util import dumps,loads, ObjectId
import pprint
import json
from joiner import join
from datetime import datetime
import logging

app = Flask(__name__)

client = MongoClient()
db = client['test_db']
debug = 1
logging.basicConfig(filename='exec_log.log', level=logging.DEBUG)

@app.route('/posts',methods = ['GET'])
def get_posts():
    master_coll = db['master']
    posts = []
    resp = loads(dumps(master_coll.find({})))
    for i in resp:
        for j in i['posts']:
            posts.append({'userId':j['userId'],'id':j['id'],'title':j['title'],'body':j['body']})
    if (debug):
        f = open('op.txt', 'w')
        f.write(dumps(posts[:2]))
        f.close()
    return dumps(posts, indent = 4)

@app.route('/posts/<int:idi>',methods = ['GET'])
def get_posts_id(idi):
    master_coll = db['master']
    resp = loads(dumps(master_coll.find({"posts.id":idi})))
    for i in resp[0]['posts']:
        if(i['id']==int(idi)):
            return dumps({'userId':i['userId'],'id':i['id'],'title':i['title'],'body':i['body']}, indent = 1)
    return str([])

@app.route('/all_comments',methods = ['GET'])
def get_all_comments():
    master_coll = db['master']
    resp = loads(dumps(master_coll.find({})))
    comments = []
    for i in resp:
        for j in i['posts']:
            for k in j['comments']:
                comments.append({'postId':k['postId'],'id':k['id'],'name':k['name'],'email':k['email'],'body':k['body']})
    if(debug):
        f = open('op.txt','w')
        f.write(dumps(comments[:2]))
        f.close()
    return dumps(comments, indent = 4)

@app.route('/comments',methods = ['GET'])
def get_post_comments():
    post_id = request.args.get('postId')
    comments = []
    master_coll = db['master']
    resp = loads(dumps(master_coll.find({"posts.id":int(post_id)})))
    for i in resp[0]['posts']:
        if(i['id']==int(post_id)):
            for j in i['comments']:
                comments.append({'postId':j['postId'],'id':j['id'],'name':j['name'],'email':j['email'],'body':j['body']})
            if (debug):
                f = open('op.txt','w')
                f.write(dumps(comments, indent = 4))
                f.close()
            return dumps(comments, indent=4)
    return str([])

@app.route('/post',methods = ['GET'])
def get_user_posts():
    user_id = request.args.get('userId')
    master_coll = db['master']
    resp = loads(dumps(master_coll.find({'id':int(user_id)})))
    posts = []
    for i in resp[0]['posts']:
        posts.append({'userId':i['userId'],'id':i['id'],'title':i['title'],'body':i['body']})
    return dumps(posts, indent = 4)


@app.route('/del_post/<int:idi>',methods = ['DELETE'])
def delete_post(idi):
    client = MongoClient()
    db = client['test_db']
    master_coll = db['master']
    resp = loads(dumps(master_coll.find({"posts.id":idi})))
    idx = None
    for i in range(len(resp[0]['posts'])):
        if(resp[0]['posts'][i]['id']==idi):
            idx = i
    if(idx!=None):
        resp[0]['posts'].pop(idx)
        master_coll.update_one({"posts.id":idi},{"$set":{"posts":resp[0]['posts']}})
        return 'Deleted'
    return f'Post with id {idi} : Not Found'

@app.route('/postsu',methods = ['PUT'])
def add_post():
    post_data = request.get_json()
    new_post = {"_id":ObjectId(),"userId":post_data['userId'],"id":post_data['id'],"title":post_data['title'],"body":post_data["body"],"date_modified":datetime.now(),"comments":[]}
    master_coll = db['master']
    resp = loads(dumps(master_coll.find({"id":int(post_data['userId'])})))
    if(debug):
        print(type(resp[0]['posts'][0]))
    for i in resp[0]['posts']:
        if(i['id']==post_data['id']):
            return f"Post with id {post_data['id']} already present!"
    resp[0]['posts'].append(new_post)
    master_coll.update_one({"id":post_data['userId']}, {"$set":{"posts":resp[0]['posts']}})
    return 'Inserted'

@app.route('/addcomments',methods=['PUT'])
def add_comment():
    post_data = request.get_json()
    new_comment = {"_id":ObjectId(),"postId":post_data['postId'],'id':post_data['id'],'name':post_data['name'],'email':post_data['email'],'body':post_data['body'],'date_modified':datetime.now()}
    master_coll = db['master']
    resp = loads(dumps(master_coll.find({"posts.id":int(post_data['postId'])})))
    for i in resp[0]['posts']:
        if(i['id']==int(post_data['postId'])):
            for j in i['comments']:
                if(j['id']==post_data['id']):
                    return f"Comment with id {post_data['id']} already present!"
            i['comments'].append(new_comment)
            master_coll.update_one({'posts.id':post_data['postId']},{'$set':{'posts.$.comments':i['comments']}})
    return 'Comment Added'

@app.route('/get_photo', methods = ['GET'])
def get_photo():
    photo_id = int(request.args.get('photoId'))
    master_coll = db['master']
    resp = loads(dumps(master_coll.find_one({"albums.photos.id":photo_id})))
    for i in resp['albums']:
        for j in i['photos']:
            if(j['id']==photo_id):
                return dumps({'Album ID':j['albumId'],'Title':j['title'],'URL':j['title'],'Post ID':j['postId']}, indent = 4)
    return str([])

@app.route('get_all_photos', methods = ['GET'])
def get_all_photos():
    album_id = int(request.args.get('albumId'))
    master_coll = db['master']
    resp = loads(dumps(master_coll.find_one({"albums.id":album_id})))
    photos = []
    for i in resp['albums']:
        for j in i['photos']:
            photos.append({'Album ID':j['albumId'],'Title':j['title'],'URL':j['title'],'Post ID':j['postId']})
    return dumps(photos, indent = 4)

@app.route('albums', methods = ['GET'])
def get_all_albums():
    user_id = int(request.args.get('userId'))
    master_coll = db['master']
    resp = loads(dumps(master_coll.find_one({"id":user_id})))
    albums = []
    for i in resp['albums']:
        albums.append({'User ID':i['userId'],'Title':i['title']})
    return dumps(albums, indent = 4)

@app.route('todos', methods = ['GET'])
def get_todos():
    user_id = int(request.args.get('userId'))
    master_coll = db['master']
    resp = loads(dumps(master_coll.find_one("id":user_id)))
    todos = []
    for i in resp['todos']:
        todos.append({'User ID':i['userId'], 'ID':i['id'], 'Title':i['title'], 'Completed':i['completed']})
    return dumps(todos, indent = 4)

@app.route('create_album', methods = ['POST'])
def create_album():
    #_id, userId, id, title, photos, date_modified
    post_data = request.get_json()
    new_album = {'_id':ObjectId(),'userId':post_data['userId'],'id':post_data['id'],'title':post_data['title'],'date_modified':post_data['date_modified'],'photos':[]}
    resp = loads(dumps(master_coll.find_one({"id":post_data['userId']})))
    if(not resp):
        return 'ID not found'
    resp['albums'].append(new_album)
    master_coll.update_one({'id':post_data['userId']}, {'$set':{'albums':resp['albums']}})
    return 'New Album Created'

@app.route('create_photo', methods = ['POST'])
def create_photo():
    #_id, albumId, id, title, url, thumbnailURl, date_modified, postId
    post_data = request.get_json()
    master_coll = db['master']
    resp1 = master_coll.find_one({"albums.id":post_data['albumId']})
    if(not resp1):
        return 'Album ID not valid'
    resp2 = master_coll.find_one({"posts.id":post_data['postId']})
    if(not resp2):
        return 'Post ID not valid'
    new_photo = {'_id':ObjectId(), 'albumId':post_data['albumId'], 'id':post_data['id'], 'title':post_data['title'], 'url':post_data['url'], 'thumbnailUrl':post_data['thumbnailUrl'], 'date_modified':datetime.now(),'postId', post_data['postId']}
    for i in resp1['albums']:
        if(i['id']==post_data['albumId']):
            i['photos'].append(new_photo)
            master_coll.update_one({'albums.id':post_data['albumId']}, {'$set':{'albums.$.photos':i['photos']}})
            break
    return 'New Photo Created'

@app.route('del_album/<int:idi>', methods = ['DELETE'])
def del_album(idi):
    master_coll = db['master']
    resp = master_coll.find_one({"albums.id":idi})
    if(not resp):
        return 'ID not valid'
    idx = None
    for i in range(len(resp['albums'])):
        if(resp['albums'][i]['id']==idi):
            idx = i
    resp['albums'].pop(idx)
    master_coll.update_one({'albums.id':idi}, {'$set':{"albums":resp['albums']}})

@app.route('del_photo/<int:idi>', methods = ['DELETE'])
def del_photo(idi):
    master_coll = db['master']
    resp = master_coll.find_one({"albums.photos.id":idi})
    if(not resp):
        return 'ID not valid'
    idx = None
    for i in resp['albums']:
        for j in range(len(i['photos'])):
            if(i['photos'][j]['id']==idi):
                idx = j
        if(idx):
            i['photos'].pop(idx)
            master_coll.update_one({"albums.photos.id":idi},{'$set':{"albums.$.photos":i['photos']}})
            break
    return 'Deleted'