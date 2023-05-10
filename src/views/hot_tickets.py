import re

import telebot
from src.config import Config
from src import api


def get_name(code: str) -> str:
    NAME_BY_CODE = {
        'VVO': 'Владивосток',
        'MOW': 'Москва'
    }
    return NAME_BY_CODE.get(code) or code


async def send_hot_tickets(message: telebot.types.Message, bot: telebot.TeleBot) -> None:

    result_found = re.findall(r'/hotTickets (\w+)', message.text)
    if not result_found:
        await bot.reply_to(
            message, 
            'Необходимо указать пункт отправления, примеры:\n "/hotTickets MOW" из Москвы или "/hotTickets VVO" - из Владивостока.'
        )
        return

    await bot.reply_to(message, 'Запустил поиск, ожидайте...')
    from_original = result_found[0]

    try:
        hot_ticket_offers = api.get_russian_hot_ticket_offers(from_=from_original)
    except api.exceptions.TicketCodeError:
        await bot.reply_to(message, f'Нет города отправления с кодом {from_original}.')
        return

    response_text = ' \n\n'.join([
        (
            f"""<b>{get_name(from_original)} > {offer['destination_name'] or offer['destination']} за {offer['value']} р. <s>{offer['old_value']} р.</s></b>"""
            f"""\nПериод вылета/прибытия: {offer['local_depart_date'].strftime('%Y-%m-%d %H:%M')} - {offer['local_arrival_date'].strftime('%Y-%m-%d %H:%M')}."""
            f"""<a href="{Config.PUBLIC_DOMAIN_AVIASALES + '/search' + offer['ticket_link']}">Подробнее</a>"""
        )
        for offer in hot_ticket_offers
    ]) if hot_ticket_offers else f'Нет горячих билетов из {get_name(from_original)}.'

    await bot.send_message(message.chat.id, response_text, parse_mode="HTML")