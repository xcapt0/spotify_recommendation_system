FROM python:3.8.1
RUN mkdir /app
COPY . /app
WORKDIR /app
ENV LISTEN_PORT=5000
EXPOSE 5000
RUN pip install -r requirements.txt
CMD ["python3", "app.py"]