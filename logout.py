from telegram import Bot
import json
creds = open('creds.json',)
creds = json.load(creds)
Bot(token=creds["telegram_token"]).log_out()