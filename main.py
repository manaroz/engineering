try:
    import tkinter as tk
except:
    import Tkinter as tk
from bs4 import BeautifulSoup
from requests import get
import sqlite3
from sys import argv


def parse_price(price):
    return float(price.replace(' ', '').replace('zł', '').replace(',', '.'))


def parse_page(number):
    print(f'przetwarzam stronę numer {number}.')
    page = get(f'{URL}&page={number}')
    bs = BeautifulSoup(page.content, 'html.parser')
    for offer in bs.find_all('div', class_='offer-wrapper'):
        footer = offer.find('td', class_='bottom-cell')
        location = footer.find('small', class_='breadcrumb').get_text().strip()
        title = offer.find('strong').get_text().strip()
        price = parse_price(offer.find('p', class_='price').get_text().strip())

        print(title, price, location)

        cursor.execute('INSERT INTO offers VALUES (?, ?, ?)', (title, price, location))

    db.commit()

class App(tk.Frame):
    def __init__(self,master=None,**kw):
        tk.Frame.__init__(self,master=master,**kw)
        self.txtURL = tk.StringVar()
        self.entryURL = tk.Entry(self,textvariable=self.txtURL)
        self.entryURL.grid(row=0,column=0)
        self.btnGet = tk.Button(self,text="Szukaj smartfona!",command=self.getPhones)
        self.btnGet.grid(row=0,column=1)

    def getPhones(self):
        get_page(self.txtURL.get())


if __name__ == '__main__':
    root = tk.Tk()
    root.geometry('350x200')
    App(root).grid()
    root.mainloop()

URL = 'https://www.olx.pl/elektronika/telefony/smartfony-telefony-komorkowe/samsung/pomorskie/?search%5Bfilter_float_price%3Afrom%5D=10&search%5Bfilter_enum_state%5D%5B0%5D=new&page=1'
db = sqlite3.connect('phones.db')
cursor = db.cursor()

# python main.py setup  --->polecenie tworzące plik bazy danych dene.db

if len(argv) > 1 and argv[1] == 'setup':
    cursor.execute('''CREATE TABLE offers (name TEXT, price REAL, city TEXT)''')
    quit()

for page in range(1, 4):
    parse_page(page)

db.close()
