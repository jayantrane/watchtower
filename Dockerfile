# Use an official Python runtime as a parent image
FROM python:3.9-slim

# Set the working directory in the container
WORKDIR /app

# Copy the entire project directory and install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY *.py .
RUN mkdir data
#COPY data /app/data/

ENV OPTIONS="--periodic_alert"
# Command to run the Python script
CMD ["sh", "-c", "python3 main.py $OPTIONS"]