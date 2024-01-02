from models.Post import Post

class UserPostManager:
    def __init__(self, user_data_manager):
        self.user_data_manager = user_data_manager

    def create_post(self, user_id, post):
        if not isinstance(post, Post):
            raise ValueError("post must be an instance of Post class")

        user_data = self.user_data_manager.get_or_create_user_data(user_id)
        return user_data.add_post(post)

    def get_posts(self, user_id):
        user_data = self.user_data_manager.get_or_create_user_data(user_id)
        return user_data.posts

    def get_post(self, user_id, post_id):
        user_data = self.user_data_manager.get_or_create_user_data(user_id)
        return user_data.get_post(post_id)

    def update_post(self, user_id, post_id, new_post):
        if not isinstance(new_post, Post):
            raise ValueError("new_post must be an instance of Post class")

        user_data = self.user_data_manager.get_or_create_user_data(user_id)
        user_data.update_post(post_id, new_post)

    # Add more methods as needed (e.g., delete_post, etc.)
