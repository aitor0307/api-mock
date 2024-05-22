# Use an official Python runtime as a parent image
FROM python:3.11-slim

# Set the working directory in the container
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY . /app

# Install any needed packages specified in requirements.txt
RUN pip install --trusted-host pypi.python.org -r requirements.txt

# Make port 5000 available to the world outside this container
EXPOSE 5000

# Define environment variable
#ENV FLASK_APP=main.py

# Run app.py when the container launches
CMD [ "python", "-u", "-m" , "flask", "run", "--host", "0.0.0.0", "-p", "5000"] 