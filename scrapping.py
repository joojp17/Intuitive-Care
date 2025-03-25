import requests
from bs4 import BeautifulSoup
import os
import zipfile

def scrapping_anexos_pdf():
    """
    Baixar os arquivos PDF 'Anexo_I' e 'Anexo_II' e os compactar em um ZIP.
    """
    try:
        # Acessando a página e extraindo os links dos PDFs
        pagina = requests.get('https://www.gov.br/ans/pt-br/acesso-a-informacao/participacao-da-sociedade/atualizacao-do-rol-de-procedimentos')
        
        soup = BeautifulSoup(pagina.text, 'html.parser')
        
        anexos_links = soup.find_all('a', 
            href=lambda href: href and href.endswith('.pdf') and ('Anexo_I' in href or 'Anexo_II' in href),
            class_='internal-link'
        )
        
        # Verifica se encontrou anexos
        if not anexos_links:
            print("Nenhum anexo PDF encontrado.")
            return
        
        # Inicio do download dos PDFs e a compactação em ZIP
        os.makedirs('downloads', exist_ok=True)
        
        anexos_baixados = []
        
        for link in anexos_links:
            
            pdf_url = link.get('href')

            pdf = requests.get(pdf_url)
            
            filename = os.path.join('downloads', os.path.basename(pdf_url))
            
            with open(filename, 'wb') as f:
                f.write(pdf.content)
            
            anexos_baixados.append(filename)
            print(f"Baixado: {filename}")

        with zipfile.ZipFile(os.path.join('downloads', 'anexos.zip'), 'w') as zipf:
            for file in anexos_baixados:
                zipf.write(file, os.path.basename(file))
        
        for file in anexos_baixados:
            os.remove(file)
        
        # Finalizando o processo
        print("Arquivos compactados em anexos.zip com sucesso!")
    
    #Exceções para tratamento de erros
    except requests.exceptions.RequestException as e:
        print(f"Erro na requisição: {e}")
    except Exception as e:
        print(f"Erro inesperado: {e}")

scrapping_anexos_pdf()