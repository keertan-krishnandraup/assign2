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