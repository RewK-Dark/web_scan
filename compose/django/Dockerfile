# More Datascience frendly gist can be found here: https://gist.github.com/ruddra/870d7a51238ddfa4b50375086c12a4f5
# pull official python alpine image
FROM python:3.8.18-bullseye

# Set Environment Variable
ENV PYTHONUNBUFFERED 1
ENV C_FORCE_ROOT true



# Making source and static directory
RUN mkdir /source
RUN mkdir /static

# Creating Work Directory
WORKDIR /source

# un-comment the following two dependecies if you want to add library like pandas, scipy and numpy
# openblas \ 
# libstdc++ 
RUN apt-get update && apt-get install -y gettext libgettextpo-dev zlib1g libjpeg-dev
# Installing temporary packages required for installing requirements.pip 

# un-comment if you want to install numpy, pandas, scipy etc and their supported dependencies
# g++ \
# openblas-dev \
# cmake \
# && ln -s /usr/include/locale.h /usr/include/xlocale.h

# Update pip
RUN pip install --upgrade pip

# **if you want to install scipy uncomment the following file**
# RUN pip3 install --no-cache-dir --disable-pip-version-check scipy==1.3.1

# Installing requirements.pip from project
COPY ./requirements.txt /scripts/
RUN pip install --no-cache-dir -r /scripts/requirements.txt

# *install psycopg2 if you don't have it requirements.pip*
# RUN pip install --no-cache-dir psycopg2

# removing temporary packages from docker and removing cache 
# RUN apk del build-deps && \
#     find -type d -name __pycache__ -prune -exec rm -rf {} \; && \
#     rm -rf ~/.cache/pip

# CMD will run when this dockerfile is running
CMD ["sh", "-c", "python manage.py collectstatic --no-input; python manage.py migrate; gunicorn core.wsgi -b 0.0.0.0:85"]
