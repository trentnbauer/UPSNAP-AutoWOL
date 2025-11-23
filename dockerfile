# Use an official Python runtime as a parent image
FROM python:3.9-slim

# Set the working directory in the container
WORKDIR /app

# Install any necessary dependencies
# We install requests directly since it's the only one
RUN pip install --no-cache-dir requests

# Copy the current directory contents into the container at /app
COPY main.py .

# Set the entrypoint to python and the script
# This allows you to pass arguments directly to the docker run command
ENTRYPOINT ["python", "main.py"]