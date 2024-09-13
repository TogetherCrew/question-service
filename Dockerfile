# It's recommended that we use `bullseye` for Python (alpine isn't suitable as it conflcts with numpy)
FROM python:3.12-bullseye AS base
WORKDIR /project
COPY . .
RUN pip3 install -no-cache-dir --upgrade -r requirements.txt

FROM base AS prod
CMD ["fastapi", "run", "app/main.py", "--port", "80"]