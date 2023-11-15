# start by pulling the python image
FROM python:3.8-alpine

# copy the requirements file into the image
COPY ./ /app/

# switch working directory
WORKDIR /app

# install the dependencies and packages in the requirements file
RUN pip install -r requirements.txt

# set environment variables
ENV DD_SERVICE="flask-test"
ENV DD_ENV="flask-test"
ENV DD_LOGS_INJECTION=true

# configure the container to run in an executed manner
ENTRYPOINT [ "ddtrace-run", "python", "app.py" ]
