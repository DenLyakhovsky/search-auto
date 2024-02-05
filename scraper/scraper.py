import requests
from bs4 import BeautifulSoup
from PIL import Image
from io import BytesIO


# Функція, для збереження та перетворення фото у байти
def convert_to_png(img_url):
    blobs = []

    n = 1
    for url in img_url:
        image_data = requests.get(url)

        image = Image.open(BytesIO(image_data.content))

        blob_image = BytesIO()
        image.save(blob_image, "PNG")
        n += 1

        blobs.append(blob_image.getvalue())

    return blobs


# Функція, для видалення непотрібних символів
def remove_symbols(text):
    dd = " '"
    for i in text:
        if i in dd:
            new_text = text.replace(i, "")
            return new_text


datas_from_card = []


# Парсинг автомобілів
def scrappy_cards():
    url_auto = "https://auto.ria.com/uk/search/?indexName=auto,order_auto,newauto_search&categories.main.id=1&brand.id[0]=79&model.id[0]=2104&country.import.usa.not=0&price.currency=1&abroad.not=0&custom.not=-1&page=0&size=30"

    r = requests.get(url_auto).text
    soup = BeautifulSoup(r, 'lxml')

    num = 1
    all_cards = soup.find(id='searchResults').find_all('section')
    for element in all_cards:
        try:
            title = element.find(class_='content').find('a').text.strip()
            price = element.find(class_='content').find(class_='size15').find_all('span')[0].text.strip()  # with $

            urls = element.find(class_='address').get('href')

            datas_from_card.append({
                'title': title,
                'price': int(remove_symbols(price)),
                'url': urls,
            })

            print(f'Виконано: {num}')
            num += 1

            if num == 5:
                break

        except AttributeError:
            continue

    return datas_from_card
