from bs4 import BeautifulSoup
import requests
import sqlite3

def Gartner_Research():
    connection = sqlite3.connect('articles.db')
    cursor = connection.cursor()

    command1 = """CREATE TABLE IF NOT EXISTS
    articles(title TEXT, link TEXT, date TEXT, source TEXT)"""
    cursor.execute(command1)

    # HTML From Website
    # we are web scrapign the Research sit of AQR Capital
    url = "https://www.gartner.com/en/information-technology/research/research-index"
    result = requests.get(url)
    doc = BeautifulSoup(result.text, "html.parser")
    # this is the main div that holds each article on the main page

    # finds the div that contains the title and link for IT Security Guru articles
    tags = doc.find_all("div", class_="individual-block tile col-md-4 col-sm-6 col-xs-12 page-1")

    for x in range(0, len(tags)):
        article = tags[x]
        article = str(article)

        article = article.split("href=")

        link = article[2]

        link = link.split('val="title"')
        title = link[1]

        link = link[0]
        link = link.split('<div class="tag-xs visible')
        link = link[0]

        link = link[:-3]
        link = link[1:]
        link = "gartner.com" + link

        title = title.split("</h4>")
        title = title[0]
        title = title[1:]

        date = "2022"

        source = "Gartner Research"

        title = title.replace("'", "")
        title = title.replace('"', '')

        # this is to prevent duplicate articles. Check to see if article with same title is already in db
        cursor.execute("SELECT * FROM articles WHERE title = '" + title + "'")
        results = cursor.fetchall()
        if len(results) > 0:
            continue

        cursor.execute("INSERT INTO articles VALUES('" + title + "', '" + link + "', '" + date + "', '" + source + "')")
        # commit so that it saves
        connection.commit()

    #cursor.execute("DROP TABLE articles")
    #connection.commit()
    # cursor.execute("SELECT * FROM articles")
    # results = cursor.fetchall()
    # for x in results:
    #   print(x)
    connection.close()






