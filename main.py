import requests
from bs4 import BeautifulSoup

date = input("input the date in format(YYYY-MM-DD)")

billboard_url = f"https://www.billboard.com/charts/hot-100/{date}"

response = requests.get(url=billboard_url)
billboard_data = response.text

soup = BeautifulSoup(billboard_data,"html.parser")

title_tags = soup.find_all(name="span",class_="chart-element__information__song")
titles = []
for title in title_tags:
    titles.append(title.getText())

print(titles)