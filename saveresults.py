import csv
import os
from log import *
from datetime import datetime, timezone

CSVFILE = 'source/breachs_posts.csv'
NUM_LINES_TO_CHECK = 100

def is_new_record(postline):
    try:
        with open(CSVFILE, 'r', newline='', encoding='utf-8') as file:
            csvreader = csv.reader(file, delimiter=';')
            existinglines = [tuple(line[:3]) for line in csvreader if csvreader.line_num > csvreader.line_num - NUM_LINES_TO_CHECK]
    except FileNotFoundError:
        with open(CSVFILE, 'w', newline='', encoding='utf-8') as file:
            csvwriter = csv.writer(file, delimiter=';')
            csvwriter.writerow(['date', 'victim', 'group', 'matchingtags'])
        existinglines = []

    compareline = (
        postline.dateString, 
        postline.victim, 
        postline.group
        )
    
    return compareline not in existinglines

def save_result(postline):
    newline = (
        postline.dateString, 
        postline.victim, 
        postline.group, 
        postline.matchingtags
        )
    with open(CSVFILE, 'a', newline='', encoding='utf-8') as file:
        csvwriter = csv.writer(file, delimiter=';')
        csvwriter.writerow(newline)

def save_result_siem(postline, filepath):
    try:
        # Converte postline.dateString para timestamp no formato ISO 8601 UTC
        timestamp = convert_to_timestamp_iso(postline.dateString)
        event = postline.victim
        details_url = "https://www.ransomlook.io/recent"

        file_exists = os.path.exists(filepath)

        with open(filepath, 'a', newline='', encoding='utf-8') as file:
            writer = csv.writer(file, quoting=csv.QUOTE_ALL)
            
            # Escreve cabeçalho se o arquivo ainda não existir
            if not file_exists:
                writer.writerow(['timestamp', 'event', 'detailsUrl'])

            writer.writerow([
                timestamp,
                event,
                details_url
            ])
    except Exception as error:
        error_message = str(error)
        log_event(error_message)

def convert_to_timestamp_iso(data_str):
    try:
        # Converte a data string em um objeto datetime (sem hora)
        data_base = datetime.strptime(data_str, '%Y-%m-%d').date()
        
        # Obtém a hora atual em UTC
        hora_atual_utc = datetime.now(timezone.utc).time()
        
        # Combina a data fornecida com a hora atual em UTC
        data_hora_completa = datetime.combine(data_base, hora_atual_utc).replace(tzinfo=timezone.utc)

        # Retorna no formato ISO 8601 com 'Z' indicando UTC
        return data_hora_completa.strftime('%Y-%m-%dT%H:%M:%SZ')
    
    except ValueError as e:
        return f"Erro ao converter data: {e}"