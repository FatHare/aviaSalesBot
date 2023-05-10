import os

from dotenv import load_dotenv

load_dotenv()

class Config:
    BOT_TOKEN = os.environ['BOT_TOKEN']
    PUBLIC_DOMAIN_AVIASALES = os.environ['PUBLIC_DOMAIN_AVIASALES']