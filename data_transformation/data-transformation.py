import os
import zipfile
import tabula
import pandas as pd

def mesclar_quebras(df):
    """
    Limpa e agrupa colunas quebradas em linhas múltiplas.
    
    Args:
        df (pd.DataFrame): DataFrame para processamento
    
    Returns:
        pd.DataFrame: DataFrame processado
    """
    # Função para mesclar valores de células quebradas
    def mesclar_valores(df):

        df_limpo = df.copy()

        for col in df_limpo.columns:
            # Verificar se há valores quebrados
            df_limpo[col] = df_limpo[col].apply(lambda x: ' '.join(str(x).split()) if pd.notna(x) else x)
        
        return df_limpo
    
    # Mesclar cabeçalhos quebrados
    def mesclar_cabecalho(df):
        # Se houver mais de uma linha de cabeçalho
        if len(df.columns) > len(df.columns.unique()):
            # Pegar as primeiras duas linhas
            cabecalho_linha1 = df.columns
            cabecalho_linha2 = df.iloc[0]
            
            colunas_novas = []
            for i, col in enumerate(cabecalho_linha1):
                # Verificar se o valor da próxima linha não é nulo
                texto_adicional = str(cabecalho_linha2[i]) if pd.notna(cabecalho_linha2[i]) else ''
                nova_coluna = f"{col} {texto_adicional}".strip()
                colunas_novas.append(nova_coluna)
            
            df.columns = colunas_novas
            df = df.iloc[1:]  # Remover a linha de cabeçalho adicional
        
        return df
    
    df_limpo = df.copy()
    df_limpo = mesclar_cabecalho(df_limpo)
    df_limpo = mesclar_valores(df_limpo)
    
    df_limpo.reset_index(drop=True, inplace=True)
    
    return df_limpo

def extrair_tabelas(pdf_path):
    """
    Extrai as tabelas do Rol de Procedimentos e Eventos em Saúde
    
    Args:
        pdf_path (str): Caminho completo para o arquivo PDF
    
    Returns:
        pandas.DataFrame: DataFrame consolidado com os dados extraídos
    """
    try:
        
        dfs = tabula.read_pdf(
            pdf_path, 
            pages='all',  
            multiple_tables=True,
            pandas_options={'dtype': str},
            guess=False, 
            stream=False, 
            lattice=True
        )
        
        # Filtrar tabelas válidas
        tabelas = [
            df for df in dfs 
            if len(df.columns) >= 10 and  # Verificar número mínimo de colunas
            df.columns[0] != 'Unnamed: 0'  
        ]
        
        # Processar cada tabela
        if tabelas:
            tabelas_processadas = []
            for df in tabelas:
                # Limpar e mesclar dados
                df.columns = [
                    col.replace('\r', ' ').replace('/r', ' ').strip() 
                    for col in df.columns
                ]

                df_limpo = mesclar_quebras(df)
                
                # Remover linhas totalmente vazias
                df_limpo.dropna(how='all', inplace=True)
                
                # Remover linhas de legenda e página
                df_limpo = df_limpo[
                    ~df_limpo.iloc[:, 0].str.contains('Legenda:', na=False) &
                    ~df_limpo.iloc[:, 0].str.contains('Página', na=False)
                ]
                
                tabelas_processadas.append(df_limpo)
            
            # Concatenar tabelas
            combined_df = pd.concat(tabelas_processadas, ignore_index=True)
            
            return combined_df
        
        print("Nenhuma tabela válida encontrada.")
        return None

    except Exception as e:
        print(f"Erro ao extrair dados do PDF: {e}")
        import traceback
        traceback.print_exc()
        return None

def sub_abreviacao(df):
    abbr_map = {'OD': 'Odontológico', 'AMB': 'Ambulatorial'}
    df_atualizado = df.copy()
    df_atualizado.rename(columns=abbr_map, inplace=True)
    return df_atualizado

def salvar_csv(df, filename):
    try:
        df.to_csv(filename, index=False, encoding='utf-8')
        print(f"Dados salvos em {filename}")
    except Exception as e:
        print(f"Erro ao salvar CSV: {e}")

def salvar_zip(csv_path, zip_filename):
    try:
        with zipfile.ZipFile(zip_filename, 'w', zipfile.ZIP_DEFLATED) as zipf:
            zipf.write(csv_path, arcname=os.path.basename(csv_path))
        print(f"Arquivo compactado em {zip_filename}")
    except Exception as e:
        print(f"Erro ao compactar arquivo: {e}")

def main():
    # Caminho para o arquivo PDF dentro do ZIP do scraping anterior
    base_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'web_scraping', 'downloads', 'anexos.zip'))
    
    if not os.path.exists(base_path):
        print(f"Arquivo não encontrado: {base_path}")
        return
    
    with zipfile.ZipFile(base_path, 'r') as zip_ref:
        pdf = [f for f in zip_ref.namelist() if f.lower().endswith('.pdf')]
        
        if not pdf:
            print("Nenhum PDF encontrado no ZIP")
            return
        
        pdf_filename = pdf[0]
        zip_ref.extract(pdf_filename)
    
    # Extrair tabelas do PDF
    df = extrair_tabelas(pdf_filename)
    
    if df is None:
        print("Falha na extração dos dados")
        return
    
    df_updated = sub_abreviacao(df)
    
    csv_filename = f"Teste_JoaoPedro.csv"
    zip_filename = f"Teste_JoaoPedro.zip"
    
    salvar_csv(df_updated, csv_filename)
    salvar_zip(csv_filename, zip_filename)
    
    os.remove(pdf_filename)
    os.remove(csv_filename)

if __name__ == "__main__":
    main()