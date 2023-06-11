import requests
import json
import csv
import urllib.request
import os

base_url = 'https://api.themoviedb.org/3/'
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

movie_list = []

def discover_movies(page=1):
    url = f'{base_url}discover/movie?api_key={api_key}&primary_release_date.gte=1900-01-01&primary_release_date.lte=2021-12-31&page={page}'
    response = requests.get(url)
    data = json.loads(response.content)
    return data['results']

# Crear directorio para guardar las imágenes
image_dir = 'images'
if not os.path.exists(image_dir):
    os.makedirs(image_dir)

for page in range(1, 101):
    movies = discover_movies(page)
    movie_list.extend(movies)
    if len(movie_list) >= 2000:
        break

with open('movies.csv', 'w', newline='', encoding='utf-8') as csvfile:
    fieldnames = ['Title', 'Rating', 'Genre', 'Year', 'Director', 'Image']
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames, delimiter=';')
    writer.writeheader()

    for movie in movie_list:
        movie_data = get_movie_details(movie['id'])
        title = movie_data['title']
        rating = movie_data['vote_average']
        genre = get_genre(movie_data['genres'])
        year = movie_data['release_date'][:4]
        director = movie_data['credits']['crew'][0]['name'] if len(movie_data['credits']['crew']) > 0 and movie_data['credits']['crew'][0]['job'] == 'Director' else 'Unknown'
        
        poster_path = movie_data['poster_path']
        if poster_path is None:
            image_path = os.path.join(image_dir, 'noimage.jpg')
        else:
            image_url = f'https://image.tmdb.org/t/p/w500{poster_path}'
            image_path = os.path.join(image_dir, f'{movie["id"]}.jpg')
            try:
                urllib.request.urlretrieve(image_url, image_path)
            except urllib.error.HTTPError:
                image_path = os.path.join(image_dir, 'noimage.jpg')

        writer.writerow({'Title': title, 'Rating': rating, 'Genre': genre, 'Year': year, 'Director': director, 'Image': image_path})
