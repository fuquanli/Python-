from html.parser import HTMLParser
from urllib import request

class TestHTMLParser(HTMLParser):
    flag = 0
    res = []
    is_get_data = 0

    def handle_starttag(self, tag, attrs):
        if tag == "ul" and attrs[0][1] == "list-recent-events menu":
            self.flag = 1
        
        if tag == "a" and self.flag == 1:
            self.is_get_data = 'title'

        if tag == "time" and self.flag == 1:
            self.is_get_data = 'time'

        if tag == "span" and self.flag == 1:
            self.is_get_data = "address"

    def handle_data(self, data):
        if self.is_get_data and self.flag == 1:
            if self.is_get_data == 'title':
                self.res.append({self.is_get_data:data})
            else:
                self.res[len(self.res)-1][self.is_get_data] = data
            self.is_get_data = None

    def handle_endtag(self, tag):
        if self.flag == 1 and tag == "ul":
            self.flag = 0

parser = TestHTMLParser()
html = ""
with request.urlopen("https://www.python.org/events/python-events/") as r:
    html = r.read().decode('utf-8')
parser.feed(html)
for item in TestHTMLParser.res:
    print('-------------------')
    for k, v in item.items():
        print("%s : %s" % (k, v))
