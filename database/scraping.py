import zipfile
import requests
from bs4 import BeautifulSoup
import os

URL_1 = "https://dadosabertos.ans.gov.br/FTP/PDA/demonstracoes_contabeis/"
URL_2 = "https://dadosabertos.ans.gov.br/FTP/PDA/operadoras_de_plano_de_saude_ativas/"
DOWNLOAD_DIR = "output/downloads"

os.makedirs(DOWNLOAD_DIR, exist_ok=True)

def baixar_demonstracoes_contabeis():
    response = requests.get(URL_1)
    if response.status_code != 200:
        print("Erro ao acessar a página:", response.status_code)
        exit()

    soup = BeautifulSoup(response.text, "html.parser")
    links = [a["href"].strip("/") for a in soup.find_all("a", href=True)]

    pastas = [int(link) for link in links if link.isdigit() and len(link) == 4]
    pastas_download = sorted(pastas, reverse=True)[:2]

    if not pastas_download:
        print("Nenhum ano válido encontrado!")
        exit()

    for pasta in pastas_download:
        pasta_url = f"{URL_1}{pasta}/"
        
        print(f"\nAcessando {pasta_url}...")
        response = requests.get(pasta_url)
        if response.status_code != 200:
            print(f"Erro ao acessar a pasta {pasta}")
            continue

        soup = BeautifulSoup(response.text, "html.parser")
        arquivos = [a["href"] for a in soup.find_all("a", href=True) if a["href"].endswith(".zip")]

        ano_dir = os.path.join(DOWNLOAD_DIR, str(pasta))
        os.makedirs(ano_dir, exist_ok=True)

        for arquivo in arquivos:
            arquivo_url = f"{pasta_url}{arquivo}"
            arquivo_path = os.path.join(ano_dir, arquivo)

            print(f"Baixando {arquivo}...")
            with requests.get(arquivo_url, stream=True) as r:
                with open(arquivo_path, "wb") as f:
                    for chunk in r.iter_content(chunk_size=8192):
                        f.write(chunk)
                        
            with zipfile.ZipFile(arquivo_path, 'r') as zip_ref:
                zip_ref.extractall(ano_dir)

            os.remove(arquivo_path)  

def baixar_operadoras_ativas():
    response = requests.get(URL_2)
    if response.status_code != 200:
        print("Erro ao acessar a página:", response.status_code)
        exit()

    soup = BeautifulSoup(response.text, "html.parser")

    arquivo_url = [a["href"] for a in soup.find_all("a", href=True) if "Relatorio_cadop.csv" in a["href"]]

    if not arquivo_url:
        print("Nenhum arquivo 'Relatorio_cadop.csv' encontrado!")
        exit()

    arquivo_url_completo = arquivo_url[0] 
    if not arquivo_url_completo.startswith("http"):

        arquivo_url_completo = URL_2 + arquivo_url_completo

    arquivo_nome = arquivo_url_completo.split("/")[-1]  

    arquivo_path = os.path.join(DOWNLOAD_DIR, arquivo_nome)

    print(f"\nBaixando {arquivo_nome}...")
    with requests.get(arquivo_url_completo, stream=True) as r:
        with open(arquivo_path, "wb") as f:
            for chunk in r.iter_content(chunk_size=8192):
                f.write(chunk)

def main():
    baixar_demonstracoes_contabeis()
    baixar_operadoras_ativas()
    print("Download concluído!")

if __name__ == "__main__":
    main()
