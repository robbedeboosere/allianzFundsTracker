import requests
import bs4


class Fonds:
    headers = {
        'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 11_0_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.101 Safari/537.36',
        'content-type': 'application/json; charset=utf-8'}

    def __init__(self, shares, product, fund):
        self._shares = shares
        self._url = 'https://www.allianz.be/Life/PerformanceCalculation/UI/PerformanceCalculation/getChart?fund=' + str(
            fund) + '&product=' + str(product) + '&years=0'
        self._value = 0
        self.update_value()

    def get_request(self):
        for _ in range(5):
            try:
                response = requests.get(self._url, headers=self.headers, timeout=20)
                if response.status_code == 200:
                    return response
            except Exception as e:
                print(e)
                continue
        print('Error status code', response.status_code, response.text)

    def update_value(self):
        response = self.get_request()
        data = response.content
        page = bs4.BeautifulSoup(data, 'lxml')
        text = page.get_text()
        price = float(text.split('{')[-1].split('close')[1].split('}')[0][3:])
        self._value = price * self._shares

    def get_value(self):
        self.update_value()
        return self._value


class Portefeuille:
    def __init__(self):
        self._fondsen = list()
        self._value = 0

    def add_fonds(self, fonds):
        self._fondsen.append(fonds)

    def update_value(self):
        total = 0
        for fonds in self._fondsen:
            total += fonds.get_value()
        self._value = total

    def get_value(self):
        self.update_value()
        return self._value


if __name__ == "__main__":
    portefeuille = Portefeuille()
    markets = Fonds(4.764704, 4, 162)
    portefeuille.add_fonds(markets)
    avenir = Fonds(154.963896, 4, 30)
    portefeuille.add_fonds(avenir)
    equity = Fonds(209.623399, 4, 104)
    portefeuille.add_fonds(equity)
    neutral = Fonds(325.601821, 4, 105)
    portefeuille.add_fonds(neutral)
    balanced = Fonds(286.568249, 4, 106)
    portefeuille.add_fonds(balanced)
    immo = Fonds(65.754409, 4, 129)
    portefeuille.add_fonds(immo)
    print(portefeuille.get_value())
