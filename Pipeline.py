#%%
import json 
import os 
import requests
import pandas 
import psycopg2
from sqlalchemy import create_engine

#Pega a chave no .env
api_key =os.getenv('API_KEY')
city = os.getenv('city')

#Conectando ao PostgreSQL
db_user = os.getenv('db_username')
db_password = os.getenv('db_password')
db_host = os.getenv('db_host')
db_port = os.getenv('db_port')
db_name = os.getenv('db_name')

#url para trazer os dados
url = f"http://api.weatherapi.com/v1/forecast.json?key={api_key}&q={city}&days=5&lang=pt"

#Faz a requisição e trata os dados
response = requests.get(url)
if response.status_code == 200:
    data = response.json()
    json_str=json.dumps(data)
    print(json_str)
    weather_data = [ ]

#%%
#Tratando os dados

# Criando um dataframe com os dados
for i in range(0, len(data['forecast']['forecastday'][0]['hour']), 3):
        hour = data['forecast']['forecastday'][0]['hour'][i]

        date_time = hour["time"]# Data e hora
        temp = hour["temp_c"]# temperatura
        pressure = hour["pressure_mb"]# pressão atmosferica
        humidity = hour["humidity"]# Umidade
        weather_main = hour["condition"]["text"]# clima
        wind_speed = hour["wind_kph"]# velocidade do vento
        cloudiness = hour["cloud"]# qtd de nuvens
        rain_volume = hour.get("precip_mm", 0)# Quantidade de chuva em mm
        city = data["location"]["name"]# cidade
        state = data["location"] ["region"]# estado
        country = data["location"]["country"]# pais

        # Adicionando dados à lista de dados
        weather_data.append({
            "Data_Hora": date_time,
            "Temperatura": temp,
            "Pressao": pressure,
            "Umidade": humidity,
            "Clima": weather_main,
            "Velocidade_Vento": wind_speed,
            "Nuvens": cloudiness,
            "Volume_Chuva": rain_volume,
            "Cidade": city,
            "Estado": state,
            "Pais": country,
        })

        df = pandas.DataFrame(weather_data)
        print(f'Dados Tratados')
        print(df)
else:
    print(f"Erro ao pegar os dados:{response.status_code}")

# Mostrando as primeiras linhas do Df
df.head(100)

#%%
#Cerregando os dados do BD

# Criando engine de conexão com PostgreSQL
engine = create_engine(f'postgresql://{db_user}:{db_password}@{db_host}:{db_port}/{db_name}')

#Criar a tabela
table_name = 'weather'

# Coloca os dados no Banco de dados
df.to_sql(table_name, engine, if_exists='replace', index = False)

engine.dispose()

