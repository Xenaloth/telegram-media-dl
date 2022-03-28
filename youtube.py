import os,json,random,yt_dlp
num = 0

def downloadVideo(url):
    num = random.randrange(10000,99999)
    os.system("./yt-dlp --sponsorblock-mark all --sub-format best --sub-langs en.* --embed-subs  --embed-thumbnail -f 'bv+ba/b' -o "+str(num)+" --merge-output-format mkv "+url)
    return str(num)+'.mkv'