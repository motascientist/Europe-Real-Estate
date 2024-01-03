'''Importing Libraries'''

import pandas as pd # Manipulate Dataset
from urllib.parse import urlparse
import os

'''Concatenating the data'''
# Diretctory where .csv is located
diretorio = '.'

# List to store dataframes
dataframes = []

# Loop pelos arquivos no diretório
for arquivo in os.listdir(diretorio):
    if arquivo.endswith('.csv'):
        caminho_arquivo = os.path.join(diretorio, arquivo)
        df = pd.read_csv(caminho_arquivo)
        dataframes.append(df)

# Concatenar os DataFrames
concatenated_df = pd.concat(dataframes, ignore_index=True)

# Salvar o DataFrame resultante em um novo arquivo CSV
concatenated_df.to_csv('concatenated_data.csv', index=False)

# Reading Dataset
df = pd.read_csv('concatenated_data.csv')
'''Extracting the id throw url'''
# Função para extrair o último número da URL
def extract_house_id(url):
    parsed_url = urlparse(url)
    path_segments = parsed_url.path.split('/')
    for segment in reversed(path_segments):
        if segment.isdigit():
            return int(segment)
    return None

# Aplicar a função à coluna 'links' para criar a coluna 'house_id'
df['house_id'] = df['links'].apply(extract_house_id)

# Assuming df is your DataFrame
df.drop_duplicates(subset=['day', 'house_id'], keep='first', inplace=True)

# If you want to reset the index after removing duplicates
df.reset_index(drop=True, inplace=True)

''' Room Treatment '''
def transform_rooms(value):
    if isinstance(value, str):
        if '+' in value:
            return int(value[:-1])  # Remove the '+' and convert to integer
        elif '-' in value:
            # Extract the last number in the range
            return int(value.split('-')[-1])
        else:
            return int(value)
    else:
        # If the value is not a string, return it as is
        return value

# Applying the function to the 'rooms' column
df['rooms'] = df['rooms'].apply(transform_rooms)

'''m² Treatment'''

def remove_square_meter(value):
    # Check if the value is a string
    if isinstance(value, str):
        # Remove "m²" and return the cleaned string
        return value.replace('m²', '').strip()
    else:
        # If the value is not a string (e.g., it's a float), return it as is
        return value

# Applying the function to the 'm2' column
df['m2'] = df['m2'].apply(remove_square_meter)
      
'''Bathroom Treatment'''
def transform_bathrooms(value):
    # Check if the value is a string
    if isinstance(value, str):
        # Remove "+" and convert to integer
        if '+' in value:
            return int(value.replace('+', '').strip())
        # Remove "G" and convert to integer
        elif 'G' in value:
            return None  # Returning None will effectively remove the line
        else:
            return int(value)
    else:
        # If the value is not a string (e.g., it's a float), return it as is
        return value

# Applying the function to the 'bathrooms' column
df['bathrooms'] = df['bathrooms'].apply(transform_bathrooms)

# Checking the result
print(df['bathrooms'].value_counts())

'''Price Treatment'''
import re


# Função para transformar o preço em float
# Função para transformar o preço em float
def transformar_para_float(preco_str):
    # Tratar "Price on application" como NaN
    if 'Price on application' in preco_str:
        return None

    # Extrair o primeiro valor usando regex
    match = re.search(r'€\s*([\d,]+)', preco_str)
    
    if match:
        # Remover vírgulas e converter para float
        preco_limpo = match.group(1).replace(',', '')
        try:
            preco_float = float(preco_limpo)
            return preco_float
        except ValueError:
            print(f"Erro ao converter valor: {preco_str}")
            return None
    else:
        print(f"Padrão não encontrado: {preco_str}")
        return None

# Aplicar a função à coluna 'price'
df['price'] = df['price'].apply(transformar_para_float)

df.to_csv('Processed_data.csv',index=False)