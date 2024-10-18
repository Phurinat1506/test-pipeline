FROM python:3.9-slim
WORKDIR /test_pipeline
COPY test_api_p5000.py /test_pipeline/
COPY requirements.txt /test_pipeline/
COPY . /test_pipeline/
RUN pip install --upgrade pip setuptools wheel --user
RUN pip install -r requirements.txt
ENV TZ="Asia/Bangkok"
CMD ["python","test_api_p5000.py"]
EXPOSE 5000