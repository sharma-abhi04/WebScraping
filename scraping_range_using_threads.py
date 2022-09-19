from requests import get
from bs4 import BeautifulSoup as sp
import pandas as pd
import numpy as np
import concurrent.futures
import time

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

def create_csv():
    df = pd.DataFrame({
    "title" : title,
    "id" : id,
    "runtime" : runtime,
    "genre" : genre,
    "ratings" : ratings,
    "director" : director,
    "cast" : cast,
    "Describtion" : desc,
    "released_year":released_year,
    "movie_link" : movie_link,
    })
    df = df.mask(df.applymap(str).eq('[]'))
    df=df.dropna()
    df = df.drop_duplicates(subset=["title"], keep=False)
    return df

def data_gen(tup):
    count1 = 1
    for year in range(tup[0],tup[1]):
        url = f"https://www.imdb.com/search/title/?year={year}&title_type=feature&"
        url1 = url
        count = 1
        # create_csv()
        # url = "https://www.imdb.com//search/title/?title_type=feature&year=2018-01-01,2018-12-31&sort=release_date,asc&start=6801"
        while(True):
            html = get(url1)
            html = html.text
            soup = sp(html,'html.parser')
            print(year,count1,count,url1)
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
                    director.append(card_movie.find("p",class_="").text.strip().replace(",","").split("\n")[1:2][0])

                if len(card_movie.find("p",class_="").text.strip().split("|")) < 2:
                    cast.append(None)
                else:
                    if len(card_movie.find("p",class_="").text.strip().split("|")[1].replace("\n","").split(":")) < 2:
                        cast.append(card_movie.find("p",class_="").text.strip().split("|")[1].replace("\n","").split(":")[1].replace(", ",",").split(","))
                    else:
                        cast.append(None)
            
            count1 +=1
            if soup.find('a',class_ = 'lister-page-next next-page') != None:
                url1 = link_base+""+soup.find('a',class_ = 'lister-page-next next-page').get('href')
            else:
                break

            if soup.find('a',class_ = 'lister-page-next next-page') == None:
                print("RUNNING")
                break
    return create_csv()
                
global res
with concurrent.futures.ThreadPoolExecutor() as executor:
    st_yr = [2000,2009,2015,2019]
    ls_yr =  [2008,2014,2018,2022]
    # st_yr = range(2000,2021)
    # ls_yr = range(2001,2022)
    results = executor.map(data_gen, zip(st_yr,ls_yr))
    res = results

print("Completed...")