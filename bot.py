import json
import aiohttp
from aiogram import Bot, Dispatcher, types
import asyncio


class CharacterBot:
    def __init__(self, bot_token):
        self.bot_token = bot_token
        self.bot = Bot(token=self.bot_token)
        self.dp = Dispatcher(self.bot)
        self.endpoint = 'http://95.217.14.178:8080/candidates_openai/gpt'
        self.headers = {'Content-Type': 'application/json'}

    async def send_request(self, messages):
        data = {
            'model': 'gpt-3.5-turbo',
            'messages': messages
        }

        async with aiohttp.ClientSession() as session:
            async with session.post(self.endpoint, headers=self.headers, data=json.dumps(data)) as response:
                response_text = await response.read()
                return response_text.decode("utf-8")

    async def handle_message(self, message):
        message_content = message.text
        role = 'user'
        message_data = {
            'role': role,
            'content': message_content
        }
        messages = [message_data]

        response = await self.send_request(messages)

        reply = json.loads(response)['choices'][0]['message']['content']
        await message.answer(reply)

    def register_handlers(self):
        self.dp.register_message_handler(
            self.handle_message, content_types=types.ContentType.TEXT
        )

    def run(self):
        loop = asyncio.get_event_loop()
        try:
            loop.run_until_complete(self.dp.start_polling())
        finally:
            loop.close()


def main():
    bot_token = '6293413845:AAGLJ1k1k7Cs7_-lto-mqhGSNScps1Ax8qQ'
    character_bot = CharacterBot(bot_token)
    character_bot.register_handlers()
    character_bot.run()


if __name__ == '__main__':
    main()
