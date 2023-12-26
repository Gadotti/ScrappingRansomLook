import json
import os

def get_config(config_name):
    config_file_path = 'config/appconfig.json'

    try:
        with open(config_file_path, 'r', encoding='utf-8') as file:
            config_data = json.load(file)
            return config_data.get(config_name)
    except FileNotFoundError:
        print(f"O arquivo de configuração '{config_file_path}' não foi encontrado.")
    except json.JSONDecodeError:
        print(f"Erro ao decodificar o arquivo de configuração '{config_file_path}'. Verifique o formato JSON.")
