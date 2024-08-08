from aiogram.dispatcher.filters.state import State, StatesGroup


class QuestionsState(StatesGroup):
    first_question = State()
    reason = State()
    questions = State()
