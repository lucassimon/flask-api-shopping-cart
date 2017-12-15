#CASO de TESTE:

## Criar um carrinho sem items

Realizar um POST `http://localhost:5001/carts`

* Testar se os dados enviados foram retornados com sucesso

* Testar envio de parametros errados

## Criar um carrinho simulando o adicionar o produto

Realizar um POST `http://localhost:5001/carts` informando um `json`

```
{
    "supplier": {
        "supplier_id": "5a25310afb5d1b350e22f2e0"
    },
    "product": {
        "product_id": "5a268686fb5d1b26053b62d3",
        "seller_id": "5a269c88fb5d1b551bd2bb41",
        "supplier_id": "5a25310afb5d1b350e22f2e0",
        "name": "CERVEJAS KIT 3 un",
        "qty": 1,
        "price": 10772,
        "image": {
            "url" : "http://placehold.it/500x500",
            "title" : "CERVEJAS KIT 3 un"
        },
        "variant" : {
            "key" :"5a268687fb5d1b26053b62d5",
            "name" : "PADRAO",
            "price" : 0,
            "quantity" : 12
    }
    }
}
```

* Testar se os dados enviados foram retornados com sucesso

* Testar envio de parametros errados

## Buscar os dados de um carrinho

Realizar um GET `http://localhost:5001/carts/5a32ca0afb5d1b12e3d9be00` informando o ID como último parametro.

* Testar o retorno dos dados estao OK

* Testar envio de parametros errados

## Adicionar o produto ao carrinho

Realizar um PUT na rota `http://localhost:5001/carts/5a33ec88fb5d1b21fb49cbf3/product/add`

### Teste 1

Enviar os dados de fornecedor A

* Testar se os dados enviados foram retornados com sucesso

Principais campos:

- Preço, quantidade, total, subtotal, shipping

- Informações do produto: Nome e etc...


### Teste 2

Enviar os dados de fornecedor A com o produto B


Principais campos:

- Preço, quantidade, total, subtotal, shipping

- Informações do produto: Nome e etc...

### Teste 3

Enviar os dados novamente do fornecedor A com o produto B


Principais campos:

- Preço, quantidade, total, subtotal, shipping

- Informações do produto: Nome e etc...

### Teste 4

Enviar os dados novamente do fornecedor A com o produto B aumentando a
quantidade escolhida


Principais campos:

- Preço, quantidade, total, subtotal, shipping

- Informações do produto: Nome e etc...


### Teste 5

Enviar os dados novamente do fornecedor A com o produto C


Principais campos:

- Preço, quantidade, total, subtotal, shipping

- Informações do produto: Nome e etc...


### Teste 6

Enviar os dados novamente do fornecedor A com o produto D aumentando a quantidade

Principais campos:

- Preço, quantidade, total, subtotal, shipping

- Informações do produto: Nome e etc...

### Teste 7

Repetir os testes de 1 a 6 com outro fornecedor e outro produto


Principais campos:

- Preço, quantidade, total, subtotal, shipping

- Informações do produto: Nome e etc...




