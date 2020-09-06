from importlib import import_module


class CrawlerFactory():
    @staticmethod
    def create_crawler(url):
        if 'americanas' in url:
            crawler = 'Americanas'
        elif 'acer.com' in url:
            crawler = 'Acer'
        elif 'submarino' in url:
            crawler = 'Submarino'

        module_path = f'sites.{crawler.lower()}'
        module = import_module(module_path)
        cls = getattr(module, crawler)
        return cls.create_instance(url)
