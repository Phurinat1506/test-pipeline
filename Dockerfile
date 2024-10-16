FROM python:3.9-slim
WORKDIR /test_api
COPY test_api_p5000.py /test_api_p5000/
COPY requirements.txt /test_api_p5000/
COPY config.yaml /test_api_p5000/
COPY . /test_api_p5000/
RUN pip install --upgrade pip setuptools wheel --user
RUN pip install -r requirements.txt
ENV TZ="Asia/Bangkok"
CMD ["python","test_api_p5000.py"]
EXPOSE 5000