# Assignment 2 - User DB CRUD Operations
## Updated DB Schema
![alt text](https://raw.githubusercontent.com/keertan-krishnandraup/assign2/master/schema.png)

## APIs
### Found in apis.py file
* Posts : **route**: /posts **Role**: To find all posts of all users
* Single Post: **route**: /posts/1 **Role**: To find a post with a particular Post ID
* Comments: **route**: /all_comments **Role**: To find all comments for all posts for all users
* Comments of a post: **route**: /comments?postId=5 **Role**: To find all comments for a particular post
* Posts of a user: **route**: /post?userId=1 **Role**: To find all posts for a particular user
* Delete Post: **route**: /del_post/5 **Role** : To delete a particular post by specifying it's ID
* Add Post: **route**: /postsu **Role**: To add a post, as long as there isn't a post with the same ID **Sample Request Body**:
{ "userId":1,
   "id":5,
   "title":"new title",
   "body":"new body"
}
* Add Comment: **route**: /addcomments **Role**: To add a comment, as long as a comment with the same ID does not exist  
**Sample Request Body**:
{
  "postId":5,
  "id":3567,
  "name":"Keertan",
  "email":keertan.krishnan@draup.com,
  "body":"new comment"
}

## Queries 
### Found in queries.py file
* Query 1 - Prahlad Rayapu : Find posts for a photo
* Query 2 - Prahlad Rayapu : Find comments for a photo
