FROM python:3.9

WORKDIR /usr/src/app

COPY requirements/ requirements/
RUN pip install --no-cache-dir --upgrade pip
RUN pip install --no-cache-dir --upgrade setuptools
RUN pip install --no-cache-dir -r requirements/requirements.txt

COPY . /usr/src/app

EXPOSE 5000
ENV RUNTIME_DOCKER Yes

CMD python app.py
