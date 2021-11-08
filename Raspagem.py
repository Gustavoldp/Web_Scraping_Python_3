from functools import partial
from os import write
from bs4 import BeautifulSoup as bs
import requests
import pandas as pd

equipe_2020_1 = []
youtube_2020_1 = []
git_2020_1 = []

equipe_2020_2 = []
youtube_2020_2 = []
git_2020_2 = []

equipe_2021_1 = []
youtube_2021_1 = []
git_2021_1 = []

source = "https://fatecsjc-prd.azurewebsites.net/api/"

url = "https://fatecsjc-prd.azurewebsites.net/api/turmas.php"
html = requests.get(url).text
sopa = bs(html, "html.parser")
semestres = sopa.findAll("a")


url = source + semestres[0].attrs["href"]
html = requests.get(url).text
sopa = bs(html, "html.parser")
turmas = sopa.findAll("a")

for t in turmas:
    u = source + "2020-1/" + t.attrs["href"]
    html = requests.get(u).text
    sopa = bs(html, "html.parser")
    equipes = sopa.findAll("a")
    for e in equipes:
        youtube = e.attrs["href"]
        equipe_2020_1.append([e.text, t.text])
        youtube_2020_1.append([youtube])
caso = "não possue"
for git in youtube_2020_1:
    if not git[0].startswith("https://"):
        git[0] = "https://" + git[0]
    html = requests.get(git[0]).text
    ini = html.find(r"https://github.com")
    if ini != -1:
        fim = ini
        while html[fim] != "\\" and html[fim] != '"':
            fim = fim + 1
        git_2020_1.append(html[ini:fim])
    else:
        git_2020_1.append(caso)


for s in semestres[1:2]:
    print("Processando semestre...")
    sem = s.text.split("/")[0]  # separa antes da barra
    sem = sem.split()[1]  # "Turmas 2020-2" pega a 2a parte
    url = source + s.attrs["href"]
    html = requests.get(url).text
    sopa = bs(html, "html.parser")
    trs = sopa.findAll("tr", {"class": "hidden"})
    for tr in trs:
        tds = tr.findAll("td")
        if len(tds) >= 3:  # tem tabela sem todas as infos
            youtube_2020_2.append(tds[2].text)
            equipe_2020_2.append([tr["id"], tds[1].text, sem])
c = 0
while c <= len(youtube_2020_2) - 1:
    a = youtube_2020_2[c]
    if not a.startswith("https://"):
        a = "https://" + a
    html = requests.get(a).text
    ini = html.find(r"https://github.com")
    if ini != -1:
        fim = ini
        while html[fim] != "\\" and html[fim] != '"':
            fim = fim + 1
        git_2020_2.append(html[ini:fim])
    else:
        git_2020_2.append(caso)
    c = c + 1


for s in semestres[2:]:
    print("Processando semestre...")
    sem = s.text.split("/")[0]  # separa antes da barra
    sem = sem.split()[1]  # "Turmas 2020-2" pega a 2a parte
    url = source + s.attrs["href"]
    html = requests.get(url).text
    sopa = bs(html, "html.parser")
    trs = sopa.findAll("tr", {"class": "hidden"})
    for tr in trs:
        tds = tr.findAll("td")
        if len(tds) >= 3:  # tem tabela sem todas as infos
            youtube_2021_1.append(tds[2].text)
            equipe_2021_1.append([tr["id"], tds[1].text, sem])
c = 0
while c <= len(youtube_2021_1) - 1:
    a = youtube_2021_1[c]
    if not a.startswith("https://"):
        a = "https://" + a
    html = requests.get(a).text
    ini = html.find(r"https://github.com")
    if ini != -1:
        fim = ini
        while html[fim] != "\\" and html[fim] != '"':
            fim = fim + 1
        git_2021_1.append(html[ini:fim])
    else:
        git_2021_1.append(caso)
    c = c + 1


df = pd.DataFrame(
    {
        "Equipes": equipe_2020_1,
        "Youtube": youtube_2020_1,
        "Github": git_2020_1,
    },
)
df.to_csv("Api2020-1.csv", index=False)

df = pd.DataFrame(
    {
        "Equipes": equipe_2020_2,
        "Youtube": youtube_2020_2,
        "Github": git_2020_2,
    },
)
df.to_csv("Api2020-2.csv", index=False)

df = pd.DataFrame(
    {
        "Equipes": equipe_2021_1,
        "Youtube": youtube_2021_1,
        "Github": git_2021_1,
    },
)
df.to_csv("Api2021-1.csv", index=False)
