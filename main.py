import telebot
from flask import Flask, request

import config
from config import API_TOKEN


bot = telebot.TeleBot(API_TOKEN, threaded=False)
app = Flask(__name__)


@app.route("/index")
def index():
	return "<h1>Flask app</h1>"

@app.route(f"/{API_TOKEN}", methods=["POST"])
def get_message():
	bot.process_new_updates([telebot.types.Update.de_json(request.stream.read().decode("utf-8"))])
	return "!", 200

@app.route("/")
def webhook():
	bot.remove_webhook()
	bot.set_webhook(url=config.WEBHOOK_URL)
	return "!", 200

@bot.message_handler(commands=["start"])
def start_command(msg):
	bot.send_message(msg.chat.id, "Привет, я бот")

@bot.message_handler(commands=["help"])
def help_command(msg):
	bot.send_message(msg.chat.id, "Помощь")

@bot.message_handler()
def default_handler(msg):
	bot.send_message(msg.chat.id, "Не понимаю, посмотри /help")


if __name__ == "__main__":
	app.run(host=config.WEBAPP_HOST, port=config.WEBAPP_PORT)