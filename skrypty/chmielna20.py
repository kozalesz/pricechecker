from bs4 import BeautifulSoup
import requests
import csv

def chmielna20(url):
    source = requests.get(url).text
    soup = BeautifulSoup(source, 'lxml')

    try:
        error = soup.find('div', class_='text-site').h1.text
        if error is not '':
            return None
    except:
        pass

    product = soup.find('div', {'id': 'product'})
    product_name = product.find('div', class_='product__name').h1.text
    product_number = str(product_name.strip(')'))[
                     product_name.rfind("(") + 1:product_name.rfind(")")]
    product_name = str(product_name[:product_name.rfind('(')]).strip()
    product_price = product.find('div', class_='product__price')
    actually_price = product_price.find('span',
                                        class_='product__price_shop').text.strip(
        'PLN')
    original_price = product_price.find('span', class_='product__price_producent')
    if original_price is not None:
        original_price = original_price.text.strip('PLN')
    else:
        original_price = actually_price
    sizes = product.find('div', class_='selector')
    avaliable_sizes = []
    for size in sizes.find_all('li'):
        a_size = size.get('data-value')
        avaliable_sizes.append(a_size)

    try:
        if product_number not in s:
            with open('Chmielna - lista.csv', 'a', encoding='utf-8') as csvfile:
                csvwriter = csv.writer(csvfile)
                csvwriter.writerow([product_number, product_name, original_price, actually_price])
                print('Zapisano!')
        else:
            print("Już jest!")
    except:
        print("Nie udało się zapisać...")

    # print(product_name)
    # print(product_number)
    # print(original_price)
    # print(actually_price)
    # print(avaliable_sizes)

chmielna20('https://chmielna20.pl/menu/obuwie/page,1')

def get_all_links(s, url='https://chmielna20.pl/menu/obuwie/page,500'):
    source = requests.get(url).text
    soup = BeautifulSoup(source, 'lxml')
    for product in soup.find_all('div', class_='col-sm-4 col-md-3 col-xs-6 products__item'):
        product_url = product.p.a.get('href')
        print("Sprawdzam link: {}".format(product_url))
        chmielna20(product_url, s)
        print()
with open('Chmielna - lista.csv', 'r') as fp:
    s = fp.read()
get_all_links(s)