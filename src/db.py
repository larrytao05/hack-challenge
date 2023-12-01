from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class User(db.Model):
    """
    User Model
    """
    __tablename__ = "user"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String, nullable=False)
    netid = db.Column(db.String, nullable=False)
    posts = db.relationship("Post", cascade="delete")

    def __init__(self, **kwargs):
        """
        Initialize a User object
        """
        self.name= kwargs.get("name", "")
        self.netid = kwargs.get("netid", "")
    
    def serialize(self):
        """
        Serialize a user
        """
        return {
            "id": self.id,
            "name": self.name,
            "netid": self.netid,
            "posts": [post.serialize() for post in self.posts]
        }
    
class Post(db.Model):
    """
    Post Model
    """
    __tablename__ = "post"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    item_name = db.Column(db.String, nullable=False)
    item_desc = db.Column(db.String, nullable=True)
    date = db.Column(db.Float, nullable=False)
    loc_name = db.Column(db.String, nullable=False)
    loc_desc = db.Column(db.String, nullable=True)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)
    post_type = db.Column(db.Boolean, nullable=False) # false means a lost item, true is a found item
    image_url = db.Column(db.String, nullable=True)

    def __init__(self, **kwargs):
        """
        Initialize a Post object
        """
        self.item_name = kwargs.get("item_name", "")
        self.item_desc = kwargs.get("item_desc", "")
        self.date = kwargs.get("date", 0)
        self.loc_name = kwargs.get("loc_name", "")
        self.loc_desc = kwargs.get("loc_desc", "")
        self.user_id = kwargs.get("user_id", 0)
        self.post_type = kwargs.get("post_type", False)
        self.image_url = kwargs.get("image_url", "")
    
    def serialize(self):
        """
        Serialize a post
        """
        return {
            "id":self.id,
            "item_name":self.item_name,
            "item_desc":self.item_desc,
            "date": self.date,
            "loc_name":self.loc_name,
            "loc_desc":self.loc_desc,
            "netid":User.query.filter_by(id=self.user_id).first().netid,
            "post_type":self.post_type,
            "image_url":self.image_url
        }
