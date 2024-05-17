from flask_login import UserMixin
from datetime import datetime


class User(UserMixin):
    def __init__(self, username, email, password):
        self.username = username
        self.email = email
        self.password = password


class Paper:
    def __init__(self, title, summary, url, publication_date, authors):
        self.title = title
        self.summary = summary
        self.url = url
        self.publication_date = publication_date
        self.authors = authors


class Post:
    def __init__(self, content, user_id, paper_id):
        self.content = content
        self.user_id = user_id
        self.paper_id = paper_id
        self.timestamp = datetime.now()
