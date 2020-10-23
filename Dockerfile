FROM python:3.8.6-alpine
COPY . /app
WORKDIR /app
ENV DATA_DIR /data
ENV PYO3_PYTHON=/usr/local/bin/python
RUN echo "https://dl-3.alpinelinux.org/alpine/v3.10/main" >> /etc/apk/repositories && echo "https://dl-3.alpinelinux.org/alpine/v3.10/community" >> /etc/apk/repositories
RUN apk add --no-cache python3 gcompat patchelf rust cargo && patchelf --add-needed libgcompat.so.0 /usr/local/bin/python
RUN echo 'manylinux1_compatible = True' > /usr/local/lib/python/_manylinux.py && cd /app/check-env/ && cargo build --release && cd .. && cp /app/check-env/target/release/libcheck_env.so /app/check_env.so && rm /usr/local/lib/python3.7/_manylinux.py
RUN pip install -r requirements.txt ; touch /.containernv
CMD /usr/local/bin/python /app/main.py
