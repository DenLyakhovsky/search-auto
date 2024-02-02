import io
import sqlite3

from aiogram.filters import CommandStart
from aiogram import types
from aiogram import F
import time

from .app import router
from .app import bot

from .checker import delete_the_car, check_the_id, newly_published_cars
from models.base import save_to_db


# Стартовий хендлер
@router.message(CommandStart())
async def start_handler(message: types.Message):
    kb = [
        [
            types.KeyboardButton(text='Слідкувати'),
            types.KeyboardButton(text='Не слідкувати'),
        ]
    ]
    keyboard = types.ReplyKeyboardMarkup(
        keyboard=kb,
        resize_keyboard=True,
    )

    await message.answer(
        f'Привіт, {message.from_user.first_name}.\nЩоб почати слідкувати за Toyota Sequoia виберіть <b>"Слідкувати"</b>',
        parse_mode="HTML", reply_markup=keyboard, one_time_keyboard=True)


# Хендлер пошуку
@router.message(F.text.lower() == 'слідкувати')
async def search_handler(message: types.Message):
    await message.answer('Слідкую')

    while True:
        print('Перевіряю чи БД створена')
        save_to_db()

        print("Виконую newly_published_cars")
        newly_cars = newly_published_cars()

        print('Перевіряю є нові авто')
        if newly_cars:
            for new_car in newly_cars:
                print('Надсилаю дані користувачу про автомобіль')
                await message.answer("<b>Знайдений автомобіль</b>\n\n"
                                     f'<b>Заголовок</b>: <i>{new_car.get("title")}</i>\n'
                                     f'<b>Ціна</b>: $<i>{new_car.get("price")}</i>\n\n'
                                     f'<b>Посилання</b>: {new_car.get("url")}',
                                     parse_mode='HTML'
                                     )

                print("Зберігаю нові елементи у БД")
                with sqlite3.connect('auto.db') as con:
                    cur = con.cursor()

                    imgs = new_car.get('*imgs')

                    # Перевіряємо, чи imgs є списком з трьома елементами
                    if isinstance(imgs, list) and len(imgs) == 3:
                        # Розпаковуємо значення
                        img1, img2, img3 = imgs
                    else:
                        # Якщо щось пішло не так, ініціалізуємо всі три значення як None
                        img1, img2, img3 = None, None, None

                    data_values = (new_car.get("title"), new_car.get("price"), new_car.get("url"), img1, img2, img3)

                    cur.execute('INSERT INTO cars(title, price, url, image1, image2, image3) VALUES (?, ?, ?, ?, ?, ?)',
                                data_values)

        time.sleep(10)
        # Перевірка та видалення обʼєктів
        print("Виконую delete_the_car")
        check_the_car = delete_the_car()

        # Перевірка чи є елементи у check_the_car
        print('Перевіряю чи авто не було куплене')
        if check_the_car:
            for item_from_db in check_the_car:
                print('Надсилаю дані користувачу про автомобіль')
                await message.answer(f'<b>Викуп</b>\n\n'
                                     f'Автомобіль <b>{item_from_db.get("title")}</b> був куплений\n\n'
                                     f'Посилання: {item_from_db.get("url")}')

                # Підʼєднюємось до БД та видаляємо
                with sqlite3.connect('auto.db') as con:
                    print("Видаляю із БД")
                    cur = con.cursor()

                    cur.execute('DELETE FROM cars WHERE url = ?', (item_from_db.get('url'),))
        else:
            print('Куплених авто немає')

        time.sleep(10)
        # Перевірка цін
        print("Виконую check_the_id")
        cars_id = check_the_id()

        print('Надсилаю користувачу авто')
        if cars_id:
            for item in cars_id:
                await message.answer(f'<b>Змінена ціна</b>\n\n'
                                     f'<b>ID</b>: <i>{item[0]}</i>'
                                     f'<b>Заголовок</b>: <i>${item[1]}</i>\n'
                                     f'<b>Ціна</b>: <i>${item[2]}</i>\n\n'
                                     f'<b>Посилання</b>: <i>${item[3]}</i>',
                                     parse_mode='HTML')
                if item[4]:
                    print('Надсилаю фото')

                    # photo_stream = io.BytesIO(item[4])
                    # photo = types.InputFile(photo_stream)
                    # await bot.send_photo(chat_id=message.chat.id, photo=photo)

                else:
                    await message.reply("Image not found")
                    continue

        print('Завершив перевірку та надсилання')

        time.sleep(600)
        print('Починаю перевірку')


# Хендлер скасування пошуку
@router.message(F.text.lower() == 'не слідкувати')
async def search_cancel_handler(message: types.Message):
    await message.answer('Більше не слідкую\n\nЩоб почати слідкувати знову введіть <b>/start</b>', parse_mode='HTML')
