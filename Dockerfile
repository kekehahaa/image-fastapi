FROM python:3.11

WORKDIR /app

COPY ./requirements.txt ./
COPY ./.env /code/.env

RUN apt update && apt install -y ffmpeg
RUN pip install --no-cache-dir -r requirements.txt
RUN pip install python-ffmpeg
RUN pip install ffmpeg-python

COPY . .

EXPOSE 8000

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]