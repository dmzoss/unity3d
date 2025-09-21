FROM python:3.11-slim



EXPOSE 8001
WORKDIR /app
COPY . /app
RUN pip install -r requirements.txt

CMD ["python", "api.py"]