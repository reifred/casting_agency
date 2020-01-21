# Casting Agency Backend

## Getting Started

### Installing Dependencies

#### Python 3.7

Follow instructions to install the latest version of python for your platform in the [python docs](https://docs.python.org/3/using/unix.html#getting-and-installing-the-latest-version-of-python)

#### Virtual Enviornment

We recommend working within a virtual environment whenever using Python for projects. This keeps your dependencies for each project separate and organaized. Instructions for setting up a virual enviornment for your platform can be found in the [python docs](https://packaging.python.org/guides/installing-using-pip-and-virtual-environments/)

#### PIP Dependencies

Once you have your virtual environment setup and running, install dependencies by naviging to the `/backend` directory and running:

```bash
pip install -r requirements.txt
```

This will install all of the required packages we selected within the `requirements.txt` file.

##### Key Dependencies

- [Flask](http://flask.pocoo.org/)  is a lightweight backend microservices framework. Flask is required to handle requests and responses.

- [SQLAlchemy](https://www.sqlalchemy.org/) and [Flask-SQLAlchemy](https://flask-sqlalchemy.palletsprojects.com/en/2.x/) are libraries to handle the lightweight sqlite database. Since we want you to focus on auth, we handle the heavy lift for you in `./src/database/models.py`. We recommend skimming this code first so you know how to interface with the Drink model.

- [jose](https://python-jose.readthedocs.io/en/latest/) JavaScript Object Signing and Encryption for JWTs. Useful for encoding, decoding, and verifying JWTS.

### Setting up Auth0

1. Create a new Auth0 Account
2. Select a unique tenant domain
3. Create a new, single page web application
4. Create a new API
    - in API Settings:
        - Enable RBAC
        - Enable Add Permissions in the Access Token
5. Create new API permissions:
    - `get:actors`
    - `post:actors`
    - `patch:actors`
    - `delete:actors`
    - `get:movies`
    - `post:movies`
    - `patch:movies`
    - `patch:movies`
6. Create a new machine to machine application called Casting         Assistant.
    - For each application created: Authorize the application by selecting at least one authorized API and select permissions required.
    - Repeat steps above for Casting Director and Executive Producer

    Permissions allowed for the different users:
    - Casting Assistant
        - can `get:movies`
        - can `get:actors`
    - Casting Director
        - All permissions a Casting Assistant has and…
        - can `post:actors`
        - can `delete:actors`
        - can `patch:actors`
        - can `patch:movies`
    - Executive Producer
        - All permissions a Casting Director has and…
        - can `post:movies`
        - can `delete:movies`

    - Take note of the client_id and client_secret of the different applications created. These are to be used
      in the environment variables. Check the .env-example for more environment variables.

## Database Setup
With Postgres running, create two databases.
- From the project folder, in terminal run:
```bash
createdb agency
```
Create another database that will be used for running tests.
```bash
createdb agency_test
```
Ensure that the user has all privileges access to both databases. If you need additional information on setting up the PostgreSQL databases, checkout the [PostgreSQL tutorial](http://www.postgresqltutorial.com/).

## Running the server

From within the project directory first ensure you are working using your created virtual environment.

To run the server:

- Create a `.env` file in the root of the project directory. 
- Copy the contents of `.env.example` into the `.env` file.
- Edit with the database information from the previous section.
- Add the Auth0 machine to machine applications' `Client ID` and `Client Secret`.
- Run the command `source .env` to load the environment variables.
- Run the tests `pytest`. If the tests all pass, then the setup was successfull.
- To run the application on `http://localhost:5000`, execute:

```bash
flask run
```
## API Documentation.
7. Endpoints

    | Functionality            | Endpoint                      | Casting assistant  |  Casting Director  | Executive Producer |
    | ------------------------ | ----------------------------- | :----------------: | :----------------: | :----------------: |
    | Fetches a list of actors | GET /actors                   | :heavy_check_mark: | :heavy_check_mark: | :heavy_check_mark: |
    | Fetches a list of movies | GET /movies                   | :heavy_check_mark: | :heavy_check_mark: | :heavy_check_mark: |
    | Fetches a specific actor | GET /actors/&lt;id&gt;        | :heavy_check_mark: | :heavy_check_mark: | :heavy_check_mark: |
    | Fetches a specific movie | GET /movies/&lt;id&gt;        | :heavy_check_mark: | :heavy_check_mark: | :heavy_check_mark: |
    | Creates an actor         | POST /actor                   |        :x:         | :heavy_check_mark: | :heavy_check_mark: |
    | Patches an actor         | PATCH /actors/&lt;id&gt;      |        :x:         | :heavy_check_mark: | :heavy_check_mark: |
    | Delete an Actor          | DELETE /actors/&lt;id&gt;     |        :x:         | :heavy_check_mark: | :heavy_check_mark: |
    | Creates a movie          | POST /movies                  |        :x:         |        :x:         | :heavy_check_mark: |
    | Deletes a movie          | DELETE /movies/&lt;id&gt;     |        :x:         |        :x:         | :heavy_check_mark: |

    >_tip_: The endpoints are prefixed with  **api/v1** i.e GET actors **/api/v1/actors**
