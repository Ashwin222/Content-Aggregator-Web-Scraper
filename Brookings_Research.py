from bs4 import BeautifulSoup
import requests
import sqlite3


def Brookings_Research():
    connection = sqlite3.connect('articles.db')
    cursor = connection.cursor()

    command1 = """CREATE TABLE IF NOT EXISTS
    articles(title TEXT, link TEXT, date TEXT, source TEXT)"""
    cursor.execute(command1)

    # HTML From Website
    # we are web scrapign the Research sit of AQR Capital
    url = "https://www.brookings.edu/project/artificial-intelligence-and-emerging-technology-initiative/?type=research"
    result = requests.get(url)
    doc = BeautifulSoup(result.text, "html.parser")
    # this is the main div that holds each article on the main page

    # finds the div that contains the title and link for IT Security Guru articles
    tags = doc.find_all("div", class_="article-info")

    for x in range(0, len(tags)):

        article = tags[x]
        article = str(article)
        article = article.split("href")
        link = article[1]
        link = link.split('">')
        title = link[1]
        link = link[0]
        date = article[len(article) - 1]

        title = title.replace("\n", "")
        title = title.replace("\t", "")
        title = title[:-25]

        link = link[2:]

        date = date.replace("\n", "")
        date = date.replace("\t", "")
        date = date[:-19]
        date = date.split("<time>")
        date = date[1]

        title = title.replace("'", "")
        title = title.replace('"', '')

        source = "Brookings Research"

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




