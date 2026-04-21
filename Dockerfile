FROM python:3.12-alpine
ENV PORT=8080 \
    APP_NAME=enclava-cap-e2e-payload \
    APP_VERSION=v2 \
    DATA_DIR=/data
COPY app.py /usr/local/bin/app
RUN chmod +x /usr/local/bin/app && mkdir -p /data && chmod 0777 /data
EXPOSE 8080
CMD ["/usr/local/bin/app"]
