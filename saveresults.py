import csv

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