FROM python:3.10-bookworm

RUN apt-get install -y git

ARG GITHUB_REPO_URL

COPY parse_path.py .

RUN git clone $GITHUB_REPO_URL

RUN python3 parse_path.py $GITHUB_REPO_URL --output-file GIT_DIR

RUN pip3 install -r /$(cat GIT_DIR)/requirements.txt

CMD uvicorn $(cat GIT_DIR).main:app --host 0.0.0.0 --port 80