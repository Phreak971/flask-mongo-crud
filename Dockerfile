# Step 1 select default OS image
FROM alpine

# Step 2 Setting up environment
RUN apk add py3-pip
RUN apk add --no-cache python3-dev && pip3 install --upgrade pip

# Step 3 Configure a software
WORKDIR /app   # Defining working directory

# Installing dependencies.
COPY /requirements.txt /app

RUN pip3 install -r /app/requirements.txt

# Copying project files.
COPY ["flask_api.py", "/app"]
COPY ["mongo_api.py", "/app"]

# Exposing an internal port
EXPOSE 5001


# Step 4 set default commands
ENTRYPOINT [ "python3" ] # Default command

# These commands will be replaced if user provides any command by himself
CMD ["flask_api.py"]
