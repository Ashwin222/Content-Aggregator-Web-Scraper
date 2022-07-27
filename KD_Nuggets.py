from bs4 import BeautifulSoup
import requests
import sqlite3


def KD_Nuggets():
    connection = sqlite3.connect('articles.db')
    cursor = connection.cursor()

    command1 = """CREATE TABLE IF NOT EXISTS
    articles(title TEXT, link TEXT, date TEXT, source TEXT)"""
    cursor.execute(command1)

    # HTML From Website
    # we are web scrapign the Research sit of AQR Capital
    url = "https://www.kdnuggets.com/"
    result = requests.get(url)
    doc = BeautifulSoup(result.text, "html.parser")
    # this is the main div that holds each article on the main page

    # finds the div that contains the title and link for IT Security Guru articles
    tags = doc.find_all("div", class_="li-has-thumb__content")
    tags = str(tags)
    articles = tags.split("li-has-thumb__content")
    articles.remove(articles[0])

    for x in range(0, len(articles)):
        a = articles[x]
        a = a.replace("\n", "")
        a = a.replace("\t", "")

        a = a.split("onclick")

        link = a[0]
        title = a[1]
        title = title.split("href")
        date = title[1]
        title = title[0]

        title = title.split("<b>")
        title = title[1]
        title = title.split(" </b>")
        title = title[0]

        link = link[11:]
        link = link[:-2]

        date = date.split("on")
        date = date[2]
        date = date[1:]
        date = date[:-6]

        source = "KD Nuggets"

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
