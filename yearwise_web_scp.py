from requests import get
from bs4 import BeautifulSoup as sp
import pandas as pd
import numpy as np

title = []
id = []
runtime = []
genre = []
ratings = []
director = []
cast = []
desc = []
movie_link = []
released_year = []
link_base = "https://www.imdb.com"

def create_csv(year):
    df = pd.DataFrame({
    "Title" : title,
    "Id" : id,
    "Runtime" : runtime,
    "Genre" : genre,
    "Ratings" : ratings,
    "Director" : director,
    "Cast" : cast,
    "Description" : desc,
    "Released_year":released_year,
    "Movie_link" : movie_link,
    })
    df = df.mask(df.applymap(str).eq('[]'))
    df=df.dropna()
    df = df.drop_duplicates(subset=["title"], keep=False)
    df.to_csv(f"cleaned_data_{year}.csv",index=False)

inp_year = int(input("Enter the year for which you want to scrap the movies data "))

print("Year  Number of pages visited")
for year in range(inp_year,inp_year+1):
    url = f"https://www.imdb.com/search/title/?year={year}&title_type=feature&"
    url1 = url
    count = 1
    
    title = []
    id = []
    runtime = []
    genre = []
    ratings = []
    director = []
    cast = []
    desc = []
    movie_link = []
    released_year = []

    # url = "https://www.imdb.com//search/title/?title_type=feature&year=2018-01-01,2018-12-31&sort=release_date,asc&start=6801"
    while(True):
        html = get(url1)
        html = html.text
        soup = sp(html,'html.parser')
        print(year,count,url1)
        count +=1
        for card_movie in soup.find_all('div',class_ = "lister-item mode-advanced"):

            id.append(card_movie.find('h3',class_ = "lister-item-header").a.get("href").split("/")[2])

            title.append(card_movie.find('h3',class_ = "lister-item-header").a.text)

            if card_movie.find('h3',class_ = "lister-item-header") == None:
                movie_link.append(None)
            else:
                movie_link.append(link_base+""+card_movie.find('h3',class_ = "lister-item-header").a.get("href"))

            if card_movie.find('span',class_ = "genre") == None:
                genre.append(None)
            else:
                genre.append(card_movie.find('span',class_ = "genre").text.replace(",","").split())

            released_year.append(year)

            try:
                desc.append(card_movie.find_all('p',class_ = "text-muted")[-1].text.strip())
            except:
                desc.append(None)

            if card_movie.find('span',class_ = "runtime") == None:
                runtime.append(None)
            else:
                runtime.append(card_movie.find('span',class_ = "runtime").text.strip())

            if card_movie.find('div',class_ = 'ratings-bar') == None or card_movie.find('div',class_ = 'ratings-bar').strong==None:
                ratings.append(None)
            else:
                ratings.append(card_movie.find('div',class_ = 'ratings-bar').strong.text)
            
            if card_movie.find("p",class_="").text.strip().replace(",","").split("\n") == None:
                director.append(None)
            else:
                director.append(card_movie.find("p",class_="").text.strip().replace(",","").split("\n")[1:2])

            if len(card_movie.find("p",class_="").text.strip().split("|")) < 2:
                cast.append(None)
            else:
                if len(card_movie.find("p",class_="").text.strip().split("|")[1].replace("\n","").split(":")) <= 2:
                    cast.append(card_movie.find("p",class_="").text.strip().replace("\n","").split("Stars:")[-1].replace(" ","").split(","))
                else:
                    cast.append(None)
            if count%40 == 0:
                create_csv(year)
        
        if soup.find('a',class_ = 'lister-page-next next-page') != None:
            url1 = link_base+""+soup.find('a',class_ = 'lister-page-next next-page').get('href')
        else:
            break

        if soup.find('a',class_ = 'lister-page-next next-page') == None:
            # print("RUNNING")
            break

print("Completd...")