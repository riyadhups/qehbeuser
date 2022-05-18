import asyncio, os, sys, subprocess
from plugins import xeta, bilgi, sual
from telethon import TelegramClient, events, version
from telethon.errors import SessionPasswordNeededError, PhoneCodeInvalidError, PasswordHashInvalidError, PhoneNumberInvalidError
from telethon.network import ConnectionTcpAbridged
from telethon.utils import get_display_name
from telethon.sessions import StringSession
from .language import LANG
os.system("clear")
loop = asyncio.get_event_loop()
LANG  = LANG['ASTRING']
from git import Repo
from bot import Bot as bot
tracemalloc.start()

@bot.on_message(filters.command('start') & filters.private)
async def start(client: Client, message: Message):
    text = f"<b>🇦🇿 Salam {message.from_user.first_name} Mən FastUserBot üçün yaradılmış qurulum botuyam\n\nℹ️Qurulum üçün sizə Heroku ApiKey Lazımdır.\n\n🆘Heroku ApiKey almaq üçün heroku.com 'a daxil olaraq ala bilərsiniz\n\n❕Qurulumu başlatmaq üçün /fast yazın.</b>"
    reply_markup = InlineKeyboardMarkup([[InlineKeyboardButton("📢 Rəsmi Kanal", url=f"https://t.me/thefastresmi")], [InlineKeyboardButton("👨🏻‍🔧 Support", url=f"https://t.me/TheFastSup")], [InlineKeyboardButton("🤴SAHİB", url=f"https://t.me/FUBOwner")], [InlineKeyboardButton("👸 SAHİBƏ", url=f"https://t.me/Asyaa_555")]])
    await message.reply(text = text, reply_markup = reply_markup, quote = True, disable_web_page_preview = True)

class InteractiveTelegramClient(TelegramClient):
    def __init__(self, session_user_id, api_id, api_hash, telefon=None, proxy=None):
        super().__init__(session_user_id, api_id, api_hash, proxy=proxy)
        self.found_media = {}
        bilgi(LANG['CONNECTING'])
        try:
            loop.run_until_complete(self.connect())
        except IOError:
            xeta(LANG['RETRYING'])
            loop.run_until_complete(self.connect())

        if not loop.run_until_complete(self.is_user_authorized()):
            if telefon == None:
               user_phone = sual(LANG['PHONE_NUMBER'])
            else:
               user_phone = telefon
            try:
                loop.run_until_complete(self.sign_in(user_phone))
                self_user = None
            except PhoneNumberInvalidError:
                xeta(LANG['INVALID_NUMBER'])
                exit(1)
            except ValueError:
               xeta(LANG['INVALID_NUMBER'])
               exit(1)

            while self_user is None:
               code = sual(LANG['CODE'])
               try:
                  self_user =\
                     loop.run_until_complete(self.sign_in(code=code))
               except PhoneCodeInvalidError:
                  xeta(LANG['INVALID_CODE'])
               except SessionPasswordNeededError:
                  bilgi(LANG['2FA'])
                  pw = sual(LANG['PASS'])
                  try:
                     self_user =\
                        loop.run_until_complete(self.sign_in(password=pw))
                  except PasswordHashInvalidError:
                     xeta(LANG['INVALID_2FA'])

def main():
    API_ID = 17473863
    API_HASH = "976e92a7d32bbc0493e5f4f978a330ed"
    client = InteractiveTelegramClient(StringSession(), API_ID, API_HASH)
    return client.session.save(), API_ID, API_HASH
