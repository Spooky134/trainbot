import requests
from bs4 import BeautifulSoup

HEADERS = {'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko)'
                         ' Chrome/104.0.0.0 Safari/537.36',
           'accept': '*/*'}


class Train:
    def __init__(self, date=None, number=None, train_route=None, train_type=None, city_from=None, city_to=None,
                 departure=None, arrival=None, travel_time=None, places=None, link=None):
        self.date = date
        self.number = number
        self.train_route = train_route
        self.train_type = train_type
        self.city_from = city_from
        self.city_to = city_to
        self.departure = departure
        self.arrival = arrival
        self.travel_time = travel_time
        self.places = places
        self.link = link

    def get_place_info(self, place_type):
        return place_type + self.places[place_type]

    def get_all_place_info(self):
        items = []
        for key in self.places:
            items.append(self.get_place_info(key))
        return items

    def get_text(self):
        string = f'{self.number}\n{self.train_type}\n{self.city_from}\n{self.city_to}\n{self.departure}\n' \
                 f'{self.arrival}\n{self.travel_time}'
        return string


def get_html(url, params=None):
    r = requests.get(url, headers=HEADERS, params=params)
    return r


def get_content(html):
    soup = BeautifulSoup(html, 'html.parser')
    items = soup.find_all('div', class_='sch-table__row-wrap')
    date = soup.find('div', class_='sch-title__date h3').get_text()

    trains = []
    for i, item in enumerate(items):
        places = []
        all_price_type = item.find_all('div', class_='sch-table__t-item has-quant')
        for el in all_price_type:
            typ = el.find('div', class_='sch-table__t-name').get_text()
            amount = el.find('span').get_text()
            cost = el.find('span', 'ticket-cost').get_text()
            places.append((typ, amount, cost))

        if len(places) == 0:
            places.append(('Мест нет', '', ''))

        print(f'trains number {i}\n{places}\n{len(all_price_type)}\n')

        trains.append(Train(date=date,
                            number=item.find('span', class_='train-number').get_text(),
                            train_route=item.find('span', class_='train-route').get_text(),
                            train_type=item.find('span', class_='sch-table__route-type').get_text(),
                            city_from=item.find('div', class_='sch-table__station train-from-name').get_text(),
                            city_to=item.find('div', class_='sch-table__station train-to-name').get_text(),
                            departure=item.find('div', class_='sch-table__time train-from-time').get_text(),
                            arrival=''.join(item.find('div', class_='sch-table__time train-to-time').get_text()
                                            .split()),
                            travel_time=item.find('div', class_='sch-table__duration train-duration-time').get_text(),
                            places=places,
                            link='https://pass.rw.by'+item.find('a', class_='sch-table__route').get('href'),))
    return trains


def parse(url):
    html = get_html(url)
    if html.status_code == 200:
        return get_content(html.text)
    else:
        return 'error' + str(html.status_code)


def trains_route_url(city_from, city_to, date):
    url = f'https://pass.rw.by/ru/route/?from={city_from}&from_esr=&from_exp=&to={city_to}&to_esr=&to_exp=&date={date}'
    return url


def get_trains_info(city_from, city_to, date):
    url = trains_route_url(city_from, city_to, date)
    trains = parse(url)
    return trains, url


if __name__ == '__main__':
    pass
