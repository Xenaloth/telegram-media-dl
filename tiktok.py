import requests,os,json,random
def getIdFromURL(url):
    head, sep, tail = url.partition('?')
    url = head.split('/')
    return url[5]
def downloadVideo(videoId):
    url = 'http://api2.musical.ly/aweme/v1/aweme/detail/?aweme_id='+videoId
    res = requests.get(
        url,
        headers = {
            'User-Agent' : 'okhttp',
        }
    )
    data = res.json()
    num = random.randrange(10000,99999)
    # I hate all of this
    url2 = data['aweme_detail']['video']['play_addr']['url_list'][0]
    res2 = requests.get(
        url2,
        headers = {
            'User-Agent' : 'okhttp',
        }
    )
    with open("./"+str(num)+".mp4", 'wb') as out:
        out.write(res2.content)
    return str(num)+".mp4"