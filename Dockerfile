############################################################
# Dockerfile to build Python WSGI Application Containers
# Based on Ubuntu
############################################################

# Set the base image to Ubuntu
FROM ubuntu

# File Author / Maintainer
MAINTAINER bvcelari@gmail.com

# Add the application resources URL
RUN echo "deb http://archive.ubuntu.com/ubuntu/ $(lsb_release -sc) main universe" >> /etc/apt/sources.list

# Update the sources list
RUN apt-get update

# Install basic applications
RUN apt-get install -y git curl wget net-tools vim

# Install Python and Basic Python Tools
RUN apt-get install -y python python-dev python-distribute python-pip
#shuold be done using pip but do not work :/, is requirement for development, no live
RUN apt-get install Graphviz

# Install GIP system requirements
RUN apt-get install -y libmysqlclient-dev
RUN apt-get install -y libpq-dev python-dev
RUN apt-get install -y mysql-server
RUN apt-get install -y libjpeg8-dev zlib1g-dev libfreetype6-dev liblcms2-dev libwebp-dev tcl8.6-dev tk8.6-dev python-tk

# Clone app
RUN git clone https://github.com/bvcelari/GIP

# Get pip to download and install requirements:
RUN pip install -r /GIP/requirements.txt


# Expose ports, check if many aare fine
EXPOSE 8000 3306

# Set the default directory where CMD will execute
WORKDIR /GIP

# start mysql
# CMD /etc/init.d/mysql start
# Set the default command to execute
# when creating a new container
# CMD python manage.py runserver 0.0.0.0:8000
CMD /bin/bash
