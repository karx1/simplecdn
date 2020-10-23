FROM python:3.8.6-alpine
COPY . /app
WORKDIR /app
ENV DATA_DIR /data
ENV PYO3_PYTHON=/usr/local/bin/python
RUN echo "https://dl-3.alpinelinux.org/alpine/v3.10/main" >> /etc/apk/repositories && echo "https://dl-3.alpinelinux.org/alpine/v3.10/community" >> /etc/apk/repositories
RUN wget -q -O /etc/apk/keys/sgerrand.rsa.pub https://alpine-pkgs.sgerrand.com/sgerrand.rsa.pub && wget https://github.com/sgerrand/alpine-pkg-glibc/releases/download/2.32-r0/glibc-2.32-r0.apk && apk add glibc-2.32-r0.apk
RUN apk add --no-cache build-base python3 patchelf rust cargo && patchelf --add-needed libgcompat.so.0 /usr/local/bin/python
RUN echo 'manylinux1_compatible = True' > /usr/local/lib/python3.8/_manylinux.py && cd /app/check-env/ && cargo build --release && cd .. && cp /app/check-env/target/release/libcheck_env.so /app/check_env.so && rm /usr/local/lib/python3.8/_manylinux.py
RUN pip install -r requirements.txt ; touch /.containernv
CMD /usr/local/bin/python /app/main.py
