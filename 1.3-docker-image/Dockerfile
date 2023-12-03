FROM python:3-alpine

ENV OWM_CITY Honolulu
ENV OWM_API_KEY xxxxxxxxxxx

WORKDIR /app

COPY requirements.txt ./

RUN pip install -r requirements.txt

COPY getweather.py ./

CMD [ "python", "getweather.py" ]
