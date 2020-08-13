import numpy as np
import pandas as pd
import requests
from bs4 import BeautifulSoup

imdb_url = "https://www.imdb.com/chart/top/"
r = requests.get(imdb_url)
soup = BeautifulSoup(r.content, "html.parser")
incoming_data = soup.find_all("table", {"class" : "chart full-width"})
movie_table = (incoming_data[0].contents)[len(incoming_data[0].contents)-2]
movie_table = movie_table.find_all("tr")

names = []
release_year = []
rates = []
movie_sequence = np.arange(1,251,1)

# getting movie title and release year data
for movie in movie_table:
    movie_title = movie.find_all("td", {"class":"titleColumn"})
    movie_name = movie_title[0].text.replace("\n","").strip()
    release_year.append(movie_name[-6:].strip("()"))
    names.append((movie_name[5:len(movie_name)-6]).strip())

#getting movie rate
for movie in movie_table:
    movie_rating = movie.find_all("td", {"class":"ratingColumn imdbRating"})
    rates.append(movie_rating[0].text.replace("\n",""))

# dataframe creation from the data captured
df = {"Sequence" : movie_sequence, "Name": names, "Rates" :rates,"RealeaseYear": release_year}
movies = pd.DataFrame(data=df)

# save data as csv
# Enter the path below to the location where you want to save the csv file on your computer.
movies.to_csv(r'Path where you want to store the exported CSV file\imdbTop250.csv', index = False, header = True)
