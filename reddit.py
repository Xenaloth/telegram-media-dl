from RedDownloader import RedDownloader
import os,random
def download(url):
    num = random.randrange(10000,99999)
    os.mkdir("reddit")
    out = RedDownloader.Download(url, 1080, destination="reddit", output=str(num))
    return out.GetMediaType(), str(num)
def handleMedia(mtype, name, update, context):
    if(mtype=="i"):
        context.bot.send_photo(chat_id=update.effective_chat.id, caption='Here\'s your photo!', photo=open("reddit/"+name+'.jpeg', 'rb'))
        os.remove("reddit/"+name+'.jpeg')
    elif(mtype=="v"):
        context.bot.send_video(chat_id=update.effective_chat.id, caption='Here\'s your video!', video=open("reddit"+name+'.mp4', 'rb'))
        os.remove("reddit"+name+'.mp4')
    elif(mtype=="g"):
        files = os.listdir("reddit/"+name)
        filecount = len(files)
        count=0
        while(count<filecount):
            context.bot.send_photo(chat_id=update.effective_chat.id, photo=open("reddit/"+name+"/"+name+(str(count+1))+".jpeg", 'rb'))
            os.remove("reddit/"+name+"/"+name+(str(count+1)+".jpeg"))
            count+=1
        context.bot.send_message(chat_id=update.effective_chat.id, text='Here\'s your gallery!')
        os.rmdir("reddit/"+name)
    os.rmdir("reddit/")