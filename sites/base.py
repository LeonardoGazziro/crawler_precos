import requests
from lxml.html import fromstring


class CrawlerBase():
    def __init__(self, url):
        self.url = url

    def get_root(self):
        """
        Pega o root e retorna o texto da pagina
        :param url: url da pagina
        :param xpath: xpath da pagina
        :return: Preço
        """
        resp = requests.get(self.url)
        root = fromstring(resp.content)
        price, msg = self.get_price_and_create_msg(root)

        return price, msg

    def get_price_and_create_msg(self, root):
        """
        Extrai o texto da pagina
        :param root: objeto root
        :param xpath: xpath do texto
        :return: texto
        """
        try:
            price = self.get_xpath(root, '')
            msg = ''

            return price, msg
        except Exception as err:
            raise Exception("Deu erro!! {}".format(err))

    def get_xpath(self, root, xpath):
        try:
            value = root.xpath(xpath)
            if len(value) > 0:
                value = value[0].text
            else:
                value = None
            return value
        except Exception as err:
            raise Exception(f'Falha ao extrair informações: {err}')