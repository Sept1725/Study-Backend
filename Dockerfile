FROM python:latest
WORKDIR /work/app/backend
RUN pip install uvicorn
RUN pip install fastapi
EXPOSE 8000