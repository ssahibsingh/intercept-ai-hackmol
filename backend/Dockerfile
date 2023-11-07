# Use the official Python 3.10 image as the base
FROM python:3.10

# Set the working directory in the container to /app
WORKDIR /app

# Copy the current directory's content into the container at /app
COPY . /app

# Install the Python dependencies from the requirements.txt file
RUN pip --no-cache-dir install -r requirements.txt
# RUN pip install -r requirements.txt

# Expose port 5000 to the outside world
EXPOSE 5000

# Define the command to run when the container starts
CMD ["waitress-serve", "--listen=0.0.0.0:5000", "index:app"]