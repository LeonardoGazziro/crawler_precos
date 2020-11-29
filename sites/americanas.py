from sites.base import CrawlerBase
from utils import bcolors


class Americanas(CrawlerBase):
    def __init__(self, url):
        self.site = 'Americanas'
        super().__init__(url)

    def get_price_and_create_msg(self, root):
        """
        Extrai o texto da pagina
        :param root: objeto root
        :return: texto
        """
        try:
            msg = None
            price = self.get_xpath(root, './/span[contains(@class, "price__SalesPrice")]')
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
        return Americanas(url=url)