# Teste de Web Scraping 🔍

## Objetivo

Este teste realiza o acesso ao site da ANS, faz o download dos **Anexos I e II** em formato PDF e os compacta em um único arquivo para facilitar o armazenamento e manipulação dos dados.

## Como Funciona

1. **Acessar o site**: O código faz o scraping do site [https://www.gov.br/ans/pt-br/acesso-a-informacao/participacao-da-sociedade/atualizacao-do-rol-de-procedimentos](https://www.gov.br/ans/pt-br/acesso-a-informacao/participacao-da-sociedade/atualizacao-do-rol-de-procedimentos).
2. **Baixar os anexos**: O script encontra e baixa os arquivos PDF dos Anexos I e II.
3. **Compactação**: Depois, ele compacta os arquivos em um único formato (ZIP).

## Como Executar

1. Instale as dependências necessárias com o comando:
    ```bash
    pip install -r requirements.txt
    ```
2. Execute o script de scraping na pasta `web_scraping` com o comando:
    ```bash
    python scraping.py
    ```
3. Verifique a pasta `output` para encontrar o arquivo compactado contendo os Anexos I e II.