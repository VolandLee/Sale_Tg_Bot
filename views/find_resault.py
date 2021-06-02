import requests
import sqlite3
from bs4 import BeautifulSoup
from multiprocessing import Pool
from multiprocessing import Process
import re
import functools

base_url = "https://www.wildberries.ru"


def get_html(url):
    r = requests.get(url)
    return r


def collect(html, shop, table):
    con = sqlite3.connect('{}.db'.format(shop))
    cur = con.cursor()

    soap = BeautifulSoup(html, "html.parser")

    products = soap.find('div', class_="catalog_main_table").find_all('a',
                                                                      class_="ref_goods_n_p j-open-full-product-card")
    resualt_search = soap.find('p', class_="searching-results-text")
    if resualt_search:
        return resualt_search.get_text()
    if not products:
        return "Введите полное название продукта"
    for product in products:

        shablon = []
        shablon.append('https://www.wildberries.ru' + product["href"])
        a = product.find('img', class_="thumbnail")
        shablon.append(a['alt'])
        if a['src'][-3:] == 'jpg':
            shablon.append(a['src'])
        else:
            shablon.append(a['data-original'])

        pr = product.find('span', class_="price").get_text()

        pr = re.sub("[-| |%|\xa0|\n]", "", pr).split('₽')
        if len(pr) == 2:
            pr = [int(pr[0]), 0, 0]
        else:
            pr = [int(el) for el in pr]
        shablon.extend(pr)

        cur.execute(
            "INSERT INTO `{}` (`id`, `title`, `image`, `new_price`, `old_price`, `sale`) VALUES(?, ?, ?, ?, ?, ?)".format(
                table), (shablon))
        con.commit()



def create_bd_with_cur_product(url, shop, table):
    try:
        con = sqlite3.connect('{}.db'.format(shop))
        cur = con.cursor()
        cur.execute(
            "CREATE TABLE `{}`(id TEXT PRIMARY KEY ON CONFLICT IGNORE, title TEXT, image TEXT, old_price INTEGER, sale INTEGER, new_price INTEGER);".format(
                table))
    except Exception:
        return 0
    else:

        with Pool(12) as p:
            p.map(functools.partial(manage, url, shop, table), [i for i in range(12)])


"""
['2\xa0433\xa03\xa0245\xa0-25\n\n']
"""


def manage(url, shop, table, l):
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


def search(text):
    url = base_url + '/catalog/0/search.aspx?search={}&xsearch=true'.format(text)
    print(url)
    return url


def create_catalog(catalog, html, shablon, url='', key=''):
    catalog.append({})

    soup = BeautifulSoup(html, "html.parser")
    items = soup.find("{}".format(shablon[0]), class_="{}".format(shablon[1])).find_all('a')

    for item in items:
        if key:
            if url + item['href'] != catalog[0]:
                catalog[1][item.img["alt"]] = [url + item['href']]
        else:
            if url + item['href'] != catalog[0]:
                catalog[1][item.get_text()] = [url + item['href']]


    return catalog


def proc1(catalog):
    for i in catalog[1]:

        html = get_html(*catalog[1][i])

        a = create_catalog(catalog[1][i], html.text, ["ul", 'sidemenu'], url=base_url)

        for l in a[1]:

            html = get_html(*a[1][l])
            create_catalog(a[1][l], html.text, ["ul", 'sidemenu'], url=base_url)
        print(catalog[1][i])







def proc():
    del_key = []
    catalog = ["https://www.wildberries.ru/brandlist/all"]

    html = get_html("https://www.wildberries.ru/brandlist/all")
    catalog = create_catalog(catalog, html.text, ['ul', 'brand-list__content'], url=base_url, key="1")

    proc1(catalog)
    print(catalog)















