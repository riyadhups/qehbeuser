import os, json, time, asyncio, sys, shutil, heroku3, random, requests
from asyncio.exceptions import TimeoutError
from pyrogram import filters, Client
from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton
from telethon import TelegramClient
from telethon.sessions import StringSession
from telethon.tl.functions.channels import EditPhotoRequest, CreateChannelRequest
from telethon.errors import PhoneNumberInvalidError, PhoneCodeInvalidError, PhoneCodeExpiredError, SessionPasswordNeededError, PasswordHashInvalidError
from time import time
from asyncio import get_event_loop
from git import Repo
from bot import Bot as bot
import tracemalloc
tracemalloc.start()

@bot.on_message(filters.command('start') & filters.private)
async def start(client: Client, message: Message):
    text = f"<b>🇦🇿 Salam {message.from_user.first_name} Mən FastUserBot üçün yaradılmış qurulum botuyam\n\nℹ️Qurulum üçün sizə Heroku ApiKey Lazımdır.\n\n🆘Heroku ApiKey almaq üçün heroku.com 'a daxil olaraq ala bilərsiniz\n\n❕Qurulumu başlatmaq üçün /fast yazın.</b>"
    reply_markup = InlineKeyboardMarkup([[InlineKeyboardButton("📢 Rəsmi Kanal", url=f"https://t.me/thefastresmi")], [InlineKeyboardButton("👨🏻‍🔧 Support", url=f"https://t.me/TheFastSup")], [InlineKeyboardButton("👑 Məni Yaradan", url=f"https://t.me/FUBOwnerr")]])
    await message.reply(text = text, reply_markup = reply_markup, quote = True, disable_web_page_preview = True)

@bot.on_message(filters.command('alive') & filters.group)
async def alive(Bot, message: Message):
    id = message.chat.id
    img = "https://telegra.ph//file/99f74a87eeba21bee4a4d.jpg"
    text = f"<b>╔═════════════════\n║▻ FAST & DEPLOY Aktivdir\n║\n║▻ 🪧 Qrupun adı\n║▻ {message.chat.title}\n║▻ 💠 Python versiyası: 3.10.0\n║▻ 🏷️ Fast Userbot: v3\n║▻ 💎 Telethon versiyası: 1.24.0\n║▻ 💻 Pyrogram versiyası: 1.2.20\n║▻ 👑 Məni Yaradan\n║▻ 👤 [Sako Huseynovh](t.me/fubownerr)\n╚═════════════════</b>"
    await Bot.send_video(id, img, text)


def rm_r(path):
    if not os.path.exists(path):
        return
    if os.path.isfile(path) or os.path.islink(path):
        os.unlink(path)
    else:
        shutil.rmtree(path)

