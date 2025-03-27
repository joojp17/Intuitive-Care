-- 3.5 (1)
WITH ultima_data AS (
    SELECT 
        DATE_TRUNC('quarter', MAX(data)) AS inicio_trimestre,
        MAX(data) AS fim_trimestre
    FROM demonstracoes_contabeis
),
despesas_sinistros AS (
    SELECT 
        dc.reg_ans,
        o.razao_social,
        SUM(dc.vl_saldo_final - dc.vl_saldo_inicial) AS total_despesa
    FROM demonstracoes_contabeis dc
    JOIN ultima_data ud ON dc.data >= ud.inicio_trimestre AND dc.data <= ud.fim_trimestre
    JOIN operadoras_ativas o ON dc.reg_ans = o.registro_ans
    WHERE unaccent(replace(lower(dc.descricao), ' ', '')) = 
          unaccent(replace(lower('EVENTOS/ SINISTROS CONHECIDOS OU AVISADOS DE ASSISTÊNCIA A SAÚDE MEDICO HOSPITALAR'), ' ', ''))
    GROUP BY dc.reg_ans, o.razao_social
)
SELECT 
    reg_ans AS "Registro ANS",
    razao_social AS "Operadora",
    total_despesa AS "Total de Despesas com Sinistros no Último Trimestre",
    RANK() OVER (ORDER BY total_despesa DESC) AS "Ranking"
FROM despesas_sinistros
ORDER BY total_despesa DESC
LIMIT 10;

-- 3.5 (2)
WITH ultimo_ano AS (
    SELECT 
        DATE_TRUNC('year', MAX(data)) AS inicio_ano,
        MAX(data) AS fim_ano
    FROM demonstracoes_contabeis
    WHERE data <= DATE_TRUNC('year', CURRENT_DATE) - INTERVAL '1 day' 
),
despesas_anuais AS (
    SELECT 
        dc.reg_ans,
        oa.Razao_Social,
        SUM(dc.vl_saldo_final - dc.vl_saldo_inicial) AS total_despesa_anual
    FROM demonstracoes_contabeis dc
    JOIN ultimo_ano ua ON dc.data >= ua.inicio_ano AND dc.data <= ua.fim_ano
    JOIN operadoras_ativas oa ON dc.reg_ans = oa.Registro_ANS
    WHERE unaccent(replace(lower(dc.descricao), ' ', '')) = 
          unaccent(replace(lower('EVENTOS/ SINISTROS CONHECIDOS OU AVISADOS DE ASSISTÊNCIA A SAÚDE MEDICO HOSPITALAR'), ' ', ''))
    GROUP BY dc.reg_ans, oa.Razao_Social
)
SELECT 
    reg_ans AS "Registro ANS",
    Razao_Social AS "Operadora",
    total_despesa_anual AS "Total de Despesas com Sinistros no Último Ano",
    RANK() OVER (ORDER BY total_despesa_anual DESC) AS "Ranking"
FROM despesas_anuais
ORDER BY total_despesa_anual DESC
LIMIT 10;