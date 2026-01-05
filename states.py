from aiogram.fsm.state import StatesGroup, State


class TrackState(StatesGroup):
    waiting_track = State()


class HelpState(StatesGroup):
    waiting_question = State()


class AdminState(StatesGroup):
    waiting_password = State()
    reply_user = State()
