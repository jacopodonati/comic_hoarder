from datetime import datetime, timedelta
from lxml import html
import os, random, requests, sys, time, urllib

starting_year = 1992
starting_month = 1
starting_day = 1

finishing_year = 1992
finishing_month = 1
finishing_day = 3

starting_date = datetime(starting_year, starting_month, starting_day)
finishing_date = datetime(finishing_year, finishing_month, finishing_day)
delta = finishing_date - starting_date

url = 'http://dilbert.com/strip/'
headers = { 'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11' }

print("Downloading Dilbert from %s to %s" % ( starting_date.strftime("%B %d, %Y"), finishing_date.strftime("%B %d, %Y")))

for i in range(delta.days + 1):
    current_date = starting_date + timedelta(days=i)
    date_string_url = current_date.strftime("%Y-%m-%d")
    date_string_file = current_date.strftime("./%Y/%m/%Y-%m-%d.gif")
    try:
        page = requests.get(url + date_string_url, headers=headers)
    except requests.exceptions.RequestException as e:
        print(e)
        sys.exit(1)
    tree = html.fromstring(page.content)
    img = tree.xpath('//img[contains(@class, "img-comic")]/@src')
    
    print("Downloading %s: %s" % (current_date.strftime("%B %d, %Y"),date_string_file))
    img_file = urllib.request.urlopen(img[-1])
    if not os.path.exists(os.path.dirname(date_string_file)):
        try:
            os.makedirs(os.path.dirname(date_string_file))
        except OSError as exc: # Guard against race condition
            if exc.errno != errno.EEXIST:
                raise
    output = open(date_string_file, "wb")
    output.write(img_file.read())
    output.close()
    pause = random.randrange(1,5)
    print("Waiting %ds" % (pause))
    time.sleep(random.randrange(1,5))

print("Done.")
