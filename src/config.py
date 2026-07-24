import os

from dotenv import load_dotenv
from aiogram.types.chat_permissions import ChatPermissions

load_dotenv(dotenv_path='../.env')

BOT_TOKEN = os.getenv('BOT_TOKEN')

ACCESS_USER_PERMISSIONS = ChatPermissions(
    can_send_messages=True,
    can_send_media_messages=True,
    can_send_other_messages=True,
    can_send_audios=True,
    can_send_photos=True,
    can_send_videos=True,
    can_send_documents=True,
    can_send_polls=True,
    can_set_channels=True,
    can_send_video_notes=True,
    can_send_voice_notes=True,
)

NOT_ACCESS_USER_PERMISSIONS  = ChatPermissions(
    can_send_messages=False,
    can_send_media_messages=False,
    can_send_other_messages=False,
    can_send_audios=False,
    can_send_photos=False,
    can_send_videos=False,
    can_send_documents=False,
    can_send_polls=False,
    can_set_channels=False,
    can_send_video_notes=False,
    can_send_voice_notes=False,
)

TG_GROUP_ID = os.getenv('TG_GROUP_ID')
TG_TRADE_GROUP_ID = os.getenv('TG_TRADE_GROUP_ID')
SHEET_ID = os.getenv('SHEET_ID')

ADMIN_USERS = os.getenv('ADMIN_USERS')
if ADMIN_USERS:
    ADMIN_USERS = map(int, ADMIN_USERS.replace(" ", "").split(','))