import requests
import json
import csv

# El código genera un archivo CSV con 2000 datos de películas
# que incluyen el nombre de la pelicula, puntuación , género y año de lanzamiento

base_url = 'https://api.themoviedb.org/3/'

#Ingresar el API key generado en la página The movie Database
api_key = ''

def get_movie_details(movie_id):
    url = f'{base_url}movie/{movie_id}?api_key={api_key}&append_to_response=credits'
    response = requests.get(url)
    data = json.loads(response.content)
    return data

def get_genre(genre_list):
    if len(genre_list) > 0:
        return genre_list[0]['name']
    else:
        return 'Unknown'

def discover_movies(page=1):
    url = f'{base_url}discover/movie?api_key={api_key}&primary_release_date.gte=1900-01-01&primary_release_date.lte=2021-12-31&page={page}'
    response = requests.get(url)
    data = json.loads(response.content)
    return data['results']

movie_list = []

for page in range(1, 101):
    movies = discover_movies(page)
    movie_list.extend(movies)
    if len(movie_list) >= 2000:
        break

with open('movies.csv', 'w', newline='') as csvfile:
    fieldnames = ['Title', 'Rating', 'Genre', 'Year']
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames, delimiter=';')
    writer.writeheader()

    for movie in movie_list:
        movie_data = get_movie_details(movie['id'])
        title = movie_data['title']
        rating = movie_data['vote_average']
        genre = get_genre(movie_data['genres'])
        year = movie_data['release_date'][:4]
        writer.writerow({'Title': title, 'Rating': rating, 'Genre': genre, 'Year': year})
