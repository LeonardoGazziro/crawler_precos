# crawler-precos
## Projeto
O projeto tem como objetivo demonstrar a utilização de recursos da AWS, criando um projeto simples
que coleta o valor de alguns produtos.

Projeto criado para estudo e demonstração do uso de AWS.
## Tecnologias
- Python 3.7
- AWS Lambda
- AWS S3
- Serverless YML

## Instalação
### Python
``sudo apt install python3.7``
### AWS Cli
``-``
### Serverless
```
cd PASTA_DO_PROJETO
npm install --save-dev serverless-wsgi serverless-python-requirements
```
## Detalhamento do Projeto
### DADOS SOBRE A API
#### ENDPOINTS
- help
- inserir_produto
- listar_produtos
- alterar_preco_aviso
- ver_info_produto
- ver_ultimos_precos
- ver_ultimo_preco_prod
#### DESCRICAO DOS ENDPOINTS
##### HELP
- endpoint: /help                                
- metodo: GET                                              
- payload: JSON                                             
- descricao: Retorna o Json com as informações sobre a API

##### INSERIR PRODUTO:
- endpoint: /inserir_produto
- metodo: POST
- payload: JSON
- descricao: Insere um novo produto para pesquisa no Crawler
- exemplo: 
```
{
    "product": "NOME DO PRODUTO",
    "wanted_price": valor do produto (INTEIRO),
    "links": [
        "link americanas",
        "link submarino"
    ]
}
```
##### LISTAR PRODUTOS:
- endpoint: /listar_produtos
- metodo: GET
- descricao: Retorna a lista de produtos que estão sendo pesquisados pelo crawler.

##### ALTERAR PRECO AVISO:
- endpoint: /alterar_preco_produto
- metodo: POST
- payload: JSON
- descricao: altera o valor de aviso de um produto
- exemplo:
``` 
{
    "product_id" ID_DO_PRODUTO,
    "new_warning_price": NOVO VALOR DE AVISO (INTEIRO)
}
```                
##### VER INFO PRODUTO:
- endpoint: /ver_info_produto/{id_produto}
- metodo: GET
- payload: -
- descricao: retorna as informações de um produto, limite, nome e lista de links que estão sendo crawleadas
            
##### VER ULTIMOS PRECOS:
- endpoint: /ver_ultimos_precos
- metodo: GET
- payload: -
- descricao: Retorna o JSON com os ultimos preços crawleados
            
##### VER ULTIMO PRECO DO PRODUTO:
- endpoint: /ver_ultimo_preco_prod/{id_produto}
- metodo: GET
- payload: -
- descricao: retorna o ultimo preço de um produto utilizando o id do produto

### Deploy
Incie o serverless no diretorio do projeto
```
cd PASTA_DO_PROJETO
npm install --save-dev serverless-wsgi serverless-python-requirements
```
Faça o deploy utilizando o SLS
```
sls deploy --aws-profile NOME_PROFILE --accessid ACCESS_ID --accessseckey ACCESS_SECRET_KEY
```


* *** Conteudo destinado ao estudo de Python e utilização de micro serviços na nuvem da AWS.
* *** Created by: Leonardo Roberto Gazziro ***
* *** LinkedIn: www.linkedin.com/in/leonardo-roberto-gazziro ***
* *** GitHub: https://github.com/LeonardoGazziro ***
