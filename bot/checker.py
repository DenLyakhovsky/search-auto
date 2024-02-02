import sqlite3
from scraper.scraper import scrappy_cards


# Перевірка цін, які були раніше
def check_the_price():
    with sqlite3.connect('auto.db') as con:
        cur = con.cursor()

        cur.execute('SELECT id, price, url FROM cars')

        existing_prices = []
        for id, price, url in cur.fetchall():
            existing_prices.append({
                'id': id,
                'url': url,
                'price': price,
            })

        scrapped_cars = scrappy_cards()

        changed_prices = {}
        for new_price in scrapped_cars:
            for existing_price in existing_prices:
                if existing_price.get('url') == new_price.get('url'):
                    if existing_price.get('price') != new_price.get('price'):
                        changed_prices[existing_price.get('id')] = new_price.get('price')

        for old_price_id, new_price in changed_prices.items():
            cur.execute("UPDATE cars SET price = ? WHERE id = ?", (new_price, old_price_id))

        if changed_prices:
            print("Products with changed prices:")
            for price_id, new_price in changed_prices.items():
                print(f"ID: {price_id}, New Price: {new_price}")
        else:
            print("No changes in prices.")

        return changed_prices


# Функція, яка виконує check_the_price й оновлює дані у БД
def check_the_id():
    check = check_the_price()
    with sqlite3.connect('auto.db') as con:
        cur = con.cursor()

        cur.execute('SELECT id FROM cars')

        existing_prices = [{'id': row[0]} for row in cur.fetchall()]

        cars = []
        if check:
            for check_item in check.keys():
                for db_item in existing_prices:
                    if db_item.get('id') == check_item:
                        cur.execute('SELECT * FROM cars WHERE id = ?', (db_item.get('id'),))

                        result = cur.fetchone()
                        cars.append(result)

    return cars


# Видалення із БД авто, які були продані
def delete_the_car():
    with sqlite3.connect('auto.db') as con:
        cur = con.cursor()

        cur.execute('SELECT id, title, url FROM cars')

        existing_prices = []
        for id, title, url in cur.fetchall():
            existing_prices.append({
                'id': id,
                'title': title,
                'url': url,
            })

        scrapped_cars = scrappy_cards()

        deleted_cars = []
        for item_from_db in existing_prices:
            url_from_db = item_from_db.get('url')

            if url_from_db is not None:
                found_in_scrapped = next(
                    (item_cars for item_cars in scrapped_cars if url_from_db in item_cars.get('url')), None)

                if found_in_scrapped is None:
                    deleted_cars.append({
                        'id': item_from_db.get('id'),
                        'title': item_from_db.get('title'),
                        'url': url_from_db,
                    })

        return deleted_cars


# Функція, для обробки нових постів
def newly_published_cars():
    with sqlite3.connect('auto.db') as con:
        cur = con.cursor()

        cur.execute('SELECT id, url FROM cars')

        existing_prices = []
        for id, url in cur.fetchall():
            existing_prices.append({
                'id': id,
                'url': url,
            })

        scrapped_cars = scrappy_cards()

        new_cars = []
        for item_cars in scrapped_cars:
            is_found = False
            for item_from_db in existing_prices:
                if item_from_db.get('url') is not None and item_from_db.get('url') == item_cars.get('url'):
                    is_found = True
                    break

            if not is_found:
                new_cars.append({
                    'title': item_cars.get('title'),
                    'price': item_cars.get('price'),
                    'url': item_cars.get('url'),
                    'imgs': item_cars.get('img'),
                })

        return new_cars
