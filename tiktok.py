import requests,os,json,random,glob
from unshortenit import UnshortenIt
def getIdFromURL(url):
    if url.__contains__("vm.tiktok.com") or url.__contains__("tiktok.com/t/"):
        us = UnshortenIt()
        url = us.unshorten(url)
    head, sep, tail = url.partition('?')
    url = head.split('/')
    return url[5]
def downloadVideo(videoId, update, context):
    image=False
    url = 'http://api2.musical.ly/aweme/v1/aweme/detail/?aweme_id='+videoId
    res = requests.get(
        url,
        headers = {
            'User-Agent' : 'okhttp',
        }
    )
    data = res.json()
    num = str(random.randrange(10000,99999))
    try:
        url2 = data['aweme_detail']['image_post_info']['images']
        image=True
    except KeyError:
        url2 = data['aweme_detail']['video']['play_addr']['url_list'][0]
    if(image==True):
        count = len(url2)
        count2 = 0
        while(count > count2):
            res2 = requests.get(
                url2[count2]['display_image']['url_list'][0],
                headers = {
                    'User-Agent' : 'okhttp',
                }
            )
            with open("./"+num+str(count2)+".webp", 'wb') as out:
                out.write(res2.content)
            context.bot.send_photo(chat_id=update.effective_chat.id, photo=open(num+str(count2)+".webp", 'rb'))
            count2=count2+1
        context.bot.send_message(chat_id=update.effective_chat.id, text="Here's your TikTok images!")
        for f in glob.glob(num+"*.webp"):
            os.remove(f)
        return None
    else:
        res2 = requests.get(
            url2,
            headers = {
                'User-Agent' : 'okhttp',
            }
        )
        with open("./"+num+".mp4", 'wb') as out:
            out.write(res2.content)
        context.bot.send_video(chat_id=update.effective_chat.id, video=open(num+".mp4", 'rb'))
        context.bot.send_message(chat_id=update.effective_chat.id, text="Here's your TikTok!")
        os.remove("./"+num+'.mp4')