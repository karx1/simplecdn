FROM python:3.8.6-alpine
COPY . /app
WORKDIR /app
RUN echo "https://dl-3.alpinelinux.org/alpine/v3.10/main" >> /etc/apk/repositories && echo "https://dl-3.alpinelinux.org/alpine/v3.10/community" >> /etc/apk/repositories
RUN apk add --no-cache python3 gcompat patchelf rust cargo && patchelf --add-needed libgcompat.so.0 $(which python)
RUN cd /app/check-env/ && cargo build --release && cd .. && cp /app/check-env/target/release/libcheck_env.so /app/check_env.so
RUN pip install -r requirements.txt ; touch /.containernv
ENV DATA_DIR /data
CMD python /app/main.py
