# FSND-Capstone

FSND-Capstone is the final project of Udacity's Full Stack Web Developer Nanodegree.

## Motivation

This project aims to cover all concepts that we study in this nanodegree program, so it is a great opportunity to review all the concepts by practicing this project.

## Getting Started

### Installing Dependencies

#### Python 3.7

Follow instructions to install the latest version of python for your platform in the [python docs](https://docs.python.org/3/using/unix.html#getting-and-installing-the-latest-version-of-python)

#### Virtual Enviornment

We recommend working within a virtual environment whenever using Python for projects. This keeps your dependencies for each project separate and organaized. Instructions for setting up a virual enviornment for your platform can be found in the [python docs](https://packaging.python.org/guides/installing-using-pip-and-virtual-environments/)

#### PIP Dependencies

Once you have your virtual environment setup and running, install dependencies by naviging to the `/` directory and running:

```bash
pip install -r requirements.txt
```

This will install all of the required packages we selected within the `requirements.txt` file.

##### Key Dependencies

- [Flask](http://flask.pocoo.org/) is a lightweight backend microservices framework. Flask is required to handle requests and responses.

- [SQLAlchemy](https://www.sqlalchemy.org/) is the Python SQL toolkit and ORM we'll use handle the lightweight sqlite database. You'll primarily work in app.py and can reference models.py.

## Running the server

From within the `/` directory first ensure you are working using your created virtual environment.

To run the server, execute:

```bash
export FLASK_APP=app.py
export FLASK_ENV=development
flask run
```

Setting the `FLASK_ENV` variable to `development` will detect file changes and restart the server automatically.

Setting the `FLASK_APP` variable to `app.py` directs flask to find the flask application.

## API Documention

### Introduction

This API provide 8 endpoints for casting agency website. The endpoints cover all basic opearations on the database, get, delete, post, and update on actors and movies of the casting agency.

### Base URL

This API is hosted in fsndcoffeeapi.eu.auth0.com

### Roles:

1. Casting Assistant:
   Can view actors and movies

2. Casting Director:
   All permissions a Casting Assistant has and…
   Add or delete an actor from the database
   Modify actors or movies

3. Executive Producer:
   All permissions a Casting Director has and…
   Add or delete a movie from the database

### Roles Tokens (Authintication):

1. Casting Assistant: `eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6Ing5VVhac010TllTRG9ScmY3R1pQRyJ9.eyJpc3MiOiJodHRwczovL2ZzbmRjb2ZmZWVhcGkuZXUuYXV0aDAuY29tLyIsInN1YiI6ImF1dGgwfDYyMDhkNjczNzNjN2QyMDA3MWJlMmNkMCIsImF1ZCI6ImNhcHN0b25lIiwiaWF0IjoxNjQ0NzU5NDE2LCJleHAiOjE2NDQ3NjY2MTYsImF6cCI6IlI5WUliYUpqcmg1Z3V6aXVHOW5LWWNKSVlxVEx1YVlVIiwic2NvcGUiOiIiLCJwZXJtaXNzaW9ucyI6WyJnZXQ6YWN0b3IiLCJnZXQ6bW92aWUiXX0.c-uRrxOrNUlXA0P6tUCFdAmXj20OdDPWf0kTBqltLgtsdMU2mYgXQVMswRKVM7nt_38jjZ8uMR01-9YXYPzF2XXi1lNEjFaK292HAoCAX2OG1pvU3wN-5wyqMngXPpw7_rUNcoo80ODcYWWsgdfkzlircaDkxZcD2RSxVwI1O1uxoR940GrDV2VJjdNspCvnp8rr0vrrYZUHpEWSIbOnUiTw2Qh70SKI3KivWcFzh0QXa6-6EbphOclH974VSxm8zfbdCuAyqal5N2RF5bEtxerhdu99eCwGutNAxEjhHi7z1nJM_nzFC5X2rDuyAK3eppQl1Uiu03OJilJuaKQciw`

2. Casting Director:
   `eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6Ing5VVhac010TllTRG9ScmY3R1pQRyJ9.eyJpc3MiOiJodHRwczovL2ZzbmRjb2ZmZWVhcGkuZXUuYXV0aDAuY29tLyIsInN1YiI6ImF1dGgwfDYyMDBmODMxZWU4MmViMDA3MmEwMTVhYSIsImF1ZCI6ImNhcHN0b25lIiwiaWF0IjoxNjQ0NzU5Mjg3LCJleHAiOjE2NDQ3NjY0ODcsImF6cCI6IlI5WUliYUpqcmg1Z3V6aXVHOW5LWWNKSVlxVEx1YVlVIiwic2NvcGUiOiIiLCJwZXJtaXNzaW9ucyI6WyJhZGQ6YWN0b3IiLCJkZWxldGU6YWN0b3IiLCJnZXQ6YWN0b3IiLCJnZXQ6bW92aWUiLCJwYXRjaDphY3RvciIsInBhdGNoOm1vdmllIl19.FarS2pLCnQvMFLegik5zgYdTRPkzMZ1tm5WmC_bW6d0zR5SDlPyXZg9tZTwHfPxO6Hkl4W1V3AStbuCBNk1qXEEx23dzMOEDvP-gfpRGIjWRjwgqDJqRkidwOKTJT67vLkXLqvcuPY55pULzQQfHMrX18_olpvxCfP9JMquWSanie1ENcZ64hf33xQR_VqzwnzUTo1Sl7N2PpghVQRLuDe-5DzkukvomTjZcIRJYDpT5HwHTrR2meLn3oYX_mw2OeiXm1U-ZJDPy6k84Pr1uNuarhdm6eZPSLKEF9rMi3xTooHbeBq7ND00mT6ETG0gVeKGGPAK-zZ6uXPUEclyE7A`

3. Executive Producer:
   `eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6Ing5VVhac010TllTRG9ScmY3R1pQRyJ9.eyJpc3MiOiJodHRwczovL2ZzbmRjb2ZmZWVhcGkuZXUuYXV0aDAuY29tLyIsInN1YiI6ImF1dGgwfDYyMDBmODAyODQzODA1MDA2YWRkZTdmNiIsImF1ZCI6ImNhcHN0b25lIiwiaWF0IjoxNjQ0NzU4ODg4LCJleHAiOjE2NDQ3NjYwODgsImF6cCI6IlI5WUliYUpqcmg1Z3V6aXVHOW5LWWNKSVlxVEx1YVlVIiwic2NvcGUiOiIiLCJwZXJtaXNzaW9ucyI6WyJhZGQ6YWN0b3IiLCJhZGQ6bW92aWUiLCJkZWxldGU6YWN0b3IiLCJkZWxldGU6bW92aWUiLCJnZXQ6YWN0b3IiLCJnZXQ6bW92aWUiLCJwYXRjaDphY3RvciIsInBhdGNoOm1vdmllIl19.RNJqBPnU78A5r4RjQJ0mXWWM6x9AIzWNIjukcfxWl0DwsKzewbVqbPDctsr0FwfmuRU8iEbi7B9vbXXt9beIOAiB6rKYgPjkMGLZhvFUZTHkLZhjFkqIM5AW3TpxIRew_PyCELMeLJvWtv3nTNrt9JrTvH2OArG_EOyz8zDxBmav_-fzDc3noC1we9YaG23QYCc8d9Ux9d9d7-c4oQJiNtIl20ktPaICnSQUVQagI47GVG0qAKE977eQ2Wd-Ky5VDEkzg-gZ0ABh6H7pEmWWPmdDmNc8M4vmsvoMMHPnVarxM9hEkpIzq-sg5xu3DHHMBnRauNua6FxZcw7uwrGSSA`

### Error

1. Code: 422, Message: Unprocessable Entity,
   Response: `{ "success" : False, "status_code" : 422, "message" : "Unprocessable Entity" }`
2. Code: 404, Message: Not Found,
   Response: `{ "success" : False, "status_code" : 404, "message" : "Not Found" }`
3. Code: 400, Message: Bad Request,
   Response: `{ "success" : False, "status_code" : 400, "message" : "Bad Request" } `
4. Code: 401, Message: Unauthorized,
   Response: `{ "success": False, "error": 401, "message": "Unauthorized" } `
5. Code: 403, Message: Forbidden,
   Response: `{ "success": False, "error": 403, "message": "Forbidden" } `
6. Code: 405, Message: Method not allowed,
   Response: `{ "success": False, "error": 405, "message": "Method not allowed" } `

### Resourse endpoints

1. Method: GET, URI: '/actors'  
   -Description: This endpoint will retrieve all actors from the database.
   -Requiered Role: Casting Assistant, or Casting Director, or Executive Producer.
   -Parameters: None
   -Response: `{ "actors": [ { "age": 25, "gender": "female", "id": 3, "name": "sara" }, { "age": 22, "gender": "fmale", "id": 4, "name": "hamed" } ], "success": true }`

2. Method: DELETE, URI: '/actors/<int:actor_id>'  
   -Description: This endpoint will delete the actor with a given id.
   -Requiered Role: Casting Director, or Executive Producer.
   -Parameters: None
   Response: `{ "deleted": 4, "success": true, "total_actors": 1 }`

3. Method: POST, URI: '/actors'  
   -Description: This endpoint will create a new actor with given parameters.
   -Requiered Role: Casting Director, or Executive Producer.
   -Parameters: name, age, gender
   Response: `{ "success": true, "created": 3, "total_actors": 3 }`

4. Method: PATCH, URI: '/actors/<int:actor_id>'  
   -Description: This endpoint will update a existing actor with given parameters.
   -Requiered Role: Casting Director, or Executive Producer.
   -Parameters: name, age, gender
   Response: `{ "actors": [ { "age": 12, "gender": "male", "id": 3, "name": "ahmed" } ], "success": true }`

5. Method: GET, URI: '/movies'
   -Description: This endpoint will retrieve all movies from the database.
   -Requiered Role: Casting Assistant, or Casting Director, or Executive Producer.
   -Parameters: None
   Response: `{ "movies": [ { "release_date": "Sat, 12 Dec 2020 00:00:00 GMT", "title": "Toy Story" } ], "success": true }`

6. Method: DELETE, URI: '/movies/<int:movie_id>'  
   -Description: This endpoint will delete the movie with a given id.
   -Requiered Role: Executive Producer.
   -Parameters: None
   Response: `{ "success": true, "deleted": 2, "total_movies": 1 }`

7. Method: POST, URI: '/movies'  
   -Description: This endpoint will create a new movie with given parameters.
   -Requiered Role: Executive Producer.
   -Parameters: title, release_date
   Response: `{ "success": true, "created": 3, "total_movies": 4 }`

8. Method: PATCH, URI: '/movies/<int:movie_id>'  
   -Description: This endpoint will update a existing movie with given parameters.
   -Requiered Role: Casting Director, or Executive Producer.
   -Parameters: title, release_date
   Response: `{ "movies": [ { "release_date": "Sat, 12 Dec 2020 00:00:00 GMT", "title": "Toy Story" } ], "success": true }`

## Testing

To run the tests, run

```
dropdb casting_agency_test
createdb casting_agency_test
python test_app.py
```
