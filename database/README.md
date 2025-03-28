# Teste de Banco de Dados 💾

## Objetivo

Este teste consiste em criar queries para estruturar tabelas necessárias para a alimentação via arquivos .CSV e elaborar consultas analíticas.

## Como Funciona

1. **Baixar os dados**: Para preparação do teste, precisamos ter os dados cadastrais das *Operadoras Ativas* e as *Demonstrações Contábeis* dos últimos 2 (dois) anos, então criei um script python para realizar esse processo.
2. **Criação das tabelas**: Então, foram criadas as tabelas correspondentes no banco de dados, tendo em mente que já é conhecido as colunas dos dados que iremos utilizar.
3. **Importação dos dados**: Com as tabelas criadas, realizamos a importação dos dados via script PostgreSQL. ATENÇÃO: por se tratar de um script interno de importação do script PostgreSQL, pode acontecer de ele não achar os arquivos para importação por falta de permissão, então é aconselhavel inserir os arquivos na pasta `data` onde o Postgre se encontra em sua máquia (conforme feito no teste).
4. **Consultas analíticas**: Por fim, com as tabelas preenchidas, podemos realizar as consultas pré-estabelecidas no teste.

## Como Executar

1. Instale as dependências (caso não tenha feito nos testes passados) necessárias com o comando:
    ```bash
    pip install -r requirements.txt
    ```
2. Execute o script de scraping na pasta `database` com o comando:
    ```bash
    python scraping.py
    ```
3. Prepare os arquivos obtidos na pasta `data` do seu Postgre (da forma em que foi obtido pelo script).
4. Execute o script `criacao_tabelas.sql` em seu PostgreSQL para realizar a criação das tabelas correspondentes.
5. Execute o script `importacao_csv.sql` em seu PostgreSQL para realizar a importação dos dados.
6. Execute o script `consultas.sql` em seu PostgreSQL para realizar as consultas do teste. 