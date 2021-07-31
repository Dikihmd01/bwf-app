import requests

from bs4 import BeautifulSoup
from flask import Flask, render_template
from flask_restful import Resource, Api, reqparse
from urllib import parse

app             = Flask(__name__)
api             = Api(app)

class BwfRank(Resource):
    @app.route('/')
    def index():
        return render_template('index.html')
    
    def get(self):
        parser    = reqparse.RequestParser()
        parser.add_argument('term', help='Bwf rank term needs to be provided')
        args      = parser.parse_args()

        BwfRankTerm = parse.urlencode({'term': args.term})

        page      = requests.get(f'https://bwfbadminton.com/rankings/?{BwfRankTerm}')
        soup      = BeautifulSoup(page.content, 'html.parser')

        
        results = []

        for list in soup.select('table > tbody > tr'):
            if 'class' in list.attrs:
                if 'row1' in list.attrs['class']:
                    rank    = list.select('td')[0].text
                    country = list.select('td > div.country > span')[0].text
                    player  = list.select('td > div.player > span > a.tooltip')[0].text
                    change  = list.select('td.mobile > span.ranking-change')[0].text
                    wl      = list.select('td')[4].text
                    prize   = list.select('td')[5].text
                    pts     = list.select('td.point > strong')[0].text
                    info    = {
                            "id": rank.strip(),
                            "rank": rank.strip(),
                            "country": country.strip(),
                            "player": player.strip(),
                            "change": change.strip(),
                            "win_lose": wl.strip(),
                            "prize_money": prize.strip(),
                            "point": pts.strip()
                        }
                    
                    results.append(info)
            else:
                rank    = list.select('td')[0].text
                country = list.select('td > div.country > span')[0].text
                player  = list.select('td > div.player > span > a.tooltip')[0].text
                change  = list.select('td.mobile > span.ranking-change')[0].text
                wl      = list.select('td')[4].text
                prize   = list.select('td')[5].text
                pts     = list.select('td.point > strong')[0].text
                info    = {
                        "id": rank.strip(),
                        "rank": rank.strip(),
                        "country": country.strip(),
                        "player": player.strip(),
                        "change": change.strip(),
                        "win_lose": wl.strip(),
                        "prize_money": prize.strip(),
                        "point": pts.strip()
                    }
                
                results.append(info)
                
        return results

api.add_resource(BwfRank, '/api/bwf_rank')

if __name__ == '__main__':
    app.run(debug=True)
