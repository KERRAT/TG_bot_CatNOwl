import datetime
from models.Post import Post
import uuid

class UserData:
    def __init__(self):
        today = datetime.date.today()
        self.selected_date = None #TODO transver to posts
        self.current_year = today.year
        self.current_month = today.month
        self.last_message_id = None
        self.last_chat_id = None
        self.current_step = None
        self.posts = {}  # Dictionary to store Post objects

    def update_date(self):
        today = datetime.date.today()
        self.current_year = today.year
        self.current_month = today.month

    def set_data(self, key, value):
        if hasattr(self, key):
            setattr(self, key, value)

    def get_data(self, key):
        return getattr(self, key, None)

    def add_post(self, post):
        if not isinstance(post, Post):
            raise ValueError("post must be an instance of Post")
        post_id = str(uuid.uuid4())
        self.posts[post_id] = post
        return post_id

    def get_post(self, post_id):
        return self.posts.get(post_id)

    def update_post(self, post_id, new_post):
        if not isinstance(new_post, Post):
            raise ValueError("new_post must be an instance of Post")
        if post_id in self.posts:
            self.posts[post_id] = new_post
        else:
            raise KeyError("Post not found")

    #TODO Add more methods as needed (e.g., delete_post, etc.)