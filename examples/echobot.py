import silbot
from silbot.helper import *

token = "12345:abcdefghi" # Put bot token here
bot = silbot.botapi.botApi(token)

r,response = bot.getMe()
print(response.expected_object.__module__)
if response.ok == False:
  print("Error, wrong bot Token")
  exit()
else:
  print("Bot @" + r.username + " started")


def updateH (update: silbot.types.Update,bot: silbot.botapi.botApi):
    """
    You should edit this function to set bot commands
    """
    if hasattr(update,"message"):
        message = update.message
        chat = message.chat
        bot.sendMessage(chat.id,message.text)

silbot.startpool(bot,updateH)
    