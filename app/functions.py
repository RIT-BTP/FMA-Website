from models import CurStockData
from app import db
import numpy as np
from urllib.request import urlopen
from bs4 import BeautifulSoup
from datetime import datetime
import pandas as pd
import pandas_datareader as pdr
from threading import Thread, Event
from app import app
from flask_socketio import SocketIO, emit
from time import sleep

thread = Thread()
thread_stop_event = Event()
socketio = SocketIO(app)


class StockThread(Thread):
    def __init__(self):
        self.delay = 5
        super(StockThread, self).__init__()

    def randomNumberGenerator(self):
        """
        Generate a random number every 1 second and emit to a socketio instance (broadcast)
        Ideally to be run in a separate thread?
        """
        stock = bsoption()
        while not thread_stop_event.isSet():
            socketio.emit(
                "newprice",
                {"SP500": stock.sp500, "DOW": stock.dow, "NASDAQ": stock.nasdaq},
                namespace="/stock-api",
            )
            sleep(self.delay)

    def run(self):
        self.randomNumberGenerator()


def random_color(arange=(0, 256)):
    color = list(np.random.choice(range(*arange), size=3))
    return color


def refresh_stock_data(stocks):
    for stock in stocks:
        print(stock)
        stock_name = stock.name
        exist = CurStockData.get(name=stock_name)
        data = bsoption(stock_name)
        data.i_scrap()
        if exist:
            exist = exist[0]
            exist.cost = data.cur_price
            exist.chg = data.d_chng
            exist.dividend = data.dividend
            exist.eps = data.eps
            exist.pe = data.pe
            exist.d_open = data.open
            exist.d_close = data.close
            db.session.commit()
        else:
            CurStockData.insert(
                name=stock_name,
                cost=data.cur_price,
                chg=data.d_chng,
                dividend=data.dividend,
                eps=data.eps,
                pe=data.pe,
                d_open=data.open,
                d_close=data.close,
            )


def construct_data():
    data = {
        labels: [],
        datasets: [
            {
                data: [],
                backgroundColor: [tuple(random_color().append(0.2)) for each in data],
                borderColor: [tuple(list(each)[:-1] + [1]) for each in backgroundColor],
            }
        ],
    }

    # data: {
    #     labels: ["Red", "Blue", "Yellow", "Green", "Purple", "Orange"],
    #     datasets: [
    #         {
    #             data: [12, 19, 3, 5, 2, 3],
    #             backgroundColor: [
    #                 "rgba(255, 99, 132, 0.2)",
    #                 "rgba(54, 162, 235, 0.2)",
    #                 "rgba(255, 206, 86, 0.2)",
    #                 "rgba(75, 192, 192, 0.2)",
    #                 "rgba(153, 102, 255, 0.2)",
    #                 "rgba(255, 159, 64, 0.2)",
    #             ],
    #             borderColor: [
    #                 "rgba(255, 99, 132, 1)",
    #                 "rgba(54, 162, 235, 1)",
    #                 "rgba(255, 206, 86, 1)",
    #                 "rgba(75, 192, 192, 1)",
    #                 "rgba(153, 102, 255, 1)",
    #                 "rgba(255, 159, 64, 1)",
    #             ],
    #             borderWidth: 1,
    #         }
    #     ],
    # }


