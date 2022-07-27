from bs4 import BeautifulSoup
import requests
import sqlite3

def CIO():
    connection = sqlite3.connect('articles.db')
    cursor = connection.cursor()

    command1 = """CREATE TABLE IF NOT EXISTS
    articles(title TEXT, link TEXT, date TEXT, source TEXT)"""
    cursor.execute(command1)

    # HTML From Website
    # we are web scrapign the Research sit of AQR Capital
    url = "https://www.cio.com/analytics/"
    result = requests.get(url)
    doc = BeautifulSoup(result.text, "html.parser")
    # this is the main div that holds each article on the main page

    # finds the div that contains the title and link for IT Security Guru articles
    tags = doc.find_all("div", class_="articleFeed-inner articleFeed-20")

    tags = str(tags)
    tags = tags.split("\n")
    tags = tags[0]
    tags = tags.split("Article:")
    tags.remove(tags[0])
    # print(tags)

    for x in range(0, len(tags)):
        article = tags[x]
        article = article.split("href=")
        title = article[0]
        link = article[1]
        date = article[2]

        link = link.split("target")
        link = link[0]
        link = link[:-2]
        link = link[1:]

        title = title.split("class=")
        title = title[0]
        title = title[:-2]
        title = title[1:]

        date = date.split("item-date")
        date = date[1]
        date = date.replace("\n", "")
        date = date.replace("\t", "")
        date = date[:-62]
        date = date[2:]

        source = "CIO.com"

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

    # cursor.execute("DROP TABLE articles")
    # connection.commit()
    # cursor.execute("SELECT * FROM articles")
    # results = cursor.fetchall()
    # for x in results:
    #   print(x)
    connection.close()





