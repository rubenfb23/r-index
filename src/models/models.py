from flask_login import UserMixin
from datetime import datetime


class User(UserMixin):
    def __init__(self, username, email, password):
        self.username = username
        self.email = email
        self.password = password

    def get_id(self):
        return self.username

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
    def __init__(self, content, user_id, paper_id, score):
        self.content = content
        self.user_id = user_id
        self.paper_id = paper_id
        self.score = score
        self.timestamp = datetime.now()

    def to_dict(self):
        return {
            "_id": str(self._id),
            "content": self.content,
            "user_id": self.user_id,
            "paper_id": self.paper_id,
            "timestamp": self.timestamp.isoformat()
        }
