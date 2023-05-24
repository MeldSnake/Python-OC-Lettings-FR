# Start from a base image of python3.11
FROM python:3.11-alpine

# Determine the working directory
WORKDIR /usr/src/oc_lettings

# Copy the requirements.txt file onto the docker environment
COPY requirements.txt ./
# Run pip install on the requirements, skip caching as it would take more space
RUN [ "pip", "install", "--no-cache-dir", "-r", "requirements.txt" ]

# Copy all local files from the Host CWD to the docker CWD (/usr/src/oc_lettings)
COPY . .

# Create/Initialize the db on the docker image
RUN [ "python", "manage.py", "migrate" ]

# Collect static files
RUN [ "python", "manage.py", "collectstatic", "--noinput" ]

# Expose the port that the local server use in order for docker to know of it.
EXPOSE 8000

# Command executed to actually run the server
CMD [ "gunicorn", "--bind", "0.0.0.0:8000", "oc_lettings_site.wsgi:application" ]