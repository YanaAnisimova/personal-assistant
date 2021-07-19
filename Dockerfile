FROM python:3.9

WORKDIR /app

RUN pip install pipenv

COPY Pipfile .
COPY Pipfile.lock .

RUN pipenv install --system --deploy

COPY personal_assistant/ .

CMD ["python", "./assist_controller.py"]