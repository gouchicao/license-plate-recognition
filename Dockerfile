FROM ubuntu
LABEL maintainer="wang-junjian@qq.com"

RUN apt-get update && apt-get install -y \
    python3 \
    python3-pip \
    nano \
    && rm -rf /var/lib/apt/lists/*

ADD requirements.txt /license-plate-recognition/
WORKDIR /license-plate-recognition
RUN pip3 install --no-cache-dir -r requirements.txt

RUN apt-get update && apt-get install -y \
    libsm6 \
    libxrender1 \
    libxext-dev \
    && rm -rf /var/lib/apt/lists/*

ADD *.py /license-plate-recognition/

EXPOSE 5000

ENTRYPOINT ["python3", "app.py"]
