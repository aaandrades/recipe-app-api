# Python Image
FROM python:3.7-alpine

# Especify to python that run on docker 
ENV PYTHONUNBUFFERED 1

# Copy the requiment information 
COPY ./requirements.txt /requirements.txt
RUN pip install -r /requirements.txt

# Create empty folder on docker
RUN mkdir /app
# Change to the directory
WORKDIR /app
# Copy all the content of ./app into /app
COPY ./app /app


# Run the application with custom user to prevent security issues
RUN adduser -D user
USER user
