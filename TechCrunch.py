from bs4 import BeautifulSoup
import requests
import sqlite3

def TechCrunch():
    connection = sqlite3.connect('articles.db')
    cursor = connection.cursor()

    command1 = """CREATE TABLE IF NOT EXISTS
    articles(title TEXT, link TEXT, date TEXT, source TEXT)"""
    cursor.execute(command1)

    # HTML From Website
    # we are web scrapign the Research sit of AQR Capital
    url = "https://techcrunch.com/"
    result = requests.get(url)
    doc = BeautifulSoup(result.text, "html.parser")
    # this is the main div that holds each article on the main page

    # finds the div that contains the title and link for IT Security Guru articles
    tags = doc.find_all("h2", class_="post-block__title")
    # print(tags)

    for x in range(0, len(tags)):
        # we will iterate through each article to get the title, link and date
        # first we will get the tile and link because they are on the same line
        title_and_link = tags[x].find_all("a", class_="post-block__title__link")

        # turn it into a string for parsing
        title_and_link = str(title_and_link)

        # split it into two, the left side has the link and the right side has the title
        title_and_link = title_and_link.split('">')

        # get the title the remove the extraneous 3 characters on the end
        title = title_and_link[1]
        title = title.replace("\n", "")
        title = title.replace("\t", "")
        title = title[:-5]

        link = title_and_link[0]
        link = link.split("href=")
        link = link[1]
        link = link[1:]

        # have to use a different div to get the date due to how this site is set up
        find_date = doc.find_all("div", class_="river-byline")[x]
        # turn it into a string for parsing
        find_date = str(find_date)
        find_date = find_date.replace("\n", "")
        find_date = find_date.replace("\t", "")
        find_date = find_date[96:]
        find_date = find_date.split("</time><span class=")
        find_date = find_date[0]
        date = find_date

        source = "TechCrunch"

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



