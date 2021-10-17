FROM python:3.7

ADD . /discord

WORKDIR /discord

RUN pip3 install -r req.txt

CMD ["python","bot.py"]