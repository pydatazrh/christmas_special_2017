FROM ubuntu:16.04
RUN apt-get update
RUN apt-get install -y software-properties-common vim
RUN add-apt-repository ppa:jonathonf/python-3.6
RUN apt-get update
RUN apt-get install -y build-essential python3.6 python3.6-dev python3-pip python3.6-venv
COPY . /app
WORKDIR /app

# update pip
RUN python3.6 -m pip install pip --upgrade

RUN pip3 install -r requirements.txt
ENTRYPOINT ["python3.6"]
CMD ["api.py"]