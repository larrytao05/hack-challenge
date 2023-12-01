import os
from db import db
from flask import Flask, request
import json
from db import User
from db import Post
from datetime import datetime

app = Flask(__name__)
db_filename = "cufound.db"

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///%s" % db_filename
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["SQLALCHEMY_ECHO"] = True

db.init_app(app)
with app.app_context():
    db.create_all()

# generalized response formats
def success_response(data, code=200):
    return json.dumps(data), code

def failure_response(message, code=404):
    return json.dumps({"error": message}), code


# your routes here
@app.route("/")
@app.route("/api/posts/")
def get_posts():
    """
    Get all posts
    """
    posts = [post.serialize() for post in Post.query.all()]
    return success_response({"posts":posts})

@app.route("/api/posts/<string:netid>/", methods=["POST"])
def create_post(netid):
    """
    Create a post
    """
    body = json.loads(request.data)
    new_post = Post(
        item_name=body.get('item_name'),
        item_desc=body.get('item_desc'),
        date = datetime.utcnow().timestamp(),
        loc_name=body.get('loc_name'),
        loc_desc=body.get('loc_desc'),
        user_id=User.query.filter_by(netid=netid).first().id,
        post_type=body.get('post_type'),
        image_url=body.get('image_url')
    )
    if (
            new_post.item_name is None or 
            new_post.item_desc is None or
            new_post.loc_name is None or
            new_post.user_id is None or 
            new_post.post_type is None
        ):
        return failure_response("Missing one or more fields!", 400)
    db.session.add(new_post)
    db.session.commit()
    return success_response(new_post.serialize(), 201)

@app.route("/api/posts/<int:post_id>/")
def get_post_by_id(post_id):
    """
    Get a post by its id
    """
    post = Post.query.filter_by(id=post_id).first()
    if post is None:
        return failure_response("Course not found!", 404)
    return success_response(post.serialize())
    
@app.route("/api/posts/<int:post_id>/", methods=["DELETE"])
def delete_post_by_id(post_id):
    """
    Delete a post by its id
    """
    post = Post.query.filter_by(id=post_id).first()
    if post is None:
        return failure_response("Course not found!", 404)
    db.session.delete(post)
    db.session.commit()
    return success_response(post.serialize(), 200)

@app.route("/api/users/", methods=["POST"])
def create_user():
    """
    Create a user
    """
    body = json.loads(request.data)
    new_user = User(
        name=body.get('name'),
        netid=body.get('netid'),
    )
    if (
            new_user.name is None or new_user.netid is None
        ):
        return failure_response("Missing one or more fields!", 400)
    db.session.add(new_user)
    db.session.commit()
    return success_response(new_user.serialize(), 201)

@app.route("/api/user/<int:user_id>/")
def get_user_by_id(user_id):
    """
    Get a user by its id
    """
    user = User.query.filter_by(id=user_id).first()
    if user is None:
        return failure_response("User not found!", 404)
    return success_response(user.serialize(), 200)

@app.route("/api/users/<string:netid>/")
def get_user_by_netid(netid):
    """
    Get user by netid
    """
    user = User.query.filter_by(netid=netid).first()
    if user is None:
        return failure_response("User not found!", 404)
    return success_response(user.serialize(), 200)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000, debug=True)

