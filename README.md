# DevOps Apprenticeship: Project Exercise

> If you are using GitPod for the project exercise (i.e. you cannot use your local machine) then you'll want to launch a VM using the [following link](https://gitpod.io/#https://github.com/CorndelWithSoftwire/DevOps-Course-Starter). Note this VM comes pre-setup with Python & Poetry pre-installed.

## System Requirements

The project uses poetry for Python to create an isolated environment and manage package dependencies. To prepare your system, ensure you have an official distribution of Python version 3.7+ and install Poetry using one of the following commands (as instructed by the [poetry documentation](https://python-poetry.org/docs/#system-requirements)):

### Poetry installation (Bash)

```bash
curl -sSL https://raw.githubusercontent.com/python-poetry/poetry/master/install-poetry.py | python -
```

### Poetry installation (PowerShell)

```powershell
(Invoke-WebRequest -Uri https://raw.githubusercontent.com/python-poetry/poetry/master/install-poetry.py -UseBasicParsing).Content | python -
```

## Dependencies

The project uses a virtual environment to isolate package dependencies. To create the virtual environment and install required packages, run the following from your preferred shell:

```bash
$ poetry install
```

You'll also need to clone a new `.env` file from the `.env.template` to store local configuration options. This is a one-time operation on first setup:

```bash
$ cp .env.template .env  # (first time only)
```

The `.env` file is used by flask to set environment variables when running `flask run`. This enables things like development mode (which also enables features like hot reloading when you make a file change). There's also a [SECRET_KEY](https://flask.palletsprojects.com/en/1.1.x/config/#SECRET_KEY) variable which is used to encrypt the flask session cookie.

Also need to populate the following Trello related variables:
TRELLO_KEY
TRELLO_SECRET
TRELLO_TOKEN
TRELLO_USERNAME
TRELLO_BOARDID


## Running the App

Once the all dependencies have been installed, start the Flask app in development mode within the Poetry environment by running:
```bash
$ poetry run flask run
```

You should see output similar to the following:
```bash
 * Serving Flask app "app" (lazy loading)
 * Environment: development
 * Debug mode: on
 * Running on http://127.0.0.1:5000/ (Press CTRL+C to quit)
 * Restarting with fsevents reloader
 * Debugger is active!
 * Debugger PIN: 226-556-590
```
Now visit [`http://localhost:5000/`](http://localhost:5000/) in your web browser to view the app.


## Running the tests:

This will run both the unit and integration tests

poetry run pytest




## Docker
To build and run a development docker container, run the following commands in a docker prompt:
```bash
docker build --target development --tag todo-app:dev .
docker run -d -p 7000:8000 --env-file .\.env --mount type=bind,source="$(pwd)"/todo_app,target=/todo_app todo-app:dev
```

The container should then be running on http://localhost:7000/

To build and run a production docker container, run the following commands in a docker prompt:
```bash
docker build --target production --tag todo-app:prod .
docker run -d -p 7001:8000 --env-file .\.env --mount type=bind,source="$(pwd)"/todo_app,target=/todo_app todo-app:prod
```

The container should then be running on http://localhost:7001/

## Testing in docker containers
To build and run a test docker container, run the following command in a docker prompt:
```bash
docker build --target test --tag todo-app:test .
docker run todo-app:test
```

If all the tests run successfully, you should see terminal output something like this:

```
============================= test session starts ==============================
platform linux -- Python 3.10.7, pytest-7.1.3, pluggy-1.0.0
rootdir: /tests
collected 4 items

tests/test_client.py .                                                    [ 25%]
tests/test_viewmodel.py ...                                               [100%]

============================== 4 passed in 0.33s ===============================
```