import sqlite3

def choose(shop, table):
    """Получает данные с бд и сортирует их"""
    con = sqlite3.connect('{}.db'.format(shop))
    cur = con.cursor()
    ans = cur.execute("SELECT * FROM `{}` ORDER BY sale DESC".format(table)).fetchmany(3)
    res = []
    for el in ans:

        print(el)
        if el[-1] == 0:
            el = '{}, цена {} {}'.format(el[1], el[-3], el[0])

        else:
            el = '{}, новая цена {} старая цена {} скидка {}%! {}'.format(el[1], el[-1], el[-3], el[-2], el[0])
        res.append(el)
    return res







