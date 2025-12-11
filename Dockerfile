FROM python:3.13-alpine
ENV LANG=C.UTF-8

RUN : \
    && apk --no-interactive update \
    && apk --no-interactive --no-cache add ffmpeg \
    && rm -rf /var/cache/apk \
    && :

WORKDIR /tmp/gallery-dl
COPY . /tmp/gallery-dl/

RUN : \
    && python3 -B -m pip --no-cache-dir --no-input --disable-pip-version-check install --root-user-action ignore -U \
        pip \
    && python3 -B -m pip --no-cache-dir --no-input --disable-pip-version-check install --root-user-action ignore -U \
        /tmp/gallery-dl \
        yt-dlp[default] \
        requests[socks] \
        truststore \
        jinja2 \
        pyyaml \
    && ( rm -rf /root/.cache/pip || true ) \
    && ( find /usr/local/lib/python3.*/site-packages/setuptools -name __pycache__ -exec rm -rf {} + || true ) \
    && ( find /usr/local/lib/python3.*/site-packages/wheel      -name __pycache__ -exec rm -rf {} + || true ) \
    && rm -rf /tmp/gallery-dl \
    && :

ENTRYPOINT [ "gallery-dl" ]
