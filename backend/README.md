
# Backend - CastingAgency API

## Setting up the Backend

### Install Dependencies

1. **Python 3.8** - Follow instructions to install the latest version of python for your platform in the [python docs](https://docs.python.org/3/using/unix.html#getting-and-installing-the-latest-version-of-python)

2. **Virtual Environment** - We recommend working within a virtual environment whenever using Python for projects. This keeps your dependencies for each project separate and organized. Instructions for setting up a virual environment for your platform can be found in the [python docs](https://packaging.python.org/guides/installing-using-pip-and-virtual-environments/)

3. **PIP Dependencies** - Once your virtual environment is setup and running, install the required dependencies by navigating to the `/backend` directory and running:

```bash
pip install -r requirements.txt
```

#### Key Pip Dependencies

- [Flask](http://flask.pocoo.org/) is a lightweight backend microservices framework. Flask is required to handle requests and responses.

- [SQLAlchemy](https://www.sqlalchemy.org/) and [Flask-SQLAlchemy](https://flask-sqlalchemy.palletsprojects.com/en/2.x/) are libraries to handle the lightweight sqlite database. Since we want you to focus on auth, we handle the heavy lift for you in `./src/database/models.py`. We recommend skimming this code first so you know how to interface with the Drink model.

- [jose](https://python-jose.readthedocs.io/en/latest/) JavaScript Object Signing and Encryption for JWTs. Useful for encoding, decoding, and verifying JWTS.

### Set up the Database

With Postgres running, create a `casting-agency` database:

```bash
createdb casting-agency
```

Setup the environment variables with file provided `setup.sh`. From the `backend` folder in terminal run:

```bash
source setup.sh
```

### Run the Server

From within the `./src` directory first ensure you are working using your created virtual environment.

To run the server, execute:

```bash
flask run --reload
```

The `--reload` flag will detect file changes and restart the server automatically.


## Tasks

### Setup Auth0

1. Create a new Auth0 Account
2. Select a unique tenant domain
3. Create a new, single page web application
4. Create a new API
   - in API Settings:
     - Enable RBAC
     - Enable Add Permissions in the Access Token
5. Create new API permissions:
   - `get:actors`
   - `get:movies`
   - `patch:actor`
   - `patch:movie`
   - `post:actors`
   - `post:movies`
   - `delete:actor`
   - `delete:movie`
7. Create new roles for:
   - Casting Assistant
     - can `get:movies`
     - can `get:actors`
    - Casting Director
	     - can `get:movies`
	     - can `get:actors`
	     - can `patch:actor`
		 - can `patch:movie`
	     - can `post:actors`
	     - can `post:movies`
	    - can `delete:actor`
   - Executive Producer
     - can perform all actions
8. Test your endpoints with [Postman](https://getpostman.com).
   - Register 3 users - assign the Casting Assistant, Casting Director role and Executive Producer Role
   - Sign into each account and make note of the JWT.
   - Import the postman collection `/backend/casting-agency.postman_collection.json`

## Testing

To deploy the tests, run

```bash
dropdb casting-agency-test
createdb casting-agency-test
python test_casting_agency_api.py
```