# Teste de Frontend 💻

## Objetivo

Desenvolver uma interface web usando Vue.js que interaja com um servidor em Python para realizar uma busca textual.

## Como Funciona

1. **Entrada de dados**: Inserir o texto na busca por uma operadora
2. **Acesso ao servidor**: Após isso, será realizada uma chamada ao servidor por registros mais relevantes, seguindo o texto inserido.
3. **Listagem das operadoras**: Então, é exibido em uma tabela os dados dos registros relevantes conforme indicado.

## Como Executar

1. Instale as dependências necessárias na pasta `frontend` com o comando:
    ```bash
    npm install
    ```
2. Verifique se a porta `5173` está disponível em sua máquina.    
3. Execute o comando na pasta `frontend`:
    ```bash
    npm run dev 
    ```
4. Para realizar o teste, utilize `http://localhost:5173/`.    

## Projeto em nuvem

Para esse projeto, eu realizei o *deploy* em nuvem da interface, acesso em [https://teste-frontend-tau.vercel.app/](https://teste-frontend-tau.vercel.app/).`