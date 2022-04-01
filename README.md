# telegram-instagram-dl
This project uses instagrapi and python-telegram-bot to download posts from public Instagram accounts!

To get started, you will need to run 'pip install -r requirements.txt'. Then, you will need to enter a username and password, along with your telegram bot token from botfather, into the creds.json file.
Once you have that, simply run 'python3 app.py' to run!

Current features:
- [x] Download images, videos, reels, and galleries from public accounts
- [x] Download stories and highlights from public accounts
- [x] Download posts from private accounts
- [x] Download TikTok posts (without watermarks!)
- [x] Download YouTube videos (with sponsorblock segments marked) (limited to 50mb uploads unless you use a [custom api server](https://github.com/tdlib/telegram-bot-api))
