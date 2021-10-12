import requests
from bs4 import BeautifulSoup
from lxml import html


def league_scrapper():
    r = requests.get("http://www.siatka-lodzkie.org/_em.html")
    c = r.content
    soup = BeautifulSoup(c, "html.parser")

    tables = (soup.findAll("table"))

    cont = set()

    for table in tables:
        iframe = table.find("iframe")
        if iframe is not None:
            cont.add(iframe)

    cont = str(cont).replace("{", "").replace("}", "")

    tree = html.fromstring(cont)
    link = tree.get('src')

    r2 = requests.get(link)
    c2 = r2.content
    soup = BeautifulSoup(c2, "html.parser")

    results = soup.find(id="wrapper")
    rounds = results.find_all("div", class_="collapse")

    games = []

    for r in rounds:
        game = r.find_all("h5", class_="card-title")
        info = r.find_all("p", class_="card-text")
        score = r.find_all("p", class_="card-footer")

        sets = [y for x, y in enumerate(score) if x % 2 != 1]
        pnts = [y for x, y in enumerate(score) if x % 2 == 1]

        for (g, i, s, p) in zip(game, info, sets, pnts):
            if 'Dream Team' in g.text:
                # print(f"{g.text}\n{i.text}\n{s.text}\n{p.text}" + "\n" * 2)
                games.append({"game": g.text, "info": i.text, "sets": s.text, "points": p.text})

    return games
