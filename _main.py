import os
import requests
from bs4 import BeautifulSoup
from postline import PostLine
from saveresults import *
from config import *
from notify import *
import schedule
import time
import sys

def main():
    if len(sys.argv) > 1:
        arg = sys.argv[1]
        print("Argument:", arg)
        if sys.argv[1] == 'schedule':    
          print("-- A schedule will be running --")
          log_event('-- A schedule will be running --')
          schedule_main()

          while True:
              schedule.run_pending()
              time.sleep(60)  # 1 min

    check_new_posts()    

def schedule_main():
    schedule_times = get_config('schedule_times')

    for scheduled_time in schedule_times:
        schedule.every().day.at(scheduled_time).do(check_new_posts)

def check_new_posts():
    try:
        print('-- Start --')
        log_event('-- Starting verification --')

        url = get_config('url')
        siem_log_all = get_config('siem_breach_log_all')
        siem_log_tag = get_config('siem_breach_log_tag')
        if url is None:
            print("An 'url' setting configuration in apconfig.json is needed")
            exit()
        
        print(url)

        lines = get_post_lines(url)

        notify_messages = []

        for line in reversed(lines):
            postline = PostLine()
            postline.process_line(line)

            if not is_new_record(postline):
                continue

            print("Date:", postline.date)
            print("Victim:", postline.victim.encode("utf-8"))
            print("Group:", postline.group.encode("utf-8"))

            matchingtags = check_matching_tags(postline)
            if (matchingtags is not None):
                postline.matchingtags = matchingtags
                message = f'{postline.dateString} | {postline.victim} | {postline.group} | Tags: {matchingtags}'
                notify_messages.append(message)

                if (siem_log_tag != ''):
                    save_result_siem(postline, siem_log_tag)
            
            log_post_found(postline)
            save_result(postline)
            if (siem_log_all != ''):
                save_result_siem(postline, siem_log_all)
            print("")

        notify(notify_messages)    
            
        log_event('-- End verification --')
        print('-- End --')

    except Exception as error:
        error_message = str(error)
        log_event(error_message)

def get_post_lines(url):
    response = requests.get(url)
    html_content = response.content

    soup = BeautifulSoup(html_content, 'html.parser')
    tbody = soup.find_all('tbody')
    return tbody[0].find_all('tr')

main()
