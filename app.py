from telegram import Update
from telegram.ext import Updater, CommandHandler, CallbackContext, MessageHandler, Filters
import tiktok,instagram,youtube,reddit,json,os
creds = open('creds.json',)
creds = json.load(creds)
def start(update: Update, context: CallbackContext) -> None:
    update.message.reply_text(f'Hello, {update.effective_user.first_name}! To use this bot, send a link to an instagram or tiktok post! Note: currently only supports public tiktok accounts.')
    update.message.reply_text(f'This bot also supports youtube videos! However, telegram limits bot uploads to 50mb.')
def instagramHandler(update: Update, context: CallbackContext):
    context.bot.send_message(chat_id=update.effective_chat.id, text="Processing Instagram...")
    try:
        instagram.getMediaType(update, context)
    except:
        context.bot.send_message(chat_id=update.effective_chat.id, text="An error occurred processing the Instagram URL.")
def tiktokHandler(update: Update, context: CallbackContext):
    context.bot.send_message(chat_id=update.effective_chat.id, text="Processing TikTok...")
    try:
        filename = tiktok.downloadVideo(tiktok.getIdFromURL(update.message.text))
        context.bot.send_video(chat_id=update.effective_chat.id, video=open(filename, 'rb'))
        context.bot.send_message(chat_id=update.effective_chat.id, text="Here's your TikTok!")
        os.remove("./"+filename)
    except:
        context.bot.send_message(chat_id=update.effective_chat.id, text="An error occurred processing the TikTok.")
def youtubeHandler(update: Update, context: CallbackContext):
    context.bot.send_message(chat_id=update.effective_chat.id, text="Processing YouTube...")
    try:
        filename = youtube.downloadVideo(update.message.text)
        context.bot.send_video(chat_id=update.effective_chat.id, video=open(filename, 'rb'), timeout=500)
        context.bot.send_message(chat_id=update.effective_chat.id, text="Here's your YouTube video!")
        os.remove("./"+filename)
    except:
       context.bot.send_message(chat_id=update.effective_chat.id, text="An error occurred processing the YouTube video.")
       files = os.listdir("./")
       for f in files:
           if not os.path.isdir(f) and ".mkv" in f:
               os.remove(f)
def redditHandler(update: Update, context: CallbackContext):
    context.bot.send_message(chat_id=update.effective_chat.id, text="Processing Reddit...")
    media,name = reddit.download(update.message.text)
    reddit.handleMedia(media, name, update, context)
updater = Updater(creds["telegram_token"], base_url=creds["api_url"])
updater.dispatcher.add_handler(CommandHandler('start', start))
instagram_handler = MessageHandler(Filters.regex('(instagram\.com)'), instagramHandler)
tiktok_handler = MessageHandler(Filters.regex('(tiktok\.com)'), tiktokHandler)
youtube_handler = MessageHandler(Filters.regex('(youtube\.com|youtu\.be)'), youtubeHandler)
reddit_handler = MessageHandler(Filters.regex('(reddit\.com|redd\.it)'), redditHandler)
updater.dispatcher.add_handler(instagram_handler)
updater.dispatcher.add_handler(tiktok_handler)
updater.dispatcher.add_handler(youtube_handler)
updater.dispatcher.add_handler(reddit_handler)
updater.start_polling()
updater.idle()