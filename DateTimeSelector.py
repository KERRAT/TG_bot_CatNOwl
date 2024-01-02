from telethon import TelegramClient, events, Button
import datetime
import calendar
from modelsMenagers.UserDataManager import UserDataManager

class DateTimeSelector:
    DAYS_OF_WEEK = ["Пн", "Вт", "Ср", "Чт", "Пт", "Сб", "Нд"]
    _instance = None

    @classmethod
    def get_instance(cls, client):
        if cls._instance is None:
            cls._instance = cls(client)
        return cls._instance


    def __init__(self, client):
        if DateTimeSelector._instance is not None:
            raise Exception("This class is a singleton!")
        else:
            DateTimeSelector._instance = self

        self.client = client
        self.user_data_manager = UserDataManager()

        @self.client.on(events.CallbackQuery)
        async def callback_query_handler(event):
            sender_id = event.sender_id
            if self.user_data_manager.get_user_data(sender_id, 'last_message_id') == event.message_id:
                await self.callback_query_handler(event, sender_id)

    async def send_date_picker(self, event, sender_id, include_past=True, year=None, month=None):
        user_data = self.user_data_manager.get_or_create_user_data(sender_id)
                
        year = year or user_data.get_data('current_year')
        month = month or user_data.get_data('current_month')

        markup = self.create_calendar(year, month, include_past)
        msg_text = "Оберіть дату:"

        if user_data.get_data('last_message_id') and user_data.get_data('last_chat_id'):
            await event.client.edit_message(user_data.get_data('last_chat_id'), user_data.get_data('last_message_id'), msg_text, buttons=markup)
        else:
            msg = await event.respond(msg_text, buttons=markup)
            self.user_data_manager.set_user_data(sender_id, 'last_message_id', msg.id)
            self.user_data_manager.set_user_data(sender_id, 'last_chat_id', msg.chat_id)

    def create_calendar(self, year, month, include_past = True):
        today = datetime.date.today()

        # Додавання заголовку з місяцем і роком
        month_name = self.get_month_name(month)
        header = [Button.inline(f"{month_name} {year}", "ignore")]
        markup = [header]

        markup.extend([self.create_week_row(self.DAYS_OF_WEEK, "ignore")])

        month_calendar = calendar.monthcalendar(year, month)
        for week in month_calendar:
            week_buttons = self.create_week_buttons(week, year, month, today, include_past)
            markup.append(week_buttons)

        navigation_buttons = self.create_navigation_buttons(year, month, today, include_past)
        markup.append(navigation_buttons)

        return markup

    def create_week_row(self, days, callback_data):
        return [Button.inline(day, callback_data) for day in days]

    def create_week_buttons(self, week, year, month, today, include_past):
        week_buttons = []
        for day in week:
            if day == 0:
                week_buttons.append(Button.inline(" ", "ignore"))
            else:
                date = datetime.date(year, month, day)
                if include_past or date >= today:
                    week_buttons.append(Button.inline(str(day), f"date-{year}-{month}-{day}"))
                else:
                    week_buttons.append(Button.inline(" ", "ignore"))
        return week_buttons

    def get_month_name(self, month):
        # Повертає назву місяця
        month_names = ["Січень", "Лютий", "Березень", "Квітень", "Травень", "Червень",
                    "Липень", "Серпень", "Вересень", "Жовтень", "Листопад", "Грудень"]
        return month_names[month - 1]

    def create_navigation_buttons(self, year, month, today, include_past):
        prev_month, year_prev = (12, year - 1) if month == 1 else (month - 1, year)
        next_month, year_next = (1, year + 1) if month == 12 else (month + 1, year)

        buttons = []
        if include_past or (year > today.year or (year == today.year and month > today.month)):
            buttons.append(Button.inline("<", f"month-{year_prev}-{prev_month}-{int(include_past)}"))

        buttons.append(Button.inline(">", f"month-{year_next}-{next_month}-{int(include_past)}"))
        return buttons

    async def callback_query_handler(self, event, sender_id):
        user_data = self.user_data_manager.get_or_create_user_data(sender_id)
        data = event.data.decode('utf-8')

        if data.startswith("date-"):
            _, year, month, day = data.split('-')
            selected_date = datetime.date(int(year), int(month), int(day))
            user_data.set_data('selected_date', selected_date)
            self.user_data_manager.set_user_data(sender_id, 'selected_date', selected_date)
            await self.send_time_picker(event, selected_date, sender_id)
        elif data.startswith("month-"):
            _, year, month, include_past = data.split('-')
            self.user_data_manager.set_user_data(sender_id, 'current_year', int(year))
            self.user_data_manager.set_user_data(sender_id, 'current_month', int(month))
            await self.send_date_picker(event, sender_id, include_past=bool(int(include_past)), year=int(year), month=int(month))

    async def send_time_picker(self, event, selected_date, sender_id):
        user_data = self.user_data_manager.get_or_create_user_data(sender_id)
        markup = self.create_hour_selector()
        msg_text = f"Обрана дата: {selected_date}. Тепер оберіть час:"
        await event.client.edit_message(user_data.get_data('last_chat_id'), user_data.get_data('last_message_id'), msg_text, buttons=markup)

    def create_hour_selector(self):
        markup = []
        for hour in range(24):
            markup.append(Button.inline(f"{hour:02d}:00", f"time-{hour}"))
            markup.append(Button.inline(f"{hour:02d}:30", f"time-{hour}-30"))
        return [markup[i:i + 4] for i in range(0, len(markup), 4)]  # 4 години в рядку
