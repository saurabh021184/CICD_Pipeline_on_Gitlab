# This file is a template, and might need editing before it works on your project.
FROM alpine:3.12


RUN apk add --update --no-cache git py3-pip py-pip jq zip openssl python3

WORKDIR /usr/src/app

COPY requirements.txt /usr/src/app/

RUN pip install --upgrade pip wheel \
    &&  pip3 install --no-cache --ignore-installed -r requirements.txt

COPY . /usr/src/app

# For Django
EXPOSE 8000
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]

# For some other command
# CMD ["python", "app.py"]
