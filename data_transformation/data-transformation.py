import os
import zipfile
import tabula
import pandas as pd

def mesclar_quebras(df):
    def mesclar_valores(df):

        df_limpo = df.copy()

        for col in df_limpo.columns:
            # Verificar se há valores quebrados
            df_limpo[col] = df_limpo[col].apply(lambda x: ' '.join(str(x).split()) if pd.notna(x) else x)
        
        return df_limpo
    
    def mesclar_cabecalho(df):

        if len(df.columns) > len(df.columns.unique()):

            cabecalho_linha1 = df.columns
            cabecalho_linha2 = df.iloc[0]
            
            colunas_novas = []
            for i, col in enumerate(cabecalho_linha1):

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
        
        if tabelas:
            tabelas_processadas = []
            for df in tabelas:

                df.columns = [
                    col.replace('\r', ' ').replace('/r', ' ').strip() 
                    for col in df.columns
                ]

                df_limpo = mesclar_quebras(df)
                
                df_limpo.dropna(how='all', inplace=True)
                
                df_limpo = df_limpo[
                    ~df_limpo.iloc[:, 0].str.contains('Legenda:', na=False) &
                    ~df_limpo.iloc[:, 0].str.contains('Página', na=False)
                ]
                
                tabelas_processadas.append(df_limpo)
            
            combined_df = pd.concat(tabelas_processadas, ignore_index=True)
            
            return combined_df
        
        print("Nenhuma tabela válida encontrada.")
        return None

    except Exception as e:
        print(f"Erro ao extrair dados do PDF: {e}")
        import traceback
        traceback.print_exc()
        return None

output_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'output'))

os.makedirs(output_dir, exist_ok=True)

def sub_abreviacao(df):
    abbr_map = {'OD': 'Seg. Odontológica', 'AMB': 'Seg. Ambulatorial'}
    df_atualizado = df.copy()
    df_atualizado.rename(columns=abbr_map, inplace=True)
    return df_atualizado

def salvar_csv(df, filepath):
    try:
        df.to_csv(filepath, index=False, encoding='utf-8')
        print(f"Dados salvos em {filepath}")
    except Exception as e:
        print(f"Erro ao salvar CSV: {e}")

def salvar_zip(csv_filepath, zip_filepath):
    try:
        with zipfile.ZipFile(zip_filepath , 'w', zipfile.ZIP_DEFLATED) as zipf:
            zipf.write(csv_filepath, arcname=os.path.basename(csv_filepath))
        print(f"Arquivo compactado em {zip_filepath}")
    except Exception as e:
        print(f"Erro ao compactar arquivo: {e}")

def main():
    # Caminho para o arquivo PDF dentro do ZIP do scraping anterior
    base_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'output', 'anexos.zip'))
    
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
    
    df = extrair_tabelas(pdf_filename)
    
    if df is None:
        print("Falha na extração dos dados")
        return
    
    df_updated = sub_abreviacao(df)
    
    csv_filename = f"Teste_JoaoPedro.csv"
    zip_filename = f"Teste_JoaoPedro.zip"

    csv_path = os.path.join(output_dir, csv_filename)
    zip_path = os.path.join(output_dir, zip_filename)
    
    salvar_csv(df_updated, csv_path)
    salvar_zip(csv_path, zip_path)
    
    os.remove(pdf_filename)
    os.remove(csv_path)

if __name__ == "__main__":
    main()