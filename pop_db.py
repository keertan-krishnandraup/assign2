from pymongo import MongoClient
import json
import requests
import pprint
from datetime import datetime
#poll
#join
def get_data_and_populate():
    todos_response = requests.get('https://jsonplaceholder.typicode.com/todos')
    todos = json.loads(todos_response.content)
    # TODO : Optimize
    resp_time = datetime.now()
    for i in todos:
        i['date_modified'] = resp_time

    users_response = requests.get('https://jsonplaceholder.typicode.com/users')
    users = json.loads(users_response.content)
    # TODO : Optimize
    resp_time = datetime.now()
    for i in users:# TODO : Optimize
        i['date_modified'] = resp_time

    posts_response = requests.get('https://jsonplaceholder.typicode.com/posts')
    posts = json.loads(posts_response.content)
    # TODO : Optimize
    resp_time = datetime.now()
    for i in posts:
        i['date_modified'] = resp_time

    photos_response = requests.get('https://jsonplaceholder.typicode.com/photos')
    photos = json.loads(photos_response.content)
    # TODO : Optimize
    resp_time = datetime.now()
    for i in photos:
        i['date_modified'] = resp_time

    comments_response = requests.get('https://jsonplaceholder.typicode.com/comments')
    comments = json.loads(comments_response.content)
    # TODO : Optimize
    resp_time = datetime.now()
    for i in comments:
        i['date_modified'] = resp_time

    albums_response = requests.get('https://jsonplaceholder.typicode.com/albums')
    albums = json.loads(albums_response.content)
    resp_time = datetime.now()
    for i in albums:
        i['date_modified'] = resp_time


    client = MongoClient()
    client.drop_database('test_db')
    test_db = client['test_db']

    u_coll = test_db['users']
    u_coll.insert_many(users)

    t_coll = test_db['todos']
    t_coll.insert_many(todos)

    p_coll = test_db['posts']
    p_coll.insert_many(posts)

    ph_coll = test_db['photos']
    ph_coll.insert_many(photos)

    c_coll = test_db['comments']
    c_coll.insert_many(comments)

    a_coll = test_db['albums']
    a_coll.insert_many(albums)
    print('Populated Database')


if __name__=='__main__':
    get_data_and_populate()