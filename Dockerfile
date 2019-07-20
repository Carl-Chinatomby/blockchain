FROM python:3.7.4

WORKDIR /var/app
ENV PYTHONPATH=${PYTHONPATH}:/var/app/blockchain
RUN /usr/local/bin/pip install pip==19.1.1

RUN python3 -m venv /opt/venv

COPY . /var/app
RUN pip install -r /var/app/requirements.txt

EXPOSE 5000
CMD /opt/venv/bin/python && exec python app.py
