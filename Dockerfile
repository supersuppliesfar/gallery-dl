FROM python:3.14-alpine
ENV LANG=C.UTF-8

RUN : \
    && apk --no-interactive update \
    && apk --no-interactive --no-cache add ffmpeg \
    && rm -rf /var/cache/apk \
    && :

RUN python3 -B -m pip --no-cache-dir --no-input --disable-pip-version-check install --root-user-action ignore -U \
    pip \
    yt-dlp[default] \
    requests[socks] \
    truststore \
    jinja2 \
    pyyaml

COPY . /app/gallery-dl/
RUN python3 -B -m pip --no-cache-dir --no-input --disable-pip-version-check install --root-user-action ignore /app/gallery-dl \
    && ( rm -rf /root/.cache/pip || true ) \
    && ( find /usr/local/lib/python3.*/site-packages/setuptools -name __pycache__ -exec rm -rf {} + 2>/dev/null || true ) \
    && ( find /usr/local/lib/python3.*/site-packages/wheel      -name __pycache__ -exec rm -rf {} + 2>/dev/null || true )

ENTRYPOINT [ "gallery-dl" ]
