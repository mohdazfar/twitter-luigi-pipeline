FROM mongo:latest

WORKDIR /app

RUN apt-get update && apt-get install -y \
    python3 \
    python3-pip 

COPY ./requirements.txt ./requirements.txt
RUN pip3 install --user -r requirements.txt
