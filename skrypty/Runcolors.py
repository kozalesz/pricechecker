from bs4 import BeautifulSoup
from database import make_connection, close_connection, send_data
import requests
from time import sleep
from datetime import datetime

def find_number_of_pages(url):
    source = requests.get(url).text
    source = BeautifulSoup(source, 'lxml')
    number_of_pages = source.find('div', {'class': 'navigation'})
    number_of_pages = number_of_pages.find_all('a', class_='')
    number_of_pages = int(number_of_pages[-1].text)
    print("Pobrana liczba stron to: {}".format(number_of_pages))
    return number_of_pages

def get_all_links(number_of_pages):
    list_of_links = []
    for index in range(1, number_of_pages+1):
        url = "https://runcolors.pl/sneakers/plec/meskie.html?page={}".format(index)
        print("Pobieram linki z: {}".format(url))
        list_of_links += get_all_links_from_one_page(url)
    return list_of_links

def get_all_links_from_one_page(url):
    source = requests.get(url).text
    source = BeautifulSoup(source, 'lxml')
    list_of_links = []
    for shoe in source.find_all('a', {'class': 'pList__item__link'}):
        shoe = shoe.get('href')
        list_of_links.append(shoe)
    return list_of_links

def collecting_data(list_of_links):

    cnx, cursor = make_connection()

    for link in list_of_links:
        url = "https://runcolors.pl{}".format(link)
        print("Pracuję nad: {}".format(url))
        source = requests.get(url).text
        source = BeautifulSoup(source, 'lxml')

        product = source.find('div', {'class': 'product'})

        brand = product.find_all('span', {'class': 'product__data__content'})[1].text
        product_number = product.find('span', {'class': 'product__data__content'}).text
        product_name = product.find(class_='product__header__name').text
        product_name = product_name.replace(brand, '').strip().rstrip()
        price_regular = product.find('p', class_='product__data__price__regular').text.split()[0]
        url_jpg = product.find('a', class_='js--swiper-zoom').get('href')

        try:
            price_now = product.find('p', class_='product__data__price__list').text.split()[0]
            price_now, price_regular = price_regular, price_now
        except AttributeError:
            price_now = price_regular

        price_now = float(price_now.replace(',', '.'))
        price_regular = float(price_regular.replace(',', '.'))
        steal = 100-(price_now/price_regular)*100

        sql = (brand, product_number, product_name, price_regular, price_now, url, url_jpg, steal)
        send_data(cnx, cursor, sql)

    close_connection(cnx, cursor)


if __name__ == '__main__':
    while True:
        number_of_pages = find_number_of_pages(r"https://runcolors.pl/sneakers/plec/meskie.html")
        list_of_links = []
        list_of_links += get_all_links(number_of_pages)
        collecting_data(list_of_links)
        print("Idę spać: {}".format(datetime.now().time()))
        sleep(1800)
