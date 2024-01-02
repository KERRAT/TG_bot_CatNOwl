from models.UserData import UserData

class UserDataManager:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(UserDataManager, cls).__new__(cls)
            cls._instance.users_data = {}
        return cls._instance

    def get_or_create_user_data(self, user_id):
        if user_id is None:
            raise ValueError("User ID is required")

        if user_id not in self.users_data:
            self.users_data[user_id] = UserData()
        else:
            self.users_data[user_id].update_date()

        return self.users_data[user_id]

    def set_user_data(self, user_id, key, value):
        if user_id is None:
            raise ValueError("User ID is required")

        user_data = self.get_or_create_user_data(user_id)
        user_data.set_data(key, value)

    def get_user_data(self, user_id, key):
        if user_id is None:
            raise ValueError("User ID is required")

        user_data = self.get_or_create_user_data(user_id)
        return user_data.get_data(key)

    def update_user_step(self, user_id, step):
        self.set_user_data(user_id, 'current_step', step)

    def get_user_step(self, user_id):
        return self.get_user_data(user_id, 'current_step')
    
    def reset_last_message_id(self, user_id):
        if user_id is None:
            raise ValueError("User ID is required")
        
        self.set_user_data(user_id, 'last_message_id', None)
