import requests
import re


#https://www.cavendishonline.co.uk/investments/fund-research/
class parse:
    api_url='https://www.cavendishonline.co.uk/tools/funds.php/2/'
    req=None

    def __init__(self):
        self.req=requests.session()
        self.req.get("https://www.cavendishonline.co.uk/investments/fund-research/", headers={
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Accept-Language': 'en-US,en;q=0.8',
            'User-Agent': 'Mozilla/5.0 (X11; Linux i686) AppleWebKit/537.36 (KHTML, like Gecko) Ubuntu Chromium/52.0.2743.116 Chrome/52.0.2743.116 Safari/537.36',
        })

    def go(self):
        url='https://www.cavendishonline.co.uk/themes/Cavendish/js/fund_init.js'
        r=self.req.get(url)

        s=r.text
        r=re.match(r'var\s+fund_data\s*=\s*(\{.+\});\s*function\s+fund_init_setup',s,re.S)
        st=r.groups()[0]

        j_by_sector = re.search(r"by_sector:\{([^\}]+)\}",st,re.S).groups(list())[0]
        j_sectors=re.finditer("'([^\[]+)':\[([^\]]+)",j_by_sector,re.S)
        for x in j_sectors:
            for id in self._parse_sector_items(x.groups()[1]):
                resp=self._construct_request(self._get_item_url(id))
                print(x.groups()[0])
                print("%s: %s" % (id, resp.status_code))
                self.parse_fund(resp)
                print(resp.json())

    def _parse_sector_items(self, items_as_str):
        tmp=re.finditer("'([^']+)'",items_as_str)
        for item in tmp:
            yield item.groups()[0]
            break

    def _get_item_url(self, item):
        return self.api_url+item

    def _construct_request(self, url):
        r=self.req.get(url,headers={
            'Accept': 'application/json, text/javascript, */*',
            'User-Agent': 'Mozilla/5.0 (X11; Linux i686) AppleWebKit/537.36 (KHTML, like Gecko) Ubuntu Chromium/52.0.2743.116 Chrome/52.0.2743.116 Safari/537.36',
            'X-Requested-With': 'XMLHttpRequest'
        })
        return r

    def parse_fund(self, resp):
        pass


parser=parse()
parser.go()