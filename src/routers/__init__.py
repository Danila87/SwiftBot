from routers.commands.router import commands_router
from routers.events.router import events_router
from routers.messages.router import messages_router
from routers.admin_commands.router import admin_commands_router

__all__ = [
    "commands_router",
    "events_router",
    "messages_router",
    "admin_commands_router",
]