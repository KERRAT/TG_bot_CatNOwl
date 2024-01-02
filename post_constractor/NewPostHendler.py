from dateutil import parser
import datetime
from DateTimeSelector import DateTimeSelector
from telethon import TelegramClient, events
from modelsMenagers.UserDataManager import UserDataManager

class NewPostHandler:
    def __init__(self, client):
        self.user_data_manager = UserDataManager()
        self.date_time_selector = DateTimeSelector.get_instance(client=client)
        self.client = client

    async def handle_command(self, event):
        self.user_data_manager.update_user_step(event.sender_id, 'AWAITING_DATE')
        await self.date_time_selector.send_date_picker(event, event.sender_id, False)

    async def handle_message(self, event):
        user_id = event.sender_id
        current_step = self.user_data_manager.get_user_step(user_id)
        