FROM docker.arvancloud.ir/python:3.10.12

# set environment variables
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# set work directory
WORKDIR /code

# Install dependencies
RUN pip install --upgrade pip 
COPY requirements.txt .
RUN pip install -r requirements.txt

# copy the django project
COPY . .