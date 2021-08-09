FROM python:3-slim
WORKDIR /usr/src/app
COPY http.reqs.txt ./
RUN pip install --no-cache-dir -r http.reqs.txt
COPY ./telegram_calendar_bot.py ./
CMD [ "python", "./telegram_calendar_bot.py" ]