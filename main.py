import asyncio
import logging
import os
from io import BytesIO

import aiohttp
from aiogram import Bot, Dispatcher, F
from aiogram.types import Message

logging.basicConfig(level=logging.INFO)
log = logging.getLogger('aqua-reposter')

BOT_TOKEN = os.environ['TELEGRAM_BOT_TOKEN']
PAGE_ID = os.environ['FACEBOOK_PAGE_ID']
PAGE_TOKEN = os.environ['FACEBOOK_PAGE_TOKEN']
CHANNEL = os.getenv('TELEGRAM_CHANNEL_USERNAME', '@AquaWorld_Official').lstrip('@').lower()
GRAPH_VERSION = os.getenv('FACEBOOK_GRAPH_VERSION', 'v24.0')
BASE = f'https://graph.facebook.com/{GRAPH_VERSION}/{PAGE_ID}'

bot = Bot(BOT_TOKEN)
dp = Dispatcher()

async def fb_post(session, endpoint, data, image=None):
    if image is None:
        payload = {**data, 'access_token': PAGE_TOKEN}
        async with session.post(f'{BASE}/{endpoint}', data=payload) as r:
            result = await r.json(content_type=None)
    else:
        form = aiohttp.FormData()
        for key, val in {**data, 'access_token': PAGE_TOKEN}.items():
            form.add_field(key, str(val))
        form.add_field('source', image, filename='aqua.jpg', content_type='image/jpeg')
        async with session.post(f'{BASE}/{endpoint}', data=form) as r:
            result = await r.json(content_type=None)
    if 'error' in result or 'id' not in result:
        raise RuntimeError(f'Facebook API failed: {result}')
    return result

@dp.channel_post()
async def repost(message: Message):
    username = (message.chat.username or '').lower()
    if username != CHANNEL:
        log.warning('Ignored channel: %s', username)
        return
    caption = message.caption or message.text or ''
    try:
        async with aiohttp.ClientSession(timeout=aiohttp.ClientTimeout(total=90)) as session:
            if message.photo:
                photo = message.photo[-1]
                file = await bot.get_file(photo.file_id)
                buffer = BytesIO()
                await bot.download_file(file.file_path, destination=buffer)
                result = await fb_post(session, 'photos', {'message': caption}, buffer.getvalue())
            elif message.text:
                result = await fb_post(session, 'feed', {'message': caption})
            else:
                log.info('Unsupported message type %s', message.message_id)
                return
        log.info('Reposted message %s -> %s', message.message_id, result['id'])
    except Exception:
        log.exception('Failed to repost message %s', message.message_id)

async def main():
    await bot.delete_webhook(drop_pending_updates=False)
    await dp.start_polling(bot, allowed_updates=['channel_post'])

if __name__ == '__main__':
    asyncio.run(main())
