# Base image.
FROM python:3.5

# Set the DEBIAN_FRONTEND environment variable only during the build
ENV DEBIAN_FRONTEND noninteractive
RUN apt-get update
RUN apt-get install nano -y

# copy scripts
RUN mkdir /opt/spinn3r_data_extract
COPY . /opt/spinn3r_data_extract

#prepare work directory
WORKDIR /opt/spinn3r_data_extract

# install flask & co
RUN pip install -r requirements.txt

# prepare port
EXPOSE 5000

# Define working volumes
VOLUME ["/opt/spinn3r_data_extract", "/opt/spinn3r_data_extract/conf"]

#lauch app
CMD python app.py
