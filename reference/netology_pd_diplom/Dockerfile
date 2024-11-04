# Dockerfile for Django application

# Use an official Python runtime as a parent image
FROM python:3.12

COPY ./ /netology_pd_diplom

# Set work directory
WORKDIR /code

# Install dependencies
COPY requirements.txt . /netology_pd_diplom/
RUN pip install --no-cache-dir -r requirements.txt

# Run the Django development server
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]