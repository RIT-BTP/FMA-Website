from models import Stocks
import numpy as np
from urllib.request import urlopen
from bs4 import BeautifulSoup


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

class bsoption():

    def __init__(stock):
        url = f'https://finance.yahoo.com/quote/{stock}'
        html  = urlopen(url)
        self.soup = BeautifulSoup(html)

class apioption():

    def __init__(stock):
        pass

if __name__ == "__main__":
    bs = bsoption("AAPL")
