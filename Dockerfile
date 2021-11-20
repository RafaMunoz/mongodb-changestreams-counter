FROM python:3.10-alpine
MAINTAINER Rafa Muñoz rafa93m@gmail.com (@rafa93m)

COPY requirements.txt /requirements.txt

RUN echo "****** Install requirements.txt ******" &&\
  pip3 install --no-cache-dir -r /requirements.txt && \
  rm -rf /requirements.txt && \
  echo "****** Create user ******" && \
  addgroup -S appuser && \
  adduser -h /app -G appuser -D appuser && \
  mkdir -p /app/data && \
  chown appuser:appuser -R /app

COPY src /app

WORKDIR /app
VOLUME /app/data
USER appuser

ENTRYPOINT ["/bin/sh","/app/docker-entrypoint.sh"]
CMD ["python3", "-u", "/app/main.py"]