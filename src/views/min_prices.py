import os

import telebot
from matplotlib import pyplot as plt

from src.helpers import min_prices


async def send_min_prices_from_vvo_mow_to_hkt(message: telebot.types.Message, bot: telebot.TeleBot) -> None:

    await bot.reply_to(message, 'Запустил поиск, ожидайте...')

    lower = min_prices.from_vvo_mow_to_hkt()

    lowerVL, lowerMSC = lower[lower['city'] == 'vl'], lower[lower['city'] == 'msc']
    x1, y1 = lowerVL['depart_date'], lowerVL['price']
    x2, y2 = lowerMSC['depart_date'], lowerMSC['price']

    plt.figure(figsize=(10, 4))
    plt.plot(x1, y1, label="vl")
    plt.plot(x2, y2, label="msc")
    plt.xticks(rotation=45, ha='right')
    plt.legend()
    plt.grid(True)

    file_name = 'min_prices.jpg'
    try:
        plt.savefig(file_name)
        await bot.send_photo(message.chat.id, open('min_prices.jpg', 'rb'))
    finally:
        if os.path.exists(file_name):
            os.remove(file_name)