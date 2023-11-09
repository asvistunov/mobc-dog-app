FROM python:3.10-bookworm

COPY . mobc-dog-clinic-testing/

ARG APP_URL

RUN echo $APP_URL > mobc-dog-clinic-testing/app_url

RUN pip3 install -r mobc-dog-clinic-testing/requirements.txt


