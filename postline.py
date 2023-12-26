from bs4 import BeautifulSoup
from datetime import datetime
    
class PostLine:
    def __init__(self):
        self.date = None
        self.dateString = None
        self.victim = None
        self.group = None
        self.matchingtags = None

    def process_line(self, line):
        columns = line.find_all('td')
        try:
            self.date = datetime.strptime(columns[0].get_text().strip(), "%Y-%m-%d")
        finally:
            self.dateString = columns[0].get_text().strip()
        self.victim = columns[1].get_text().strip()
        self.group = columns[2].get_text().strip()