@Client.on_message(filters.private & ~filters.forwarded & filters.command('fast'))
async def husu(bot, msg):
    loop = get_event_loop()
    user_id = msg.chat.id
    aid = 17202681
    ash = "ef4d6e4de6f924085a01988b1bc751f0"
    api_msg = await bot.ask(user_id, "(i) **Fast Userbot Qurulumu başlayır**\n\n__(i) Zəhmət olmasa heroku API keyinizi daxil edin__", filters=filters.text)
    api = api_msg.text
    heroku_conn = heroku3.from_key(api)
    try:
        heroku_conn.apps()
    except:
        await msg.reply("⚠️) **Heroku ApiKey yanlış daxil etdiniz**")
        return
    await msg.reply("(✅) **Herokuya Giriş Uğurlu Oldu!**")

    # Telegram Prosesləri #
    phone_number_msg = await bot.ask(user_id, "📞 **İndi isə' telefon nömrənizi daxil edin.\n(i) Nümunə:** `+994551234567`", filters=filters.text)
    phone_number = phone_number_msg.text
    client = TelegramClient(StringSession(), 17202681, "ef4d6e4de6f924085a01988b1bc751f0")
    await client.connect()
    try:
        code = await client.send_code_request(phone_number)
    except PhoneNumberInvalidError:
        await msg.reply("(⚠️) **Telefon nömrəniz yanlışdır. Qurulumu yenidən başlat.** /fast")
        return
    try:
        phone_code_msg = await bot.ask(user_id, "**📳 Telegram hesabınıza göndərilmiş kodu bura daxil edin.\n(⚠️) Rəqəmlərin arasına mütləq (boşluq) buraxın.\n🔐 Kod bu şəkildə olur** '12345' **siz isə belə göndərin:** `0 0 0 0 0` InlineKeyboardMarkup([[InlineKeyboardButton("📢 Rəsmi Kanal", url=f"https://t.me/+42777")", filters=filters.text, timeout=600)
    except TimeoutError:

        
        await msg.reply("📢 **Vaxt limiti 10 dəqiqəyə çatdı. Qurulumu yenidən başlat.** /fast")
        return
    phone_code = phone_code_msg.text.replace(".", "")
    try:
        await client.sign_in(phone_number, phone_code, password=None)
    except PhoneCodeInvalidError:
        await msg.reply("(⚠️) **Doğrulama kodu etibarsızdır. Qurulumu yenidən başlat.** /fast")
        return
    except PhoneCodeExpiredError:
        await msg.reply("(⚠️) **Doğrulama kodununun müddəti başa çatıb. Qurulumu yenidən başlat.** /fast")
        return
    except SessionPasswordNeededError:
        try:
            two_step_msg = await bot.ask(user_id, "**(🆘) Hesabınızda iki addımlı doğrulama aşkar edildi.\n✍🏻 Zəhmət olmasa iki addımlı kodu daxil edin.**", filters=filters.text, timeout=300)
        except TimeoutError:
            await msg.reply("**(⚠️) Vaxt limiti 5 dəqiqəyə çatdı. Zəhmət olmasa qurulumu yenidən başlat.** /fast")
            return
        try:
            password = two_step_msg.text
            await client.sign_in(password=password)
        except PasswordHashInvalidError:
            await two_step_msg.reply("(⚠️) **İki adımlı doğrulama yanlış daxil edilib. Qurulumu yenidən başlat.** /fast", quote=True)
            return
    string = client.session.save()
    await client.send_message("me", "🗽 **Fast UserBot Avtomatik Mesaj\n\n💠 Salam Hesabınıza ⚡️ Fast Userbot qurursunuz. Userbotu qurarkən @TheFastSup qrup və @TheFastPlugin kanalına avtomatik olaraq əlavə olunursunuz.\n\n💎 Fast​ UserBotu şeçdiyiniz üçün təşəkkürlər\n\n🆘Support Üçün Və İş Birliyi Üçün @FUBOwnerr**")
    Qrup = await client(CreateChannelRequest(title='🇦🇿Fast Botlog🇦🇿', about="Fast Userbot", megagroup=True))
    Qrup = Qrup.chats[0].id
    foto = await client.upload_file(file='FastLog.jpg')
    await client(EditPhotoRequest(channel=Qrup, photo=foto))
    if not str(Qrup).startswith("-100"):
        Qrup = int(f"-100{str(Qrup)}")
    await client.disconnect()
    await msg.reply("(✅) StringSession Uğurla Alındı!")

    appname = "fastuserbot" + str(time() * 1000)[-4:].replace(".", "") + str(random.randint(0,500))
    try:
        heroku_conn.create_app(name=appname, stack_id_or_name='container', region_id_or_name="eu")
    except requests.exceptions.HTTPError:
        await msg.reply("**(⚠️) Herokuda 5 app aşkar edildi app'ları silib qurulumu yenidən başlat.**")
        return

    await bot.send_message(-1001718954263, "ℹ️FastUserBot üçün qurulum başlatdım.\n\n🆘Qurulumu Bitdikdə.\n\n❕Xəbər Edəcəm:::)")

    await msg.reply("ℹ️ Qurulum Başladı... \n\n(i) __Bu proses təxminən 2-3dəqiqə çəkir__")
    if os.path.isdir("./fastuserbot/"):
        rm_r("./fastuserbot/")
    repo = Repo.clone_from("https://github.com/fastuserbot/fastuserbot", "./fastuserbot/", branch="main")
    app = heroku_conn.apps()[appname]
    giturl = app.git_url.replace("https://", "https://api:" + api + "@")
    if "heroku" in repo.remotes:
        remote = repo.remote("heroku")
        remote.set_url(giturl)
    else:
        remote = repo.create_remote("heroku", giturl)
    try:
        remote.push(refspec="HEAD:refs/heads/master", force=True)
    except Exception as e:
        await msg.reply(f"(⚠️) Xəta Baş Verdi: {e}")

    app.install_addon(plan_id_or_name='062a1cc7-f79f-404c-9f91-135f70175577', config={})
    config = app.config()

    config['API_HASH'] = "ef4d6e4de6f924085a01988b1bc751f0"
    config['API_KEY'] = 17202681
    config['BOTLOG'] = "True"
    config['BOTLOG_CHATID'] = Qrup
    config['COUNTRY'] = "Azerbaijan"
    config['HEROKU_APIKEY'] = api
    config['HEROKU_APPNAME'] = appname
    config['STRING_SESSION'] = string
    config['TZ'] = "Asia/Baku"
    config['LANGUAGE'] = "AZ"
    config['UPSTREAM_REPO'] = "https://github.com/fastuserbot/fastuserbot.git"

    await msg.reply("**Fast Userbot aktiv olunur**")
    try:
        app.process_formation()["worker"].scale(1)
    except:
        await msg.reply("(⚠️) Fayllar yüklənərkən bir xəta baş verdi. Xahiş edirik qurulumu yenidən başlat /fast")
        return

    await bot.send_message(-1001718954263, "✅Qurulum Uğurla Başa Çatdı✅\n\n")

    await msg.reply("🎉 **Qurulum uğurla başa çatdı!**\n\n__Bir neçə saniyə sonra hər hansısa Qrupa .alive yazaraq userbotunuzu test edə bilərsiniz\n\nℹ️ FastUserBot'u seçdiyiniz üçün\n\nℹ️ Təşəkkür Edirik.")
