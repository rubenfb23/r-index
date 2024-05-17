from flask_login import UserMixin
from datetime import datetime
from sirope import OID  # Import OID class
import uuid


class User(UserMixin):
    def __init__(self, username, email, password):
        self.username = username
        self.email = email
        self.password = password

    def get_id(self):
        return self.username

    def to_dict(self):
        return {
            "username": self.username,
            "email": self.email,
            "password": self.password
        }

    @classmethod
    def from_dict(cls, data):
        return cls(data["username"], data["email"], data["password"])


class Paper:
    def __init__(self, title, summary, url, publication_date, authors):
        self.title = title
        self.summary = summary
        self.url = url
        self.publication_date = publication_date
        self.authors = authors


class Post:
    def __init__(self, content, user_id, paper_id):
        self._id = OID(Post, uuid.uuid4().int)  # Use OID class
        self.content = content
        self.user_id = user_id
        self.paper_id = paper_id
        self.timestamp = datetime.now()

    def get_id(self):
        return self._id

    def to_dict(self):
        return {
            "_id": str(self._id),
            "content": self.content,
            "user_id": self.user_id,
            "paper_id": self.paper_id,
            "timestamp": self.timestamp.isoformat()
        }

    @classmethod
    def from_dict(cls, data):
        post = cls(
            data["content"],
            data["user_id"],
            data["paper_id"]
        )
        post._id = OID.from_text(data["_id"])
        post.timestamp = datetime.fromisoformat(data["timestamp"])
        return post
