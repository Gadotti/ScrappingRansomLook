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
        # Usa o datetime completo do post quando disponível
        date_source = getattr(postline, 'dateTimeFull', None) or postline.dateString
        timestamp = convert_to_timestamp_iso(date_source)
        event = postline.victim
        details_url = "https://www.ransomlook.io/recent"

        file_exists = os.path.exists(filepath)

        with open(filepath, 'a', newline='', encoding='utf-8') as file:
            writer = csv.writer(file, quoting=csv.QUOTE_ALL, delimiter=';')
            
            # Escreve cabeçalho se o arquivo ainda não existir
            if not file_exists:
                writer.writerow(['timestamp', 'event', 'detailsUrl'])

            # # Garante que o ponteiro esteja no final para ler último caractere
            # file.seek(0, os.SEEK_END)
            # if file.tell() > 0:
            #     file.seek(file.tell() - 1, os.SEEK_SET)
            #     last_char = file.read(1)
            #     if last_char != '\n':
            #         file.write('\n')

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
        for fmt in ('%Y-%m-%d %H:%M:%S', '%Y-%m-%d'):
            try:
                dt = datetime.strptime(data_str, fmt).replace(tzinfo=timezone.utc)
                return dt.strftime('%Y-%m-%dT%H:%M:%SZ')
            except ValueError:
                continue
        return f"Erro ao converter data: formato inválido '{data_str}'"
    except Exception as e:
        return f"Erro ao converter data: {e}"