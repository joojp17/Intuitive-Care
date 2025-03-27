CREATE TABLE operadoras_ativas (
    Registro_ANS integer NOT NULL UNIQUE,
    CNPJ varchar(14),
    Razao_Social VARCHAR(255),
    Nome_Fantasia VARCHAR(255),
    Modalidade VARCHAR(100),
    Logradouro VARCHAR(255),
    Numero VARCHAR(20),
    Complemento VARCHAR(100),
    Bairro VARCHAR(100),
    Cidade VARCHAR(100),
    UF CHAR(2),
    CEP VARCHAR(8),
    DDD VARCHAR(3),
    Telefone VARCHAR(20),
    Fax VARCHAR(20),
    Endereco_eletronico VARCHAR(100),
    Representante VARCHAR(255),
    Cargo_Representante VARCHAR(100),
    Regiao_de_Comercializacao INTEGER,
    Data_Registro_ANS DATE
);

CREATE TABLE demonstracoes_contabeis (
    DATA DATE,
    REG_ANS integer,
    CD_CONTA_CONTABIL INTEGER,
    DESCRICAO VARCHAR(255),
    VL_SALDO_INICIAL numeric(15,2),
    VL_SALDO_FINAL numeric(15,2),
    FOREIGN KEY (REG_ANS) REFERENCES operadoras_ativas(Registro_ANS)
);