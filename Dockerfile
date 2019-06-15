FROM python:3.7-stretch

# Copy the app into /app
COPY /hands-on/webapp /app

# Change working directory
WORKDIR /app

# install dependencies 
RUN pip install -r app-requirements.txt \
    && cd /app

# In Docker, the containers themselves can have applications running on ports. To access these applications, we need to expose the containers internal port and bind the exposed port to a specified port on the host.
# Expose port and run the application when the container is started
EXPOSE 9999:9999
ENTRYPOINT python app.py 9999