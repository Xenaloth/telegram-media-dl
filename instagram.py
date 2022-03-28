import json,os
from instagrapi import Client
from instagrapi.exceptions import (
    MediaNotFound
)
creds = open('creds.json',)
creds = json.load(creds)
cl = Client()
cl.login(creds["username"], creds["password"])
def getMediaType(update, context):
    mediatype = None
    producttype = None
    highlight = False
    story = False
    try:
        if 'stories/' in update.effective_message.text:
            story = True
            if '/highlights' in update.effective_message.text:
                highlight = True
                media = cl.highlight_pk_from_url(update.message.text)
            else:
                media = cl.story_pk_from_url(update.message.text)
        elif '/p/' or '/tv/' or '/reel/' in update.effective_message.text:
            media = cl.media_pk_from_url(update.message.text)
            mediatype = cl.media_info(media).dict()['media_type']
            producttype = cl.media_info(media).dict()['product_type']
        else:
            head, sep, tail = update.effective_message.text.partition('?')
            user = head.split('/')
            uid = cl.user_id_from_username(user[3])
            cl.user_follow(uid)
            context.bot.send_message(chat_id=update.effective_chat.id, text="Followed "+user[3]+"!")
            return False
        download(update, context, media, mediatype, producttype, story, highlight)
    except MediaNotFound:
        context.bot.send_message(chat_id=update.effective_chat.id, text="Could not find media! Please check the account isn't private, or if it is, send a link to the profile to automatically follow!")
def download(update, context, media, mediatype, producttype, story=False, highlight=False):
    if mediatype == 1:
        media_path = cl.photo_download(media)
        context.bot.send_photo(chat_id=update.effective_chat.id, caption='Here\'s your photo!', photo=open(media_path, 'rb'))
        os.remove(media_path)
    elif mediatype == 2:
        if producttype == 'feed':
            media_path = cl.video_download(media)
            context.bot.send_video(chat_id=update.effective_chat.id, caption='Here\'s your video!', video=open(media_path, 'rb'))
        elif producttype == 'igtv':
            media_path = cl.igtv_download(media)
            context.bot.send_video(chat_id=update.effective_chat.id, caption='Here\'s your igtv!', video=open(media_path, 'rb'))
        elif producttype == 'clips':
            media_path = cl.clip_download(media)
            context.bot.send_video(chat_id=update.effective_chat.id, caption='Here\'s your clip!', video=open(media_path, 'rb'))
        os.remove(media_path)
    elif mediatype == 8:
        media_path = cl.album_download(media)
        for i in media_path:
            if str(i).endswith('.jpg') or str(i).endswith('.png') or str(i).endswith('.jpeg') or str(i).endswith('.webp'):
                context.bot.send_photo(chat_id=update.effective_chat.id, photo=open(i, 'rb'))
            elif str(i).endswith('.mp4'):
                context.bot.send_video(chat_id=update.effective_chat.id, video=open(i, 'rb'))
            os.remove(i)
        context.bot.send_message(chat_id=update.effective_chat.id, text='Here\'s your album!')
    elif highlight:
        ids = cl.highlight_info(media).dict()['media_ids']
        for i in ids:
            media_path = cl.story_download(i)
            context.bot.send_video(chat_id=update.effective_chat.id, caption='', video=open(media_path, 'rb'))
            os.remove(media_path)
        context.bot.send_message(chat_id=update.effective_chat.id, text='Here\'s your highlight!')
    elif story:
        user = cl.story_info(media).dict()['user']
        user = user['username']
        user = cl.user_id_from_username(user)
        ids = cl.user_stories(user)
        for i in ids:
            media_path = cl.story_download(i.dict()['pk'])
            context.bot.send_video(chat_id=update.effective_chat.id, caption='', video=open(media_path, 'rb'))
            os.remove(media_path)
        context.bot.send_message(chat_id=update.effective_chat.id, text='Here\'s your story!')