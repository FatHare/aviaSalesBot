import telebot
from telebot.async_telebot import AsyncTeleBot

from src.config import Config
from src import views

bot = AsyncTeleBot(Config.BOT_TOKEN)

bot.register_message_handler(views.send_hot_tickets, commands=['hotTickets'], pass_bot=True)
bot.register_message_handler(views.send_min_prices_from_vvo_mow_to_hkt, commands=['minPrices'], pass_bot=True)

@bot.message_handler(commands=['help', 'start'])
async def send_start(message: telebot.types.Message):
    await bot.reply_to(message, '/minPrices - картинка с мин. ценами в разрезе дат.\n/hotTickets VVO - горячие билеты из Владивостока')
