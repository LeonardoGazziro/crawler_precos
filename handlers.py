import json
import uuid
from os import getenv
from docstring import DOC_STRING
from utils import json_inserir_prod_valido
from components.AWS_utils import S3
from main import Crawler


def help_handler(event, context):
    """
    GET - Lambda que mostra o as informações do projeto
    :param event: informações do Evento da Lambda
    :param context:  informações do contexto da Lambda
    :return: Retorna a ajuda.
    """
    return DOC_STRING


def inserir_produto_handler(event, context):
    """
    POST - Insere um novo produto para pesquisa no Crawler
    :param event: informações do Evento da Lambda
    :param context:  informações do contexto da Lambda
    :return: retorna o status e a mensagem sobre a inserção do produto.
    """
    body = event.get('body', {})
    s3_bucket = getenv('S3_BUCKET', '')
    print(s3_bucket)
    if body:
        # Verifica se o JSON é valido
        json_valido, msg = json_inserir_prod_valido(body)
        if json_valido:
            s3 = S3(s3_bucket)
            s3.create_s3_instance()
            # insere o JSON no S3
            resp, msg = s3.put_s3_obj('', body, body['product'])
            print(resp)
            print(msg)
            json_ret = {'status': 200, 'msg': 'Produto inserido com sucesso!'}
        else:
            json_ret = {'status': 500, 'msg': msg}
    else:
        json_ret = {'status': 500, 'msg': 'Json inválido!'}

    return json_ret


def inserir_json_crawler_handler(event, context):
    """
    Quando um objeto de novo produto é criado, triggar está lambda para inserir o produto no JSON de coleta.
    :param event: informações do Evento da Lambda
    :param context:  informações do contexto da Lambda
    :return: retorna o status e a mensagem sobre a inserção do produto.
    """
    s3_bucket_crawler = getenv('S3_BUCKET_CRAWLER', '')
    crawler_prod_file_name = getenv('S3_CRAWLER_PROD_LIST_FILE', '')

    s3_crawler = S3(s3_bucket_crawler)
    s3_crawler.create_s3_instance()
    crawler_json, msg = s3_crawler.get_s3_obj('', crawler_prod_file_name)
    # se o arquivo não existir, "False", então cria o arquivo
    if crawler_json == False:
        body = {
              "scrap_time": 3600,
              "os_notify": "True",
              "products_list": []
            }
        resp, msg = s3_crawler.put_s3_obj('', body, crawler_prod_file_name)
        if resp:
            crawler_json, msg = s3_crawler.get_s3_obj('', crawler_prod_file_name)

    for obj in event['Records']:
        # Informações do arquivo que foi inserido no S3
        bucket_name = obj['s3']['bucket']['name']
        obj = obj['s3']['object']['key']

        s3 = S3(bucket_name)
        s3.create_s3_instance()
        obj_json, msg = s3.get_s3_obj('', obj)
        # Cria um ID unico para o produto
        obj_json['id'] = str(uuid.uuid4())
        # Insere na lista para ser crawleado e cria um objeto para o item no bucket
        crawler_json['products_list'].append(obj_json)
        resp, msg = s3_crawler.put_s3_obj('', crawler_json, crawler_prod_file_name)
        if resp:
            print('Inserido com sucesso.')

        obj_json['last_crawled_price'] = 0
        resp, msg = s3_crawler.put_s3_obj('', obj_json, obj_json['id'])


def listar_produtos_handler(event, context):
    """
    GET - Retorna a lista de produtos que estão sendo pesquisados pelo crawler.
    :param event: informações do Evento da Lambda
    :param context: informações do contexto da Lambda
    :return: retorna um JSON com a lista de produtos que estão sendo crawleados
    """
    s3_bucket_crawler = getenv('S3_BUCKET_CRAWLER', '')
    crawler_prod_file_name = getenv('S3_CRAWLER_PROD_LIST_FILE', '')

    s3_crawler = S3(s3_bucket_crawler)
    s3_crawler.create_s3_instance()
    crawler_json, msg = s3_crawler.get_s3_obj('', crawler_prod_file_name)
    if crawler_json:
        return {'status': 200, 'products_list': crawler_json['products_list']}
    else:
        return {'status': 404, 'msg': 'Lista de  produtos não encontrada'}


