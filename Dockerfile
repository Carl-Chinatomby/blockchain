FROM python:3.6.1

WORKDIR /var/app
ENV PYTHONPATH=${PYTHONPATH}:/var/app/blockchain
RUN /usr/local/bin/pip install pip==9.0.1

COPY . /var/app
RUN pip install -r /var/app/requirements.txt
COPY entrypoint.sh /entrypoint.sh

EXPOSE 5000
ENTRYPOINT ["/entrypoint.sh"]