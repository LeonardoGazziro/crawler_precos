import requests
import json
from lxml.html import fromstring

_DICT_XPATH = {
    'americanas': './/span[contains(@class, "price__SalesPrice")]',
    'acer.com': './/strong[contains(@class, "skuBestPrice")]',
    'submarino': './/span[contains(@class, "sales-price")]'
}


def get_xpath_from_dict(link):
    if 'americanas' in link:
        return 'americanas', _DICT_XPATH['americanas']
    elif 'acer.com' in link:
        return 'acer.com', _DICT_XPATH['acer.com']
    elif 'submarino' in link:
        return 'submarino', _DICT_XPATH['submarino']


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
    try:
        price = root.xpath(xpath)
        price = price[0].text

        return price
    except Exception as err:
        raise Exception("Deu erro!! {}".format(err))


def crawler():
    """
    Função principal para extrair os textos da pagina
    :return: None
    """
    with open('json_produto.json') as f:
        data = json.load(f)

    for key in data.keys():
        for link in data[key]:
            site, xpath = get_xpath_from_dict(link)
            print('Preço do site {}: {}'.format(site, get_root(link, xpath)))


if __name__ == '__main__':
    crawler()
