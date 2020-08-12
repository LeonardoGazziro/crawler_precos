import requests
from lxml.html import fromstring


def crawler():
    acer_link = 'https://br-store.acer.com/notebook-acer-ph315-52-7210-ci79750h-16gb-nva-6gb-256gb-ssd-2tb-hdd-w10hcsl64-preto-fhd-156-nh-q63al-001/p?idsku=492&gclid=EAIaIQobChMI5qGOvbWW6wIVDBCRCh1dig3VEAYYASABEgK-rPD_BwE'

    resp = requests.get(acer_link)
    root = fromstring(resp.content)

    price = root.xpath('.//strong[contains(@class, "skuBestPrice")]')
    price = price[0].text

    print(f'Preço Acer: {price}')

    # Americanas
    americanas_link = 'https://www.americanas.com.br/produto/1348623153/so-hoje-notebook-gamer-acer-predator-helios-300-ph315-52-7210-rtx2060-tela-144hz-ci7-16gb-ssd-256gb-hd-2tb-win10?WT.srch=1&acc=e789ea56094489dffd798f86ff51c7a9&cor=Preto&epar=bp_pl_00_go_pc_gamer&gclid=EAIaIQobChMI5qGOvbWW6wIVDBCRCh1dig3VEAYYAiABEgKhSPD_BwE&i=573fe673eec3dfb1f801fc8e&o=5ddc1d32f8e95eac3d8815d2&opn=YSMESP&sellerid=11068167000453'

    americanas_resp = requests.get(americanas_link)
    americanas_root = fromstring(americanas_resp.content)

    americanas_price = americanas_root.xpath('.//span[contains(@class, "price__SalesPrice")]')
    americanas_price = americanas_price[0].text

    print(f'Preço Americanas: {americanas_price}')

    # Submarino
    submarino_link = 'https://www.submarino.com.br/produto/1348623153/so-hoje-notebook-gamer-acer-predator-helios-300-ph315-52-7210-rtx2060-tela-144hz-ci7-16gb-ssd-256gb-hd-2tb-win10?WT.srch=1&acc=d47a04c6f99456bc289220d5d0ff208d&cor=Preto&epar=bp_pl_00_go_pla_pcgamer_geral_gmv&gclid=EAIaIQobChMI5qGOvbWW6wIVDBCRCh1dig3VEAYYCiABEgJ9CvD_BwE&i=573ff205eec3dfb1f803f911&o=5ddc1ca2f8e95eac3d881521&opn=XMLGOOGLE&sellerid=11068167000453'

    submarino_resp = requests.get(submarino_link)
    submarino_root = fromstring(submarino_resp.content)

    submarino_price = submarino_root.xpath('.//span[contains(@class, "sales-price")]')
    submarino_price = submarino_price[0].text

    print(f'Preço Submarino: {submarino_price}')


if __name__ == '__main__':
    crawler()