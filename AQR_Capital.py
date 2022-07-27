from bs4 import BeautifulSoup
import requests
import sqlite3

def AQR_Capital():
    # define connection to the SQLite database
    connection = sqlite3.connect('articles.db')
    cursor = connection.cursor()

    command1 = """CREATE TABLE IF NOT EXISTS
    articles(title TEXT, link TEXT, date TEXT, source TEXT)"""
    cursor.execute(command1)

    # HTML From Website
    # we are web scrapign the Research sit of AQR Capital
    url = "https://www.aqr.com/Insights/Research"
    result = requests.get(url)
    doc = BeautifulSoup(result.text, "html.parser")
    # this is the main div that holds each article on the main page
    tags = doc.find_all("div", class_="search-list__item")
    # we will iterate through each article to get the title, link, and date
    for x in range(0, len(tags)):
        # the cta--black class holds the title and link information
        entry = tags[x]
        get_info = entry.find_all("a", class_="cta--black")
        # we will turn it into a string to make it easy to parse
        get_info = str(get_info)

        # split the string at the > symbol because the artilce title comes after it
        get_info_title = get_info.split(">")
        title = get_info_title[1]
        # clean up the string by removing unecessary characters
        title = title[:-3]

        # do the same thing for the link. Split the string at href since the link will be on the other side
        get_link = get_info.split("href=")
        get_link = get_link[1]
        # split the string again to get rid of unecessary characters
        get_link = get_link.split(">")
        get_link = get_link[0]
        # remove unecessary character on front and end of string
        get_link = get_link[:-1]
        get_link = get_link[1:]
        # finally we end up with the link, just need to add the aqr.com part to the front
        link = "aqr.com" + get_link

        # finally, we will do the same thing for the date. Since it is in a div we need to use a different class
        get_date = entry.find_all("p", class_="article__date text--small")
        # turn it into a string for parsing
        get_date = str(get_date)
        # split string appropriately to isolate the date
        get_date = get_date.split(">")
        get_date = get_date[1]
        # get rid of white spaces by replacing them
        get_date = get_date.replace(" ", "")
        # get rid of the newline by stripping it
        get_date = get_date.strip()
        # finally, split again to get the final date
        get_date = get_date.split("<")
        get_date = get_date[0]
        date = get_date

        # set the source as AQR Capital for entry into database
        source = "AQR Capital"

        title = title.replace("'", "")
        title = title.replace('"', '')

        # this is to prevent duplicate articles. Check to see if article with same title is already in db
        cursor.execute("SELECT * FROM articles WHERE title = '" + title + "'")
        results = cursor.fetchall()
        if len(results) > 0:
            continue

        # add the information for each article into the db
        cursor.execute("INSERT INTO articles VALUES('" + title + "', '" + link + "', '" + date + "', '" + source + "')")
        # commit so that it saves
        connection.commit()

    # cursor.execute("DROP TABLE articles")
    # connection.commit()
    cursor.execute("SELECT * FROM articles")
    results = cursor.fetchall()
    # for x in results:
    # print(x)
    connection.close()
