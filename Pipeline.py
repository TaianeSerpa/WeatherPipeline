# %%
import json 
import os 
import requests
import pandas 
from dotenv import load_dotenv
from datetime import datetime
import matplotlib.pyplot as plt
import seaborn as sns

#Pega a chave no .env
api_key =os.getenv('API_KEY')
city = os.getenv('city')

#url para trazer os dados
url = f"http://api.weatherapi.com/v1/forecast.json?key={api_key}&q={city}&days=1&lang=pt"

#Faz a requisição e trata os dados
response = requests.get(url)
if response.status_code == 200:
    data = response.json()
    json_str=json.dumps(data)
    print(json_str)
    weather_data = [ ]

# %%
#Tratando os dados

for hour in data['forecast']['forecastday'][0]['hour']:
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
        print(df)
else:
    print(f"Erro ao pegar os dados:{response.status_code}")
df.head()

# %%

# %%
