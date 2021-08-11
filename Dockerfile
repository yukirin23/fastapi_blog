FROM python
COPY . /app
WORKDIR /app
COPY requirements.txt .
RUN pip instaall -r requirements.txt
CMD ["python", "main.py"]