def alterar_preco_aviso_handler(event, context):
    """
    POST - altera o valor de aviso de um produto
    :param event: informações do Evento da Lambda
    :param context:  informações do contexto da Lambda
    :return: retorna o status e a mensagem sobre a alteracao do preço de aviso
    """
    s3_bucket_crawler = getenv('S3_BUCKET_CRAWLER', '')
    crawler_prod_file_name = getenv('S3_CRAWLER_PROD_LIST_FILE', '')

    resp = None
    body = event.get('body', {})

    s3_crawler = S3(s3_bucket_crawler)
    s3_crawler.create_s3_instance()
    crawler_json, msg = s3_crawler.get_s3_obj('', crawler_prod_file_name)

    # Busca o produto e altera seu valor tanto no arquivo de crawler quando no arquivo do item
    if crawler_json and body != {}:
        for prod in crawler_json['products_list']:
            if prod['id'] == body['id']:
                prod['wanted_price'] = body['wanted_price']
                resp, msg = s3_crawler.put_s3_obj('', crawler_json, crawler_prod_file_name)
                prod_json, msg = s3_crawler.get_s3_obj('', prod['id'])
                if prod_json:
                    prod_json['wanted_price'] = body['wanted_price']
                    resp, msg = s3_crawler.put_s3_obj('', prod_json, prod['id'])
                break

    if resp:
        return {'status': 200, 'msg': 'Preço atualizado com sucesso!'}
    else:
        return {'status': 200, 'msg': 'Falha ao atualizar o preço do produto!'}


def ver_info_produto_handler(event, context):
    """
    GET - retorna as informações de um produto, limite, nome e lista de links que estão sendo crawleadas
    :param event: informações do Evento da Lambda
    :param context:  informações do contexto da Lambda
    :return: retorna as informações de um produto, caso exista
    """
    s3_bucket_crawler = getenv('S3_BUCKET_CRAWLER', '')

    prod_json, msg = None, None
    path = event.get('path', {})
    if 'id' in path.keys():
        s3 = S3(s3_bucket_crawler)
        s3.create_s3_instance()
        prod_json, msg = s3.get_s3_obj('', path['id'])

    if prod_json:
        prod_json['status'] = 200
        return prod_json
    else:
        return {'status': 404, 'msg': 'Produto não encontrado'}


def ver_ultimos_precos_handler(event, context):
    """
    GET - Retorna o JSON com os ultimos preços crawleados
    :param event: informações do Evento da Lambda
    :param context:  informações do contexto da Lambda
    :return: retorna os ultimos preços que foram crawleados para cada produto
    """
    s3_bucket_crawler = getenv('S3_BUCKET_CRAWLER', '')
    crawler_prod_file_name = getenv('S3_CRAWLER_PROD_LIST_FILE', '')

    last_price_list, msg = list(), None
    s3 = S3(s3_bucket_crawler)
    s3.create_s3_instance()
    list_files, msg = s3.get_bucket_files(s3_bucket_crawler)
    # Monta um JSON de retorno com o valor de todos os produtos
    for s3_file in list_files:
        if s3_file['Key'] == f'{crawler_prod_file_name}.json':
            continue
        else:
            prod_json, msg = s3.get_s3_obj('', s3_file['Key'])
            last_price_list.append({
                'id': prod_json['id'],
                'product': prod_json['product'],
                'last_crawled_price': prod_json['last_crawled_price']
            })

    if len(last_price_list) > 0:
        return {'status': 200, 'price_list': last_price_list}
    else:
        return {'status': 404, 'msg': 'Lista de preços não encontrada.'}


def ver_ultimo_preco_prod_handler(event, context):
    """
    GET - retorna o ultimo preço de um produto utilizando o id do produto
    :param event: informações do Evento da Lambda
    :param context:  informações do contexto da Lambda
    :return: retorna o ultimo preço de um produto crawleado
    """
    s3_bucket_crawler = getenv('S3_BUCKET_CRAWLER', '')

    prod_json, msg = None, None
    path = event.get('path', {})
    if 'id' in path.keys():
        s3 = S3(s3_bucket_crawler)
        s3.create_s3_instance()
        prod_json, msg = s3.get_s3_obj('', path['id'])

    if prod_json:
        return {'status': 200, 'id': prod_json['id'],
                'product': prod_json['product'],
                'last_crawled_price': prod_json['last_crawled_price']}
    else:
        return {'status': 404, 'msg': 'Produto não encontrado'}


