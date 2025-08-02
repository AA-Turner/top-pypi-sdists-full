from aiogram.fsm.state import StatesGroup, State


class HelloWorldClientStates(StatesGroup):
    input_text = State()
