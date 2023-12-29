from dateutil import parser
import datetime

class NewPostHandler:
    def __init__(self):
        self.user_steps = {}

    async def handle_command(self, event):
        self.user_steps[event.sender_id] = 'AWAITING_DATE'
        await event.respond('Будь ласка, введіть дату для публікації поста (наприклад, 2023-12-31).')

    async def handle_message(self, event):
        user_id = event.sender_id
        if user_id not in self.user_steps:
            return
        
        current_step = self.user_steps[user_id]

        if self.user_steps[user_id] == 'AWAITING_DATE':
            try:
                post_date = parser.parse(event.text, dayfirst=True).date()
                self.user_steps[user_id] = ('AWAITING_TIME', post_date)
                await event.respond('Тепер введіть час (наприклад, 18:00).')
            except ValueError:
                await event.respond('Некоректний формат дати. Спробуйте ще раз.')
        elif isinstance(current_step, tuple) and current_step[0] == 'AWAITING_TIME':
            try:
                post_time = parser.parse(event.text).time()
                post_datetime = datetime.datetime.combine(current_step[1], post_time)
                # Логіка запланування посту
                print(f"Заплановано пост на {post_datetime}.")
                await event.respond(f'Пост заплановано на {post_datetime}.')
                del self.user_steps[user_id]
            except ValueError:
                await event.respond('Некоректний формат часу. Спробуйте ще раз.')