from aiogram.fsm.state import State, StatesGroup


class LoginStates(StatesGroup):
    enter_login = State()
    enter_password = State()
    enter_code = State()

