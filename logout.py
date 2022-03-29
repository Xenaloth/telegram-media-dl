from telegram import Bot
import json
creds = open('creds.json',)
creds = json.load(creds)
bot = Bot(token=creds["telegram_token"], base_url=creds["api_url"])
bot.delete_webhook()
bot.close()
bot.log_out()