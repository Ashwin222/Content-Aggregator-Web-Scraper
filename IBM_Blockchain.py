from bs4 import BeautifulSoup
import requests
import sqlite3


def IBM_Blockchain():
    connection = sqlite3.connect('articles.db')
    cursor = connection.cursor()

    command1 = """CREATE TABLE IF NOT EXISTS
    articles(title TEXT, link TEXT, date TEXT, source TEXT)"""
    cursor.execute(command1)

    # HTML From Website
    # we are web scrapign the Research sit of AQR Capital
    url = "https://www.ibm.com/blogs/blockchain/"
    result = requests.get(url)
    doc = BeautifulSoup(result.text, "html.parser")
    # this is the main div that holds each article on the main page

    # finds the div that contains the title and link for IT Security Guru articles
    tags = doc.find_all("h4", class_="ibm-h3 ibm-padding-top-1")
    tags = str(tags)
    tags = tags.split('<h4 class="ibm-h3 ibm-padding-top-1"><a class="ibm-blog__header-link" href="')
    tags.remove(tags[0])

    for x in range(0, len(tags)):
        article = tags[x]
        article = article.split('"><span class="ibm-textcolor-default">')
        link = article[0]
        title = article[1]
        title = title[:-18]

        date = "2022"

        source = "IBM Blockchain"

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

