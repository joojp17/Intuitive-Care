DO $$ 
DECLARE 
    ano INT := 2023; -- ano inicial
    trimestre INT;
    base TEXT := 'C:\Program Files\PostgreSQL\17\data\'; -- caminho dos CSVs
    caminho TEXT;
    arquivo TEXT;
    ans_ativos INT[];
BEGIN
    -- operadoras ativas
	copy operadoras_ativas
	FROM 'C:\Program Files\PostgreSQL\17\data\Relatorio_cadop.csv' 
	WITH (FORMAT csv, HEADER true, DELIMITER ';');

    SELECT ARRAY(SELECT Registro_ANS FROM operadoras_ativas) INTO ans_ativos;
    
    -- demonstracoes_contabeis
    WHILE ano <= 2024 LOOP 
        caminho := base || ano ||'\';

        FOR trimestre IN 1..4 LOOP
            arquivo := caminho || trimestre || 'T' || ano || '.csv';

            -- tabela temporaria
            CREATE TEMP TABLE temp_dados (
                DATA TEXT,
                REG_ANS TEXT,
                CD_CONTA_CONTABIL TEXT,
                DESCRICAO TEXT,
                VL_SALDO_INICIAL TEXT,
                VL_SALDO_FINAL TEXT
            ) ON COMMIT DROP;

            EXECUTE format(
                'COPY temp_dados FROM %L
                 WITH (FORMAT csv, HEADER true, DELIMITER '';'', NULL '''', ENCODING''UTF8'')',
                arquivo
            );

            INSERT INTO demonstracoes_contabeis
            SELECT 
                DATA::DATE,
                REG_ANS::INTEGER,
                CD_CONTA_CONTABIL::INTEGER,
                DESCRICAO,
                REPLACE(VL_SALDO_INICIAL, ',', '.')::NUMERIC(15,2),
                REPLACE(VL_SALDO_FINAL, ',', '.')::NUMERIC(15,2)
            FROM temp_dados
            WHERE REG_ANS::INTEGER = ANY(ans_ativos);

			DROP TABLE temp_dados;

            RAISE NOTICE 'Importado: %', arquivo;
        END LOOP;

        ano := ano + 1;
    END LOOP;
END $$;