from datetime import datetime, date

class PostLine:
    def __init__(self):
        self.date = None
        self.dateString = None
        self.dateTimeFull = None
        self.victim = None
        self.group = None
        self.matchingtags = None

    def process_line(self, line):
        columns = line.find_all('td')

        # Date: read from <time datetime="..."> attribute; fall back to today
        time_tag = columns[0].find('time')
        datetime_attr = (time_tag.get('datetime') or '').strip() if time_tag else ''

        dt = None
        for fmt in ('%Y-%m-%d %H:%M:%S.%f', '%Y-%m-%d %H:%M:%S', '%Y-%m-%d'):
            try:
                dt = datetime.strptime(datetime_attr, fmt)
                break
            except ValueError:
                continue

        if dt is None:
            dt = datetime.now()

        self.date = dt.date()
        self.dateString = dt.strftime('%Y-%m-%d')
        self.dateTimeFull = dt.strftime('%Y-%m-%d %H:%M:%S')

        # Victim
        self.victim = columns[1].get_text().strip()

        # Group: find the non-empty <span> inside the group link
        self.group = None
        group_link = columns[2].find('a', class_='recent-group-link')
        if group_link:
            for span in group_link.find_all('span'):
                text = span.get_text().strip()
                if text:
                    self.group = text
                    break
        if not self.group:
            self.group = columns[2].get_text().strip()
