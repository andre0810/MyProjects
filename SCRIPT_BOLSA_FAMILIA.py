#%%
import requests
import pandas as pd
import json
#%%

BASE_URL = "https://dados.gov.br/api/publico/conjuntos-dados"

def get_dataset_info(keyword="bolsa familia"):
    """
    Fetch dataset information based on a keyword search.
    """
    params = {
        "q": keyword,
        "ordem": "relevancia",
        "pagina": 1,
        "por_pagina": 10
    }
    response = requests.get(f"{BASE_URL}", params=params)
    response.raise_for_status()
    return response.json()

def get_dataset_resources(dataset_id):
    """
    Fetch resources for a specific dataset.
    """
    response = requests.get(f"{BASE_URL}/{dataset_id}/recursos")
    response.raise_for_status()
    return response.json()

def download_resource(url, filename):
    """
    Download a resource and save it to a file.
    """
    response = requests.get(url)
    response.raise_for_status()
    with open(filename, 'wb') as f:
        f.write(response.content)
    print(f"Downloaded: {filename}")

def main():
    # Search for Bolsa Familia datasets
    datasets = get_dataset_info()
    
    if datasets['count'] == 0:
        print("No datasets found for Bolsa Familia.")
        return

    # Assume the first result is the one we want
    dataset = datasets['results'][0]
    print(f"Found dataset: {dataset['titulo']}")

    # Get resources for this dataset
    resources = get_dataset_resources(dataset['id'])
    
    for resource in resources:
        print(f"Resource: {resource['titulo']}")
        if resource['formato'] == 'CSV':
            filename = f"{resource['titulo'].replace(' ', '_')}.csv"
            download_resource(resource['url'], filename)
            
            # Read and display first few rows of the CSV
            df = pd.read_csv(filename)
            print(df.head())
            print("\n")

if __name__ == "__main__":
    main()
# %%
import requests

# URL do endpoint da API
url = "https://dados.gov.br/dados/api/publico/conjuntos-dados/bolsa-familia"

# Cabeçalhos da requisição
headers = {
    'accept': 'application/json'
}

# Fazer a requisição GET para a API, sem seguir redirecionamentos
try:
    response = requests.get(url, headers=headers, allow_redirects=False)
    
    # Exibir o status da resposta
    print(f"Status Code: {response.status_code}")
    
    # Verificar se houve redirecionamento
    if 300 <= response.status_code < 400:
        print(f"Redirecionamento detectado. Novo local: {response.headers.get('Location')}")
    elif response.status_code == 200:
        # Tentar converter a resposta para JSON
        try:
            dados = response.json()
            print("Dados recebidos (primeiros 500 caracteres):")
            print(str(dados)[:500])  # Mostrar os primeiros 500 caracteres dos dados
        except ValueError as e:
            print("Erro ao converter a resposta para JSON.")
            print(response.text[:500])  # Mostrar os primeiros 500 caracteres da resposta em texto
    else:
        # Exibir o conteúdo da resposta em caso de erro
        print("Erro ao acessar a API. Detalhes:")
        print(response.text)
        
except Exception as e:
    print(f"Exceção capturada: {e}")

# %%
