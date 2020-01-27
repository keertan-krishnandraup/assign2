# Assignment 2 - User DB CRUD Operations
## Updated DB Schema
![alt text](https://raw.githubusercontent.com/keertan-krishnandraup/assign2/master/schema.png)

## Execution Steps
1. Run MongoDB and Flask servers on local machine, on default ports.
1. Execute populate_db.sh by running bash populate_db.sh
1. DB is now populated with schema as shown above.
1. API Calls can be made through Postman. APIs found in apis.py
1. Queries are implemented in queries.py

## APScheduler
Found in scheduler.py

## APIs
### Found in apis.py file
* Posts : **Route**: /posts **Role**: To find all posts of all users
* Single Post: **Route**: /posts/1 **Role**: To find a post with a particular Post ID
* Comments: **Route**: /all_comments **Role**: To find all comments for all posts for all users
* Comments of a post: **Route**: /comments?postId=5 **Role**: To find all comments for a particular post
* Posts of a user: **Route**: /post?userId=1 **Role**: To find all posts for a particular user
* Delete Post: **Route**: /del_post/5 **Role** : To delete a particular post by specifying it's ID
* Add Post: **Route**: /postsu **Role**: To add a post, as long as there isn't a post with the same ID **Sample Request Body**:
{ "userId":1,
   "id":5,
   "title":"new title",
   "body":"new body"
}
* Add Comment: **Route**: /addcomments **Role**: To add a comment, as long as a comment with the same ID does not exist  
**Sample Request Body**:
{
  "postId":5,
  "id":3567,
  "name":"Keertan",
  "email":keertan.krishnan@draup.com,
  "body":"new comment"
}
##### New
* Get Photo: **Route**:/get_photo?photoId=4 **Role**: To retrieve a particular photo by ID
* Photos in Album: **Route**:/get_all_photos?albumId=5 **Role**: To retrieve all photos of an album, specified by an ID 
* Get Albums: **Route**:/albums?userId=1 **Role**: To find all albums of a particular user
* Get Todos: **Route**:/todos?userId=1 **Role**: To find all todos of a particular user
* Create Album: **Route**:/create_album **Role**:To create an empty album(no photos) as long as there isn't one with the same ID **Sample Request Body**:
{  
   "userId":1,
   "id":3456,
   "title":"New Album"
}
* Create Photo: **Route**:/create_photo **Role**: To create a photo as long as the album and postid already exist **Sample Request Body**:
{
   "albumId": 2,
   "id": 34563,
   "title": "new photo",
   "url": "www.new.com",
   "thumbnailUrl": "www.new.com",
   "postId": 5
}
* Delete Album: **Route**:/del_album/4 **Role**: To delete a particular album as long as the ID exists
* Delete Photo: **Route**:/del_photo/34563 **Role**: To delete a particular photo as long as the ID exists

## Queries 
### Found in queries.py file
* Query 1 - Prahlad Rayapu : Find posts for a photo
* Query 2 - Prahlad Rayapu : Find comments for a photo
