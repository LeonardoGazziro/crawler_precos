import json


def load_json_products():
    with open('json_produto.json') as f:
        data = json.load(f)

    return data


def json_inserir_prod_valido(json):
    """
    Verifica se o JSON de inserção de produto é valido.
    exemplo: {
                "product": "NOME DO PRODUTO",
                "wanted_price": valor do produto (INTEIRO),
                "links": [
                    "link americanas",
                    "link submarino"
                ]
             }
    :param json: JSON
    :return: True ou False
    """
    ret = True
    msg = None
    if "product" not in json or json['product'] is None or json['product'].strip() == '':
        ret = False
        msg = 'Json incorreto, "product" não foi informado ou com valor incorreto!'
    elif "wanted_price" not in json or json['wanted_price'] is None or not isinstance(json['wanted_price'], int):
        ret = False
        msg = 'Json incorreto, "wanted_price" não foi informado ou com valor incorreto!'
    elif "links" not in json or json['links'] is None or not isinstance(json['links'], list):
        ret = False
        msg = 'Json incorreto, "links" não foi informado ou com valor incorreto!'
    else:
        for link in json['links']:
            if 'http' not in link:
                ret = False
                msg = 'Json incorreto, URL do produto no formato incorreto!'

    return ret, msg


class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'
