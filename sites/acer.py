from sites.base import CrawlerBase
from utils import bcolors


class Acer(CrawlerBase):
    def __init__(self, url):
        self.site = 'Acer'
        super().__init__(url)

    def get_price_and_create_msg(self, root):
        """
        Extrai o texto da pagina
        :param root: objeto root
        :return: texto
        """
        try:

            price = self.get_xpath(root, './/strong[contains(@class, "skuBestPrice")]')
            if price:
                msg = 'Preço do site {}{}{}: {}{}{}'.format(bcolors.HEADER, self.site, bcolors.ENDC, bcolors.OKBLUE,
                                                            price, bcolors.ENDC)
            else:
                msg = 'Preço não encontrado!!'

            return price, msg
        except Exception as err:
            raise Exception("Deu erro!! {}".format(err))

    @staticmethod
    def create_instance(url):
        return Acer(url=url)