from aiogram import Bot, Dispatcher, Router

TOKEN_APP = '6531168502:AAHcdmVOWNXiBp_7_oWsJwTdyMUgzYeSkP8'
router = Router()
bot = Bot(TOKEN_APP, parse_mode="HTML")


async def main() -> None:
    dp = Dispatcher()
    dp.include_router(router)

    bot = Bot(TOKEN_APP, parse_mode="HTML")
    await dp.start_polling(bot)
