FROM python:3.8.6-alpine
COPY . /app
WORKDIR /app
RUN echo "https://dl-3.alpinelinux.org/alpine/v3.10/main" >> /etc/apk/repositories && echo "https://dl-3.alpinelinux.org/alpine/v3.10/community" >> /etc/apk/repositories
RUN apk add --no-cache gcompat patchelf rust cargo && patchelf --add-needed libgcompat.so.0 /usr/bin/python3
RUN pip install -r requirements.txt ; touch /.containernv
ENV DATA_DIR /data
CMD python ./main.py
