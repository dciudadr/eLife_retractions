FROM python:3.6.4
ENV PROJECT_HOME=/srv/elife_retractions

WORKDIR ${PROJECT_HOME}
RUN virtualenv venv

COPY requirements.txt ${PROJECT_HOME)/
RUN venv/bin/pip install -r requirements.txt

COPY elife_retractions ${PROJECT_HOME}/
# copy name files
#COPY *.cfg *.conf *.sh *.in *.txt *.py ${PROJECT_HOME}/

