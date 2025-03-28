# Teste de API 🌐

## Objetivo

Desenvolver um servidor em Python para realizar consultas em um arquivo *.CSV* e disponibilizar em uma rota.

## Como Funciona

1. **Acesso aos dados**: O servidor acessa o .CSV onde ficam os dados
2. **Rota de busca**: Então, por meio de uma rota cadastrada, no do teste `/api/buscar`, exibir os registros mais relevantes, filtrados por *Razão Social*.

## Como Executar

1. Instale as dependências (caso não tenha feito nos testes passados) necessárias com o comando:
    ```bash
    pip install -r requirements.txt
    ```
2. Verifique se a porta `5000` está disponível em sua máquina.    
3. Execute o script de app.py na pasta `api` com o comando:
    ```bash
    python app.py
    ```
4. Para realizar o teste, utilize `http://localhost:5000/api/buscar?q=sua_query_aqui`.    

## Projeto em nuvem

Para esse projeto, eu realizei o *deploy* em nuvem da API, acesso em [https://teste-api-0ocr.onrender.com/api/buscar](https://teste-api-0ocr.onrender.com/api/buscar).

## Passos

1. Por se tratar de uma hospedagem de teste, pode ser que demore alguns segundos para o funcionamento da API.
2. utilize o parâmetro `?q=` para realizar as buscas, exemplo: `https://teste-api-0ocr.onrender.com/api/buscar?q=bradesco`