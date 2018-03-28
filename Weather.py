from xml.parsers.expat import ParserCreate
from urllib import request

dic = {}
forecast = []

class DefaultSaxHandler(object):
    def start_element(self, name, attrs):
        if name == 'yweather:location':
            dic["city"] = attrs["city"]
        if name == 'yweather:forecast':
            daydata = {"date":attrs["date"],"high":attrs["high"],"low":attrs["low"]}
            forecast.append(daydata)

if __name__=='__main__':
    url = "https://query.yahooapis.com/v1/public/yql?q=select%20*%20from%20weather.forecast%20where%20woeid%20%3D%202151330&format=xml"
    req = request.Request(url)
    xml = ""
    with request.urlopen(req) as r:
        print('Status:%s' % r.status, r.reason)
        xml = r.read().decode('utf-8')
    handler = DefaultSaxHandler()
    parser = ParserCreate()
    parser.StartElementHandler = handler.start_element
    parser.Parse(xml)
    dic["forecast"] = forecast
    print(dic)