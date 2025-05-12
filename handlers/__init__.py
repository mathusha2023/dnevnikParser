from aiogram import Router
from .default_handlers import router as default_router
from .auth_handlers import router as auth_router
from .all_marks_handlers import router as all_marks_router

main_router = Router()
main_router.include_router(auth_router)
main_router.include_router(all_marks_router)
main_router.include_router(default_router)
