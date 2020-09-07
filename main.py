import requests
import json
import subprocess as s
from os import getenv

from time import sleep
from datetime import datetime
from lxml.html import fromstring
from utils import load_json_products, bcolors
from crawler_factory import CrawlerFactory
from components.AWS_utils import S3

_DICT_XPATH = {
    'americanas': './/span[contains(@class, "price__SalesPrice")]',
    'acer.com': './/strong[contains(@class, "skuBestPrice")]',
    'submarino': './/span[contains(@class, "sales-price")]'
}


# def get_xpath_from_dict(link):
#     if 'americanas' in link:
#         return 'americanas', _DICT_XPATH['americanas']
#     elif 'acer.com' in link:
#         return 'acer.com', _DICT_XPATH['acer.com']
#     elif 'submarino' in link:
#         return 'submarino', _DICT_XPATH['submarino']
#
#
# def get_root(url, xpath):
#     """
#     Pega o root e retorna o texto da pagina
#     :param url: url da pagina
#     :param xpath: xpath da pagina
#     :return: Preço
#     """
#     resp = requests.get(url)
#     root = fromstring(resp.content)
#     price = get_text(root, xpath)
#
#     return price
#
#
# def get_text(root, xpath):
#     """
#     Extrai o texto da pagina
#     :param root: objeto root
#     :param xpath: xpath do texto
#     :return: texto
#     """
#     try:
#         price = root.xpath(xpath)
#         price = price[0].text
#
#         return price
#     except Exception as err:
#         raise Exception("Deu erro!! {}".format(err))
#
#
# def verify_value_to_notify(value, limit, site):
#     try:
#         value_str = value
#         value = value.replace('R$', '').replace('.', '').replace(' ', '')
#         value = value.replace(',', '.')
#         value = float(value)
#         if value <= limit:
#             s.call(['notify-send', site, f'Valor abaixo do limite: {value_str}'])
#     except Exception as err:
#         print(f'Erro na conversao de valor: {err}')
#
#
# def crawler():
#     """
#     Função principal para extrair os textos da pagina
#     :return: None
#     """
#     with open('json_produto.json') as f:
#         data = json.load(f)
#
#     while True:
#         print(f'Realizando consulta: {datetime.now()}')
#         for key in data.keys():
#             for link in data[key]:
#                 site, xpath = get_xpath_from_dict(link)
#                 value = get_root(link, xpath)
#                 verify_value_to_notify(value, 9100, site)
#                 print('Preço do site {}{}{}: {}{}{}'.format(bcolors.HEADER, site, bcolors.ENDC, bcolors.OKBLUE,
#                                                             value, bcolors.ENDC))
#
#         print('Aguardando!!!\n')
#         sleep(60*15)


class Crawler():
    def __init__(self):
        self.s3_bucket_crawler = getenv('S3_BUCKET_CRAWLER', '')
        self.crawler_prod_file_name = getenv('S3_CRAWLER_PROD_LIST_FILE', '')
        self.s3 = s3 = S3(self.s3_bucket_crawler)
        self.s3.create_s3_instance()
        self.json = load_json_products()
        self.crawler_time = self.json['scrap_time']
        self.os_notify = bool(self.json['os_notify'])
        self.products_list = self.json['products_list']

    def verify_value_to_notify(self, value, limit, site):
        try:
            value_str = value
            value = value.replace('R$', '').replace('.', '').replace(' ', '')
            value = value.replace(',', '.')
            value = float(value)
            if value <= limit:
                s.call(['notify-send', site, f'Valor abaixo do limite: {value_str}'])
        except Exception as err:
            print(f'Erro na conversao de valor: {err}')

    def run(self):
            print(f'Realizando consulta: {datetime.now()}')
            for prod in self.products_list:
                att_price, att_url = None, None
                for url in prod['links']:
                    robo = CrawlerFactory.create_crawler(url)
                    price, msg = robo.get_root()
                    if price:
                        if att_price is None:
                            att_price = price
                        elif att_price > price:
                            att_price = price
                            att_url = url
                prod['last_crawled_price'] = att_price if att_price else 0
                prod['price_url'] = att_url if att_url else ''
                self.s3.put_s3_obj('', prod, prod['id'])

            self.json['products_list'] = self.products_list
            self.s3.put_s3_obj('', self.json, self.crawler_prod_file_name)
                        # if self.os_notify:
                        #     self.verify_value_to_notify(price, prod['wanted_value'], url)


if __name__ == '__main__':
    crawler = Crawler()
    crawler.run()
    # crawler()