class bsoption:
    def __init__(self, stock=None):
        if stock:
            self.url = f"https://finance.yahoo.com/quote/{stock}"
            html = urlopen(self.url)
            self.soup = BeautifulSoup(html, features="html5lib")
        else:
            self.url = "https://finance.yahoo.com/"
            html = urlopen(self.url)
            self.soup = BeautifulSoup(html, features="html5lib")
            self.index_scrap()

    def i_scrap(self):
        price_soup = (
            self.soup.find(id="quote-header-info").contents[2].contents[0].contents
        )
        self.cur_price = float(price_soup[0].text.replace(",", ""))
        self.d_chng = float(
            price_soup[1]
            .contents[0]
            .text[: price_soup[1].contents[0].text.find("(") - 1]
        )
        quote_soup = self.soup.find(id="quote-summary").contents
        if "." in quote_soup[1].contents[0].contents[0].contents[5].contents[1].text:
            print(quote_soup[1].contents[0].contents[0].contents[5].contents[1].text)
            self.dividend = float(
                quote_soup[1]
                .contents[0]
                .contents[0]
                .contents[5]
                .contents[1]
                .text[
                    : quote_soup[1]
                    .contents[0]
                    .contents[0]
                    .contents[5]
                    .contents[1]
                    .text.find("(")
                    - 1
                ]
            )
        else:
            self.dividend = None
        if "." in quote_soup[1].contents[0].contents[0].contents[3].contents[1].text:
            self.eps = float(
                quote_soup[1].contents[0].contents[0].contents[3].contents[1].text[:-1]
            )
        else:
            self.eps = None
        if "." in quote_soup[1].contents[0].contents[0].contents[2].contents[1].text:
            self.pe = float(
                quote_soup[1].contents[0].contents[0].contents[2].contents[1].text
            )
        else:
            self.pe = None
        self.close = float(
            quote_soup[0]
            .contents[0]
            .contents[0]
            .contents[0]
            .contents[1]
            .text.replace(",", "")
        )
        self.open = float(
            quote_soup[0]
            .contents[0]
            .contents[0]
            .contents[1]
            .contents[1]
            .text.replace(",", "")
        )

    def profile_scrap(self):
        html = urlopen(self.url + "/profile")
        profile_soup = BeautifulSoup(html, features="html5lib")
        pass

    def index_scrap(self):
        self.sp500 = (
            self.soup.find(id="market-summary")
            .contents[0]
            .contents[0]
            .contents[0]
            .contents[4]
            .text
        )
        self.dow = (
            self.soup.find(id="market-summary")
            .contents[0]
            .contents[1]
            .contents[0]
            .contents[4]
            .text
        )
        self.nasdaq = (
            self.soup.find(id="market-summary")
            .contents[0]
            .contents[2]
            .contents[0]
            .contents[4]
            .text
        )

    def test(self):
        df = pdr.get_data_yahoo("aapl", datetime(2018, 1, 1), datetime.now())
        print(df)

    def history(self, start, end=None):
        if not end:
            end = datetime.now()
        html = urlopen(
            self.url
            + f"/history?period1={int(datetime.timestamp(start))}&period2={int(datetime.timestamp(end))}&interval=1d&filter=history&frequency=1d"
        )
        print(
            self.url
            + f"/history?period1={int(datetime.timestamp(start))}&period2={int(datetime.timestamp(end))}&interval=1d&filter=history&frequency=1d"
        )
        soup = BeautifulSoup(html, features="html5lib")
        main = soup.find(id="Col1-3-HistoricalDataTable-Proxy")
        head = main.contents[0].contents[1].contents[0].contents[0].contents[0].contents
        body = main.contents[0].contents[1].contents[0].contents[1]
        data = {h.text: [] for h in head}
        for row in body:
            if len(row.contents) != 2:
                for i, d in enumerate(row.contents):
                    data[list(data.keys())[i]].append(d.text)
        df = pd.DataFrame(data)
        print(df)

    def __repr__(self):
        return "Current Price: {},\nDaily Change: {},\nDividend: {},\nEPS {},\nPE Ratio: {},\nClosed: {},\nOpen: {}".format(
            self.cur_price,
            self.d_chng,
            self.dividend,
            self.eps,
            self.pe,
            self.close,
            self.open,
        )


class apioption:
    def __init__(stock):
        pass


if __name__ == "__main__":
    bs = bsoption()
    print(bs.dow)
    # bs.test()
    # bs.history(datetime(2018,1,1))
    # bs.i_scrap()
    # print(bs)
