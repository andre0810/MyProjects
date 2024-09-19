#%%
#Importando as bibliotecas do script python
import requests
import pandas as pd

# URL da API https://apisidra.ibge.gov.br/. Aqui você pode fazer a consulta pelo numero da tabela e passar os parametros para verificar se extrai.
# Dentro dos parametros é necessário passar o número da tabela (t), a localização geografia (N), sendo N1 Brasil, N2 Regiões, N3 Unidades Federativas, 
# N24 Região Geográfica Intermediária, N25 Região Geográfica Imediata e N6 Municípios e os outros paramêtros que começam com a letra c são as colunas 
# que no caso do projeto conta com 3, sendo elas C125 Tipo de domicílio, C58 Grupo de idade e C86 Cor ou raça.
url = "https://apisidra.ibge.gov.br/values//t/6893/N3/all/c125/all/c58/all/c86/all"

# Fazendo a requisição
response = requests.get(url)

# Verificando o status da conexão com a API e configurando a resposta
if response.status_code == 200:
    dados = response.json()

    # Transformar o JSON em um DataFrame com pandas
    df = pd.json_normalize(dados, sep='_')

    # Promover a primeira linha como cabeçalho
    df.columns = df.iloc[0]  # Define a primeira linha como cabeçalho
    df = df[1:]  # Remove a primeira linha do DataFrame

    # Resetar os índices
    df.reset_index(drop=True, inplace=True)

    # Mostrar as primeiras linhas do DataFrame
    print(df.head())

    # Salvar em CSV
    df.to_csv('dados_ibge.csv', index=False)
    
else:
    print(f"Erro: {response.status_code}")



# %%
