from telethon import TelegramClient, events, Button
import datetime
import calendar

class DateTimeSelector:
    
    def __init__(self, client, include_past=True):
        self.selected_date = None
        self.current_year = datetime.date.today().year
        self.current_month = datetime.date.today().month
        self.include_past = include_past
        self.last_message_id = None
        self.last_chat_id = None
        self.client = client

        @self.client.on(events.CallbackQuery)
        async def callback_query_handler(event):
            if(event.message_id == self.last_message_id):
                await self.callback_query_handler(event)

    async def send_date_picker(self, event, year=None, month=None):
        if year is None or month is None:
            year = self.current_year
            month = self.current_month

        self.today = datetime.date.today()
        markup = self.create_calendar(year, month)

        if self.last_message_id and self.last_chat_id:
            await event.client.edit_message(self.last_chat_id, self.last_message_id, "Оберіть дату:", buttons=markup)
        else:
            msg = await event.respond("Оберіть дату:", buttons=markup)
            self.last_message_id = msg.id
            self.last_chat_id = msg.chat_id

            
    def create_calendar(self, year, month):
        markup = []
        is_back_button = True
        days = ["Пн", "Вт", "Ср", "Чт", "Пт", "Сб", "Нд"]
        markup.append([Button.inline(day, "ignore") for day in days])

        month_calendar = calendar.monthcalendar(year, month)
        for week in month_calendar:
            week_buttons = []
            for day in week:
                if day == 0 or (not self.include_past and datetime.date(year, month, day) < self.today):
                    week_buttons.append(Button.inline(" ", "ignore"))
                    if(day != 0):
                        is_back_button = False
                else:
                    week_buttons.append(Button.inline(str(day), f"date-{year}-{month}-{day}"))
            markup.append(week_buttons)

        # Кнопки для переключення місяців
        buttons = []
        prev_month, year_prev = (12, year - 1) if month == 1 else (month - 1, year)
        next_month, year_next = (1, year + 1) if month == 12 else (month + 1, year)
        if(not self.include_past and is_back_button):
            buttons.append(Button.inline("<", f"month-{year_prev}-{prev_month}"))
        buttons.append(Button.inline(">", f"month-{year_next}-{next_month}"))
        markup.append(buttons)  # Append the buttons to the existing markup list
        return markup

    async def callback_query_handler(self, event):
        data = event.data.decode('utf-8')
        if data.startswith(f"date-"):
            _, year, month, day = data.split('-')
            self.selected_date = datetime.date(int(year), int(month), int(day))
            await self.send_time_picker(event, self.selected_date)
        elif data.startswith(f"month-"):
            _, year, month = data.split('-')
            self.current_year, self.current_month = int(year), int(month)
            if self.last_message_id and self.last_chat_id:
                await self.send_date_picker(event, year=self.current_year, month=self.current_month)
            else:
                await self.send_date_picker(event, year=self.current_year, month=self.current_month)

    async def send_time_picker(self, event, selected_date):
        markup = self.create_hour_selector()
        await event.client.edit_message(self.last_chat_id, self.last_message_id, f"Обрана дата: {selected_date}. Тепер оберіть час:", buttons=markup)

    def create_hour_selector(self):
        markup = []
        for hour in range(24):
            markup.append(Button.inline(f"{hour}:00", f"time-{hour}"))
            markup.append(Button.inline(f"{hour}:30", f"time-{hour}-30"))
        return [markup[i:i + 4] for i in range(0, len(markup), 4)]  # 4 години в рядку