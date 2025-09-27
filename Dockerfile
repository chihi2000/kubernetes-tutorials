FROM --platform=linux/amd64 python:3.11-slim

#set working directory
WORKDIR /app

#install system deps
RUN apt-get update && apt-get install -y build-essential default-libmysqlclient-dev && rm -rf /var/lib/apt/lists/*

#copy reqs of python
COPY requirement.txt .
RUN pip install --no-cache-dir -r requirement.txt

#copy source code
COPY . .
EXPOSE 8000
#run with uvicorn
CMD [ "uvicorn", "pythonbuilding.carsharing:app", "--host", "0.0.0.0", "--port", "8000" ]
