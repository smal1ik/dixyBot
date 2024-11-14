from aiogram.fsm.state import StatesGroup, State

class Admin(StatesGroup):
    ADMIN = State()
    POST = State()
    CHAT = State()
    TOKEN = State()
    TEMPERATURE = State()
    WORDS = State()
    PROMPT = State()
