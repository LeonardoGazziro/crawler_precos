DOC_STRING = {
    "DADOS SOBRE A API": {
        "ENDPOINTS": ["inserir_produto", "listar_produtos", "alterar_preco_aviso",
                      "ver_info_produto", "ver_ultimos_precos", "ver_ultimo_preco_prod"],
        "DESCRICAO DOS ENDPOINTS": {
            "INSERIR PRODUTO": {
                "endpoint": "/inserir_produto",
                "metodo": "POST",
                "payload": "JSON",
                "descricao": "Insere um novo produto para pesquisa no Crawler",
                "exemplo": ""
            },
            "LISTAR PRODUTOS": {
                "endpoint": "/listar_produtos",
                "metodo": "GET",
                "descricao": "Retorna a lista de produtos que estão sendo pesquisados pelo crawler."
            },
            "ALTERAR PRECO AVISO": {
                "endpoint": "/alterar_preco_aviso",
                "metodo": "POST",
                "payload": "JSON",
                "descricao": "altera o valor de aviso de um produto",
                "exemplo": ""
            },
            "VER INFO PRODUTO": {
                "endpoint": "/ver_info_produto/{id_produto}",
                "metodo": "GET",
                "descricao": "retorna as informações de um produto, limite, nome e lista de links que estão sendo crawleadas"
            },
            "VER ULTIMOS PRECOS": {
                "endpoint": "/ver_ultimos_precos",
                "metodo": "GET",
                "descricao": "Retorna o JSON com os ultimos preços crawleados"
            },
            "VER ULTIMO PRECO DO PRODUTO": {
                "endpoint": "/ver_ultimo_preco_prod/{id_produto}",
                "metodo": "GET",
                "descricao": "retorna o ultimo preço de um produto utilizando o id do produto"
            }
        },
        "TEXT": "Conteudo destinado ao estudo de Python e utilização de micro serviços na nuvem da AWS.",
        "CREATED BY": "Leonardo Roberto Gazziro",
        "LINKEDIN": "www.linkedin.com/in/leonardo-roberto-gazziro",
        "GITHUB": "https://github.com/LeonardoGazziro"
    }
}


"""
    DADOS SOBRE A API
    ====================================================================================================================
        ENDPOINTS:
            inserir_produto  | listar_produtos    | alterar_preco_aviso 
            ver_info_produto | ver_ultimos_precos | ver_ultimo_preco_prod

        DESCRICAO DOS ENDPOINTS:
        ################################################################################################################
        INSERIR PRODUTO:
            endpoint: /inserir_produto
            metodo: POST
            payload: JSON
            descricao: Insere um novo produto para pesquisa no Crawler
            exemplo:
                {
                    "product": "NOME DO PRODUTO",
                    "wanted_price": valor do produto (INTEIRO),
                    "links": [
                        "link americanas",
                        "link submarino"
                    ]
                }

        LISTAR PRODUTOS:
            endpoint: /listar_produtos
            metodo: GET
            descricao: Retorna a lista de produtos que estão sendo pesquisados pelo crawler.

        ALTERAR PRECO AVISO:
            endpoint: /alterar_preco_produto
            metodo: POST
            payload: JSON
            descricao: altera o valor de aviso de um produto
            exemplo: 
                {
                    "product_id" ID_DO_PRODUTO,
                    "new_warning_price": NOVO VALOR DE AVISO (INTEIRO)
                }
                
        VER INFO PRODUTO:
            endpoint: /ver_info_produto/{id_produto}
            metodo: GET
            payload: -
            descricao: retorna as informações de um produto, limite, nome e lista de links que estão sendo crawleadas
            
        VER ULTIMOS PRECOS:
            endpoint: /ver_ultimos_precos
            metodo: GET
            payload: -
            descricao: Retorna o JSON com os ultimos preços crawleados
            
        VER ULTIMO PRECO DO PRODUTO:
            endpoint: /ver_ultimo_preco_prod/{id_produto}
            metodo: GET
            payload: -
            descricao: retorna o ultimo preço de um produto utilizando o id do produto

    ====================================================================================================================
    Conteudo destinado ao estudo de Python e utilização de micro serviços na nuvem da AWS.
    ####################################################################################################################
    *** Created by: Leonardo Roberto Gazziro ***
    *** LinkedIn: www.linkedin.com/in/leonardo-roberto-gazziro ***
    *** GitHub: https://github.com/LeonardoGazziro ***
    ####################################################################################################################
    """