def crawler_prods_handler(event, context):
    """
    Coleta o valor dos produtos que estão na lista para ser crawleados
    :param event: informações do Evento da Lambda
    :param context:  informações do contexto da Lambda
    :return: None
    """
    crawler = Crawler()
    crawler.run()


if __name__ == '__main__':
    # print(help_handler('', ''))

    ex_event = json.dumps({'body':
        {'product': 'Notebook Predator Elios 300', 'wanted_price': 9200,
         'links': [
             "https://www.americanas.com.br/produto/1824928346/notebook-gamer-acer-predator-helios-300-ph315-52-7210-9a-intel-core-i7-16gb-geforce-rtx-2060-com-6gb-2tb-256gb-ssd-15-6-windows-10-preto?WT.srch=1&acc=e789ea56094489dffd798f86ff51c7a9&epar=bp_pl_00_go_inf_notebooks_todas_geral_gmv&gclid=Cj0KCQjw-O35BRDVARIsAJU5mQVD5tguYua-7adjtroZ_I7DkS_e-PhFy43w6JbaLKeAJqgn-n8X0_8aAoHWEALw_wcB&i=5612cbe46ed24cafb5cae011&o=5f22ba94f8e95eac3d1b77f3&opn=YSMESP&sellerid=02&voltagem=BIVOLT",
            "https://br-store.acer.com/notebook-acer-ph315-52-7210-ci79750h-16gb-nva-6gb-256gb-ssd-2tb-hdd-w10hcsl64-preto-fhd-156-nh-q63al-001/p?idsku=492&gclid=EAIaIQobChMI5qGOvbWW6wIVDBCRCh1dig3VEAYYASABEgK-rPD_BwE",
            "https://www.submarino.com.br/produto/1348623153/so-hoje-notebook-gamer-acer-predator-helios-300-ph315-52-7210-rtx2060-tela-144hz-ci7-16gb-ssd-256gb-hd-2tb-win10?WT.srch=1&acc=d47a04c6f99456bc289220d5d0ff208d&cor=Preto&epar=bp_pl_00_go_pla_pcgamer_geral_gmv&gclid=EAIaIQobChMI5qGOvbWW6wIVDBCRCh1dig3VEAYYCiABEgJ9CvD_BwE&i=573ff205eec3dfb1f803f911&o=5ddc1ca2f8e95eac3d881521&opn=XMLGOOGLE&sellerid=11068167000453"

            ]},
        'method': 'POST', 'principalId': '',
        'stage': 'dev',
        'cognitoPoolClaims': {'sub': ''},
        'enhancedAuthContext': {},
        'headers': {'Accept': '*/*', 'Accept-Encoding': 'gzip, deflate, br',
                    'Cache-Control': 'no-cache', 'CloudFront-Forwarded-Proto': 'https',
                    'CloudFront-Is-Desktop-Viewer': 'true',
                    'CloudFront-Is-Mobile-Viewer': 'false',
                    'CloudFront-Is-SmartTV-Viewer': 'false',
                    'CloudFront-Is-Tablet-Viewer': 'false',
                    'CloudFront-Viewer-Country': 'BR',
                    'Content-Type': 'application/json',
                    'Host': '1nhucniq8b.execute-api.us-east-1.amazonaws.com',
                    'Postman-Token': '0d40ddc9-494c-438c-9e34-30f9f44ea018',
                    'User-Agent': 'PostmanRuntime/7.26.3',
                    'Via': '1.1 3fff6e22f8d6795a61bfdca17d362ca5.cloudfront.net (CloudFront)',
                    'X-Amz-Cf-Id': 'OKNx6jkzKLQ3nbtD0t4JTNynGlc2TZDSemAepsPC-8Kv0ZV1f6Tz7w==',
                    'X-Amzn-Trace-Id': 'Root=1-5f4bf435-7d8aa2621cebaaabfa719a0c',
                    'X-Forwarded-For': '138.204.24.213, 64.252.179.69',
                    'X-Forwarded-Port': '443', 'X-Forwarded-Proto': 'https'},
        'query': {},
        'path': {},
        'identity': {'cognitoIdentityPoolId': '', 'accountId': '', 'cognitoIdentityId': '', 'caller': '',
                     'sourceIp': '138.204.24.213', 'principalOrgId': '', 'accessKey': '',
                     'cognitoAuthenticationType': '', 'cognitoAuthenticationProvider': '', 'userArn': '',
                     'userAgent': 'PostmanRuntime/7.26.3', 'user': ''},
        'stageVariables': {},
        'requestPath': '/inserir_produto'})

    ex_event_s3 = {'Records': [{'eventVersion': '2.1', 'eventSource': 'aws:s3', 'awsRegion': 'us-east-1',
                  'eventTime': '2020-09-06T18:11:57.722Z', 'eventName': 'ObjectCreated:Put',
                  'userIdentity': {'principalId': 'A1GN6EPM0JKA8K'},
                  'requestParameters': {'sourceIPAddress': '177.42.49.149'},
                  'responseElements': {'x-amz-request-id': '7857E87B7E4BA60D',
                                       'x-amz-id-2': 'lmNysI3mKLmMQoOzCtPnjT8usl2fMUYbIyipfE59v3oWuyu44XxI/L2tXxRPkqjC6uUNu3rGB/eekMpWqOj6RceGfrLLLTeg'},
                  's3': {'s3SchemaVersion': '1.0', 'configurationId': 'cc7a7b1c-d354-413c-94e0-c4c2e3cf153a',
                         'bucket': {'name': 'novo-produto', 'ownerIdentity': {'principalId': 'A1GN6EPM0JKA8K'},
                                    'arn': 'arn:aws:s3:::novo-produto'},
                         'object': {'key': 'notebook_predator_elios_300.json', 'size': 1172,
                                    'eTag': 'f64c165d9209eb645b660f04b27dc8d2', 'sequencer': '005F552670F6AF15F4'}}}]}

    ex_event_att_price = json.dumps({'body':
                               {'id': '116d4fb7-45b5-44e4-9d9e-0af8b9750c6a', 'wanted_price': 9000},
                           'method': 'POST', 'principalId': '',
                           'stage': 'dev',
                           'cognitoPoolClaims': {'sub': ''},
                           'enhancedAuthContext': {},
                           'headers': {'Accept': '*/*', 'Accept-Encoding': 'gzip, deflate, br',
                                       'Cache-Control': 'no-cache', 'CloudFront-Forwarded-Proto': 'https',
                                       'CloudFront-Is-Desktop-Viewer': 'true',
                                       'CloudFront-Is-Mobile-Viewer': 'false',
                                       'CloudFront-Is-SmartTV-Viewer': 'false',
                                       'CloudFront-Is-Tablet-Viewer': 'false',
                                       'CloudFront-Viewer-Country': 'BR',
                                       'Content-Type': 'application/json',
                                       'Host': '1nhucniq8b.execute-api.us-east-1.amazonaws.com',
                                       'Postman-Token': '0d40ddc9-494c-438c-9e34-30f9f44ea018',
                                       'User-Agent': 'PostmanRuntime/7.26.3',
                                       'Via': '1.1 3fff6e22f8d6795a61bfdca17d362ca5.cloudfront.net (CloudFront)',
                                       'X-Amz-Cf-Id': 'OKNx6jkzKLQ3nbtD0t4JTNynGlc2TZDSemAepsPC-8Kv0ZV1f6Tz7w==',
                                       'X-Amzn-Trace-Id': 'Root=1-5f4bf435-7d8aa2621cebaaabfa719a0c',
                                       'X-Forwarded-For': '138.204.24.213, 64.252.179.69',
                                       'X-Forwarded-Port': '443', 'X-Forwarded-Proto': 'https'},
                           'query': {},
                           'path': {'id': '116d4fb7-45b5-44e4-9d9e-0af8b9750c6a'},
                           'identity': {'cognitoIdentityPoolId': '', 'accountId': '', 'cognitoIdentityId': '',
                                        'caller': '',
                                        'sourceIp': '138.204.24.213', 'principalOrgId': '', 'accessKey': '',
                                        'cognitoAuthenticationType': '', 'cognitoAuthenticationProvider': '',
                                        'userArn': '',
                                        'userAgent': 'PostmanRuntime/7.26.3', 'user': ''},
                           'stageVariables': {},
                           'requestPath': '/inserir_produto'})

    # inserir_produto_handler(ex_event, '')
    # inserir_json_crawler_handler(ex_event_s3, "")
    # listar_produtos_handler('', '')
    # alterar_preco_aviso_handler(ex_event_att_price, '')
    # ver_info_produto_handler(ex_event_att_price, '')
    # ver_ultimos_precos_handler('', '')
    crawler_prods_handler('', '')