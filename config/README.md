# Movie Rating API

Build a movie rating API with Django and Django Rest Framework (DRF) that allows users to rate and review movies. The API should have the following endpoints:

- `/api/movies/`: Returns a list of movies with their title, description, and average rating.
- `/api/movies/<int:pk>/`: Returns details of a specific movie, including its title, description, release date, and rating.
- `/api/reviews/`: Returns a list of all movie reviews, including the user's name, the movie title, and the review text.
- `/api/reviews/<int:pk>/`: Returns details of a specific review, including the user's name, the movie title, and the review text.
- `/api/ratings/`: Allows users to submit a rating for a movie, with the following fields: movie id (foreign key to movie), rating (1-5), and user (foreign key to user).
- `/api/reviews/`: Allows users to submit a review for a movie, with the following fields: movie id (foreign key to movie), review text, and user (foreign key to user).

## Getting Started

1. Clone the repository:

```
git clone https://github.com/IcaroOm/Movie-Rating.git

```

2. Create and activate a virtual environment:

```
python3 -m venv env
source env/bin/activate
```

3. Install the project dependencies:

```
pip install -r requirements.txt
```

4. Set up the database:

```
python manage.py migrate
```

5. Create a superuser account:

```
python manage.py createsuperuser
```

6. Start the development server:

```
python manage.py runserver
```

7. Navigate to `http://localhost:8000` in your web browser to access the API.

## API Endpoints

- `/api/movies/`: Returns a list of movies with their title, description, and average rating.
- `/api/movies/<int:pk>/`: Returns details of a specific movie, including its title, description, release date, and rating.
- `/api/reviews/`: Returns a list of all movie reviews, including the user's name, the movie title, and the review text.
- `/api/reviews/<int:pk>/`: Returns details of a specific review, including the user's name, the movie title, and the review text.
- `/api/ratings/`: Allows users to submit a rating for a movie, with the following fields: movie id (foreign key to movie), rating (1-5), and user (foreign key to user).
- `/api/reviews/`: Allows users to submit a review for a movie, with the following fields: movie id (foreign key to movie), review text, and user (foreign key to user).

## Authentication

The API requires authentication for certain endpoints, including `/api/ratings/` and `/api/reviews/`. To authenticate, include a token in the `Authorization` header of your request. You can obtain a token by sending a `POST` request to `/api/token/` with your username and password in the request body.

## Examples

Here are some example requests you can make to the API using `curl`:

- Get a list of movies:

```
curl http://localhost:8000/api/movies/
```

- Get details of a specific movie:

```
curl http://localhost:8000/api/movies/1/
```

- Submit a rating for a movie:

```
curl -X POST -H "Authorization: Bearer <token>" \
  -H "Content-Type: application/json" \
  -d '{"movie": 1, "rating": 5}' \
  http://localhost:8000/api/ratings/
```

- Submit a review for a movie (authenticated):

```
curl -X POST -H "Authorization: Bearer <token>" \
  -H "Content-Type: application/json" \
  -d '{"movie": 1, "text": "This movie was great!"}' \
  http://localhost:8000/api/reviews/
```


