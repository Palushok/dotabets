import requests
import bs4

HEADERS = {
    'authority': 'www.joindota.com',
    'cache-control': 'max-age=0',
    'sec-ch-ua': '"Chromium";v="92", " Not A;Brand";v="99", "Google Chrome";v="92"',
    'sec-ch-ua-mobile': '?0',
    'upgrade-insecure-requests': '1',
    'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.159 Safari/537.36',
    'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
    'sec-fetch-site': 'same-origin',
    'sec-fetch-mode': 'navigate',
    'sec-fetch-user': '?1',
    'sec-fetch-dest': 'document',
    'referer': 'https://www.joindota.com/matches/468283-infamous-vs-unknown',
    'accept-language': 'ru,en-US;q=0.9,en;q=0.8,ru-RU;q=0.7',
    'cookie': 'PHPSESSID=9be459cb04bb5b20d3513cd714c53504',
}


def get_response(href):
    return requests.get(href, headers=HEADERS)


def get_teams(page):
    countries = [div.text for div in page.find_all('div', {'class': 'txt-subtitle'})[2:]]
    teams = [team.text for team in page.find_all('h2')[:2]]
    return [{'team': team, 'county': country} for team, country in zip(teams, countries)]


def get_match(response):
    soup = bs4.BeautifulSoup(response.text, features="html.parser")
    return {
        'teams': get_teams(soup),
        'maps': get_maps(soup),
        'location': get_location(soup)
    }


def get_location(page):
    icons = page.find('ul', {'class':'widget-icon-info widget-icon-info-50'}).find_all('li')
    for li in icons:
        if li.find('i', {'class': 'icon-location'}):
            return li.text.split(':')[1]


def get_maps(page):
    maps = []
    maps_soup = page.find_all("div", {"class": "content-match-sub-heroes"})
    for map_soup in maps_soup:
        maps.append({
            'bans': get_heroes(map_soup, stage='ban'),
            'picks': get_heroes(map_soup),
            'winner': get_winner(map_soup),
        }) 
    return maps


def get_winner(map_page):
    for i, team in enumerate(map_page.find_all("h3")):
        icon = team.find('i')
        if icon:
            return i

        
def get_heroes(page, stage='pick'):
    picks = {0: [], 1: []}
    picks_soup = page.find_all("ul", {"class": f"content-match-sub-{stage}s"})
    for side in range(len(picks_soup)):
        all_picks = picks_soup[side].find_all('img')
        for b in all_picks:
            picks[side].append(b['title'])
    return picks
