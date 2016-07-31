from urllib.request import Request, urlopen

class BClient:    
    def fetchURL(self, url):
        try:
            req = Request(url, headers={'User-Agent': 'Mozilla/5.0'})                  
            response = urlopen(req).read()
            urlstring = response.decode('utf-8')            
            return urlstring
        except Exception as e:
            raise            