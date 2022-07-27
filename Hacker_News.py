from bs4 import BeautifulSoup
import requests
import sqlite3


def Hacker_News():
    connection = sqlite3.connect('articles.db')
    cursor = connection.cursor()

    command1 = """CREATE TABLE IF NOT EXISTS
    articles(title TEXT, link TEXT, date TEXT, source TEXT)"""
    cursor.execute(command1)

    # HTML From Website
    # we are web scrapign the Research sit of AQR Capital
    url = "https://thehackernews.com/"
    result = requests.get(url)
    doc = BeautifulSoup(result.text, "html.parser")
    # this is the main div that holds each article on the main page

    # finds the div that contains the title and link for IT Security Guru articles

    tags = doc.find_all("a", class_="story-link")
    tags = str(tags)
    tags = tags.split("</a>")

    for x in range(0, len(tags) - 1):
        article = tags[x]
        article = article.split("clear home-post-box cf")
        link = article[0]
        article = article[1]
        article = article.split("icon-calendar")
        title = article[0]
        article = article[1]
        article = article.split("icon-font")
        date = article[0]

        link = link.split('href="')
        link = link[1]
        link = link.replace("\n", "")
        link = link.replace("\t", "")
        link = link[:-14]

        title = title.split("home-title")
        title = title[1]
        title = title.replace("\n", "")
        title = title.replace("\t", "")
        title = title[2:]
        title = title[:-49]

        date = date[7:]
        date = date[:-16]

        source = "Hacker News"

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







