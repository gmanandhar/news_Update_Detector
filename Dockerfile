FROM python:alpine3.7
COPY . /app
WORKDIR /app
RUN pip install -r requirements.txt
RUN sed -Ei 's/^(bind-address|log)/#&/' /etc/mysql/my.cnf
CMD python ./main.py