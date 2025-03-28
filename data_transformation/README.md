# Teste de Transformação de Dados 🔄

## Objetivo

Este teste extrai os dados da tabela Rol de Procedimentos e Eventos em Saúde do PDF do Anexo I do teste anterior de Web Scraping, salva os dados em uma tabela estruturada no formato .CSV e por fim compacta em um arquivo *Teste_JoaoPedro.zip*. 

## Como Funciona

1. **Acessar o PDF**: O código acessa o PDF *Anexo I* do teste anterior em `/output`.
2. **Extração de dados**: O script procura por dados tabelados, seguindo o padrão de tabela com cabeçalho em todas as páginas.
3. **Criação da tabela**: Ao extrair todos os dados, é feita a tabelação no formato *.CSV*.
4. **Compactação**: Depois, ele compacta o arquivo em um único formato *ZIP*.

## Como Executar

1. Instale as dependências (caso não tenha feito no teste passado) necessárias com o comando:
    ```bash
    pip install -r requirements.txt
    ```
2. Execute o script de scraping na pasta `data_transformation` com o comando:
    ```bash
    python data-transformation.py
    ```
3. Verifique a pasta `output` para encontrar o arquivo compactado contendo o *Teste_JoaoPedro.zip*.