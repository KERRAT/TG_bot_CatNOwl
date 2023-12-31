from dotenv import dotenv_values
from telethon import TelegramClient, events
from post_constractor.NewPostHendler import NewPostHandler
from DateTimeSelector import DateTimeSelector

config = dotenv_values(".env")

user_steps = {}

async def main():
    async with TelegramClient('anon', config["api_id"], config["api_hash"]) as client:

        # Отримання інформації про поточного користувача
        me = await client.get_me()
        bot_user_id = me.id


        @client.on(events.NewMessage(pattern='/start'))
        async def start_handler(event):
            await event.respond('Привіт! Я твій бот. Використовуй /newpost, щоб створити новий пост.')

        @client.on(events.NewMessage(pattern='/newpost'))
        async def command_handler(event):
            new_post_handler = NewPostHandler(client)
            await new_post_handler.handle_command(event)

        @client.on(events.NewMessage)
        async def message_handler(event):
            # Ігнорування повідомлень від бота
            if event.sender_id == bot_user_id:
                return

            # Ігнорування команд
            if event.message.text.startswith('/'):
                return

            await new_post_handler.handle_message(event)

        print("Бот запущено...")
        await client.run_until_disconnected()

if __name__ == '__main__':
    import asyncio
    asyncio.run(main())