import os
from dotenv import load_dotenv

load_dotenv()

MAIL_SERVER = os.environ.get('MAIL_SERVER', 'smtp.gmail.com')
MAIL_PORT = int(os.environ.get('MAIL_PORT', 587))
MAIL_USE_TLS = os.environ.get('MAIL_USE_TLS', 'True').lower() == 'true'
MAIL_USERNAME = os.environ.get('MAIL_USERNAME')
MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD')
MAIL_DEFAULT_SENDER = os.environ.get('MAIL_DEFAULT_SENDER', MAIL_USERNAME)
ADMIN_EMAIL = os.environ.get('ADMIN_EMAIL', MAIL_USERNAME)

# WhatsApp number (with country code, no "+") that click-to-WhatsApp buttons message
ADMIN_WHATSAPP = os.environ.get('ADMIN_WHATSAPP', '917893834715')
