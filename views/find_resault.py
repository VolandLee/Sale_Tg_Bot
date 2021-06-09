import requests
import sqlite3
from bs4 import BeautifulSoup
from multiprocessing import Pool
from multiprocessing import Process
import re
import functools
import time
from multiprocessing import cpu_count
BASE_URL = "https://www.wildberries.ru"
HEADERS = {'user-agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.72 YaBrowser/21.5.1.330 Yowser/2.5 Safari/537.36",
               'accept': "*/*"}

def get_html(url, params=None):


    r = requests.get(url, headers=HEADERS, params=params)
    return r


def collect(html, shop, table):
    if shop == "Lamoda":
        key = ['products-catalog__list', 'a', 'products-list-item__link link', 'https://www.lamoda.ru', 'products-list-item__img']
    else:
        key = ['catalog_main_table', 'a', 'ref_goods_n_p j-open-full-product-card', 'https://www.wildberries.ru', 'thumbnail']

    """Collects data on the product.
     Arguments: HTML page with goods, shop, table contains the result of a search in the form of a string for example:
     'Sneakers for children'.
     The function creates a template in which the data enters the received and adds them to the database"""
    con = sqlite3.connect('{}.db'.format(shop))
    cur = con.cursor()

    soap = BeautifulSoup(html, "html.parser")

    products = soap.find('div', class_="{}".format(key[0])).find_all("{}".format(key[1]), class_="{}".format(key[2]))

    if shop != "Lamoda":
        resualt_search = soap.find('p', class_="searching-results-text")
        if resualt_search:
            return resualt_search.get_text()
        if not products:
            return "Введите полное название продукта"

    for product in products:
        shablon = []
        shablon.append('{}'.format(key[3]) + product["href"])
        a = product.find('img', class_="{}".format(key[4]))
        shablon.append(a['alt'])
        if shop == "Lamoda":
            shablon.append (a['src'])
        elif a['src'][-3:] != 'jpg':
            shablon.append(a['data-original'])
        else:
            shablon.append(a['src'])
        if shop == "Lamoda":
            try:
                a = product.find('span', class_='price__actual parts__price_cd-disabled').get_text()
            except Exception:
                price = product.find('span', class_='price').get_text ()
                price = price.replace(" ", "")
                price = int(price[:-1])
                shablon.extend([price, 0, 0])
            else:
                price = product.find('span', class_='price').get_text ()
                price = price.replace(" ", "")
                a = (len(price) - 1) // 2
                new_price = int(price[-a-1:-1])
                old_price = int(price[0:-a-1])
                sale = int((new_price / old_price) * 100)
                shablon.extend([new_price, old_price, 100 - sale])
        else:

            pr = product.find ('span', class_="price").get_text ()

            pr = re.sub ("[-| |%|\xa0|\n]", "", pr).split ('₽')
            if len (pr) == 2:
                pr = [int (pr[0]), 0, 0]
            else:
                pr = [int (el) for el in pr]
            shablon.extend(pr)

        cur.execute (
            "INSERT INTO `{}` (`id`, `title`, `image`, `new_price`, `old_price`, `sale`) VALUES(?, ?, ?, ?, ?, ?)".format (
                table), (shablon))
        con.commit ()



def create_bd_with_cur_product(url, shop, table):
    """Creates a table in the database and parallel to the manage function
     If the user pressed the search, the table will be created in the database 'Shop' otherwise in the selected store """
    try:
        con = sqlite3.connect('{}.db'.format(shop))
        cur = con.cursor()
        cur.execute(
            "CREATE TABLE `{}`(id TEXT PRIMARY KEY ON CONFLICT IGNORE, title TEXT, image TEXT, old_price INTEGER, sale INTEGER, new_price INTEGER);".format(
                table))
    except Exception:
        return 0
    else:
        proc_num = cpu_count()
        with Pool(proc_num) as p:
            p.map(functools.partial(manage, url, shop, table), [i for i in range(12)])


"""
['2\xa0433\xa03\xa0245\xa0-25\n\n']
"""


def manage(url, shop, table, l):
    """Builds the URL address of the page and transmits it with HTML text
     Argument L This is a parallel process number that starts the CREATE_BD_WITH_CUR_PRODUCT function """
    for i in range(1, 5):
        shablon = url + '?sort=popular&page={}'.format(l * i)
        print(shablon)
        html = get_html(shablon)

        if html.status_code == 200:
            try:
                collect(html.text, shop, table)
            except Exception:
                pass
        else:
            break


"""

if __name__ == '__main__':

    with Pool(12) as p:

        p.map(manage, [i for i in range(12)])


    proc()    
"""


def search(shop, text):
    """Запускается если пользователь нажал поиск и строит url"""
    BASE_URL = {"Wildberries": "https://www.wildberries.ru/catalog/0/search.aspx?search=", "Lamoda": "https://www.lamoda.ru/catalogsearch/result/?q="}
    url = BASE_URL[shop]+text+"&"

    print(url)
    return url


def create_catalog(catalog, html, shablon, url='', key=''):

    catalog.append({})

    soup = BeautifulSoup(html, "html.parser")
    try:
        items = soup.find("{}".format(shablon[0]), class_="{}".format(shablon[1])).find_all('a')
    except Exception:
        return

    for item in items:

        if item['data-level'] != '2':
            catalog[1][item.get_text()] = [url + item['href'], {}]
            key = item.get_text()
        else:
            catalog[1][key][1][item.get_text()] = [url + item['href']]





    return catalog


def proc1(catalog):
    for i in catalog[1]:

        html = get_html(*catalog[1][i])

        a = create_catalog(catalog[1][i], html.text, ["ul", 'sidemenu'], url=BASE_URL)

        for l in a[1]:

            html = get_html(*a[1][l])
            create_catalog(a[1][l], html.text, ["ul", 'sidemenu'], url=BASE_URL)
        print(catalog[1][i])




base = {'Женщинам': "https://www.lamoda.ru/c/4153/default-women/", 'Мужчинам' : "https://www.lamoda.ru/c/4152/default-men/", 'Детям' : "https://www.lamoda.ru/c/4154/default-kids/"}


def proc():
    """You can use manually to update the store catalog """
    del_key = []
    catalog = ["https://www.wildberries.ru/brandlist/all"]

    html = get_html("https://www.wildberries.ru/brandlist/all")
    catalog = create_catalog(catalog, html.text, ['ul', 'brand-list__content'], url=BASE_URL, key="1")

    proc1(catalog)
    print(catalog)


def create_cat():
    for i in base:
        lamoda = ["https://www.lamoda.ru/women-home/"]
        html = get_html(base[i])
        catalog = create_catalog(lamoda, html.text, ['ul', 'cat-nav dt102_1'], url='https://www.lamoda.ru/')

        for l in catalog[1]:
            for m in catalog[1][l][1]:

                html = get_html(catalog[1][l][1][m][0])
                create_catalog(catalog[1][l][1][m], html.text, ['ul', 'cat-nav cat-nav-sub dt102_3'], url='https://www.lamoda.ru/')
        base[i] = catalog
        print(base)
















