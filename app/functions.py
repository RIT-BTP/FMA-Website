# from models import Stocks
import numpy as np
from urllib.request import urlopen
from bs4 import BeautifulSoup
from datetime import datetime
import pandas as pd
import pandas_datareader as pdr


def random_color(arange=(0, 256)):
    color = list(np.random.choice(range(*arange), size=3))
    return color


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
    def __init__(self, stock):
        self.url = f"https://finance.yahoo.com/quote/{stock}"
        html = urlopen(self.url)
        self.soup = BeautifulSoup(html, features="html5lib")

    def i_scrap(self):
        price_soup = (
            self.soup.find(id="quote-header-info").contents[2].contents[0].contents
        )
        self.cur_price = price_soup[0].text
        self.d_chng = price_soup[1].contents[0].text
        quote_soup = self.soup.find(id="quote-summary").contents
        self.dividend = (
            quote_soup[1].contents[0].contents[0].contents[5].contents[1].text
        )
        self.eps = quote_soup[1].contents[0].contents[0].contents[3].contents[1].text
        self.pe = quote_soup[1].contents[0].contents[0].contents[2].contents[1].text
        self.close = quote_soup[0].contents[0].contents[0].contents[0].contents[1].text
        self.open = quote_soup[0].contents[0].contents[0].contents[1].contents[1].text

    def profile_scrap(self):
        html = urlopen(self.url + "/profile")
        profile_soup = BeautifulSoup(html, features="html5lib")
        pass

    def test(self):
        df = pdr.get_data_yahoo("aapl", datetime(2018,1,1), datetime.now())
        print(df)

    def history(self, start, end=None):
        if not end:
            end = datetime.now()
        html = urlopen(self.url + f"/history?period1={int(datetime.timestamp(start))}&period2={int(datetime.timestamp(end))}&interval=1d&filter=history&frequency=1d")
        print(self.url + f"/history?period1={int(datetime.timestamp(start))}&period2={int(datetime.timestamp(end))}&interval=1d&filter=history&frequency=1d")
        soup = BeautifulSoup(html, features="html5lib")
        main = soup.find(id="Col1-3-HistoricalDataTable-Proxy")
        head = main.contents[0].contents[1].contents[0].contents[0].contents[0].contents
        body = main.contents[0].contents[1].contents[0].contents[1]
        data = {h.text:[] for h in head}
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
    bs = bsoption("aapl")
    bs.test()
    # bs.history(datetime(2018,1,1))
    # bs.i_scrap()
    # print(bs)
