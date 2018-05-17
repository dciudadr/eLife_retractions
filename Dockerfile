FROM jupyter/minimal-notebook
ENV PROJECT_HOME=/srv/elife_retractions

WORKDIR ${PROJECT_HOME}

COPY requirements.txt ${PROJECT_HOME}/
RUN pip install -r requirements.txt

COPY download-nltk-data.sh ${PROJECT_HOME}/
RUN bash ./download-nltk-data.sh

COPY elife_retractions ${PROJECT_HOME}/
