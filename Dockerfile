# select the base image that is best for our application
FROM python:3

# install any operating system junk

# set the working directory to copy stuff to
WORKDIR /app

# copy all the code form the local directory into the image
COPY accounts accounts
COPY attendees attendees
COPY common common
COPY conference_go conference_go
COPY events events
COPY presentations presentations
COPY requirements.txt requirements.txt
COPY manage.py manage.py

# install any language dependencies
RUN pip install -r requirements.txt

# set the command to run the application
CMD gunicorn --bind 0.0.0.0:8000 conference_go.wsgi