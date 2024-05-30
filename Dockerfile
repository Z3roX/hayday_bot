FROM python:3.8-slim
COPY bot.py /bot.py
COPY app.py /app.py
RUN apt-get update && apt-get install -y python3-opencv
RUN pip install adb numpy imutils requests flask
CMD ["flask", "run", "--host=0.0.0.0"]