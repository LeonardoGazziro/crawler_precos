import requests
import json
from lxml.html import fromstring


def get_root(url, xpath):
    """
    Pega o root e retorna o texto da pagina
    :param url: url da pagina
    :param xpath: xpath da pagina
    :return: Preço
    """
    resp = requests.get(url)
    root = fromstring(resp.content)
    price = get_text(root, xpath)

    return price


def get_text(root, xpath):
    """
    Extrai o texto da pagina
    :param root: objeto root
    :param xpath: xpath do texto
    :return: texto
    """
    price = root.xpath(xpath)
    price = price[0].text

    return price


def crawler():
    """
    Função principal para extrair os textos da pagina
    :return: None
    """
    with open('json_produto.json') as f:
        data = json.load(f)

    for key in data.keys():
        print('Preço Acer: {}'.format(get_root(data[key][0], './/strong[contains(@class, "skuBestPrice")]')))
        print('Preço Americanas: {}'.format(get_root(data[key][1], './/span[contains(@class, "price__SalesPrice")]')))
        print('Preço Submarino: {}'.format(get_root(data[key][2], './/span[contains(@class, "sales-price")]')))


if __name__ == '__main__':
    crawler()
