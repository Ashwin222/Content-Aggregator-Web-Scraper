from bs4 import BeautifulSoup
import requests
import sqlite3

def Motley_Fool():
    connection = sqlite3.connect('articles.db')
    cursor = connection.cursor()

    command1 = """CREATE TABLE IF NOT EXISTS
    articles(title TEXT, link TEXT, date TEXT, source TEXT)"""
    cursor.execute(command1)

    # HTML From Website
    # we are web scrapign the Research sit of AQR Capital
    url = "https://www.fool.com/investing-news/"
    result = requests.get(url)
    doc = BeautifulSoup(result.text, "html.parser")
    # this is the main div that holds each article on the main page

    # finds the div that contains the title and link for IT Security Guru articles
    tags = doc.find_all("div", class_="content-block promoted-articles m-np")
    tags = str(tags)
    tags = tags.split("</article>")

    for x in range(0, len(tags) - 1):

        article = tags[x]
        # print(article)
        article = article.split("h4>")
        link = article[0]
        title = article[1]
        date = article[2]

        # print(title)
        # print(date)

        link = link.split("href=")
        link = link[1]
        link = link.split("<article id")
        link = link[0]
        link = link[1:]
        link = link[:-2]
        link = "fool.com" + link
        link = link[:-1]

        title = title[:-2]
        title = title.replace("'", "")
        title = title.replace('"', '')

        date = date.split("|")
        date = date[1]
        date = date.split("<p>")
        date = date[0]
        date = date[:-6]
        date = date[1:]
        date = date[:-1]

        source = "The Motley Fool"



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






