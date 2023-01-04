### Base image...
FROM python:3-slim-buster as base

# Install poetry...
RUN pip install poetry

# Only copy the files required to specify our dependencies
COPY pyproject.toml poetry.lock /

# Install prerequisites
RUN poetry install --no-dev --no-root

# Copy everything else...
COPY . .

# Expose port to listen on...
EXPOSE 8000

#--------------------------------------------------------------------------------#

### Production image...
FROM base as production

RUN pip install flask
RUN pip install gunicorn
RUN pip install pymongo

# Define entry point...
ENTRYPOINT poetry run gunicorn --bind 0.0.0.0 "todo_app.app:create_app()"


#--------------------------------------------------------------------------------#

### Development image...
FROM base as development

RUN pip install flask
RUN pip install python-dotenv
RUN pip install pymongo

# Define entry point...
ENTRYPOINT poetry run flask run --host=0.0.0.0 --port=8000


#--------------------------------------------------------------------------------#

### Testing image...
FROM base as test

# Install pytest, flask and dotenv...
RUN pip install pytest
RUN pip install flask
RUN pip install python-dotenv
RUN pip install pymongo
RUN pip install mongomock

# Define entry point...
ENTRYPOINT ["poetry", "run", "pytest", "todo_app/tests"]
