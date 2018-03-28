from html.parser import HTMLParser
import requests, re

class BlogParser(HTMLParser):
    flag = 0
    res = []
    is_get_data = 0

    def handle_starttag(self, tag, attrs):
        if tag == "div" and len(attrs) > 0:
            for attr in attrs:
                if re.match(r'post_item', attr[1]):
                    self.flag = 1
            
        if self.flag == 1 and tag == "span" and len(attrs) > 0:
            for attr in attrs:
                if re.match(r'diggnum', attr[1]):
                    self.is_get_data = '点赞数'

        if self.flag == 1 and tag == "a" and len(attrs) > 0:
            _is_url = 0
            for attr in attrs:
                if re.match(r'titlelnk', attr[1]):
                    self.is_get_data = '标题'
                    self.res.append({"网址":attrs[1][1]}) 

                if re.match(r'lightblue', attr[1]):
                    self.is_get_data = '作者'
                
            
        if self.flag == 1 and tag == "p" and len(attrs) > 0:
            for attr in attrs:
                if re.match(r'post_item_summary', attr[1]):
                    self.is_get_data = '摘要'


    def handle_data(self, data):
        if self.is_get_data and self.flag == 1:
            if len(self.res) < 1:
                self.res.append({self.is_get_data:data})
            else:
                self.res[len(self.res)-1][self.is_get_data] = data
            self.is_get_data = None

    def handle_endtag(self, tag):
        if self.flag == 1 and tag == "div":
            self.flag = 0

parser = BlogParser()
r = requests.get('https://www.cnblogs.com/') 
html = r.text
parser.feed(html)
for item in BlogParser.res:
    print('-----------------------')
    for k, v in item.items():
        print("%s : %s" % (k, v))
