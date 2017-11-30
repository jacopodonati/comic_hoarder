from lxml import html
import os, random, requests, time, urllib

starting_comic = 1664
finishing_comic = 1666

url = 'http://www.xkcd.com/'
headers = { 'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11' }

print("Downloading xkcd from %d to %d" % ( starting_comic, finishing_comic))

for i in range(starting_comic, finishing_comic + 1):
    page = requests.get(url + str(i), headers=headers)
    tree = html.fromstring(page.content)
    img = tree.xpath('//div[@id="comic"]/img/@src')
    
    print("Downloading %d: %s" % (i,img[-1]))
    img_file = urllib.request.urlopen("http:" + img[-1])
    output = open(str(i) + img[-1][-4:], "wb")
    output.write(img_file.read())
    output.close()
    #pause = random.randrange(1,5)
    #print "Waiting %ds" % (pause)
    #time.sleep(random.randrange(1,5))
    #break

print("Done.")
