# Put dockerfile inside your image directory
# along with required building files

# After building an image: "docker build . -t /image_name/"
# Run the image specifying volumes of Host and Container paths: 
# docker run -v C:\Users\username\pathname:/tmp __imagename__
# All the files created within the container will be saved on your specified host directory

FROM ubuntu:20.04

WORKDIR /tmp

#Install Python and Python-pip:
RUN apt-get update
RUN apt-get upgrade -y
RUN apt-get autoremove
RUN apt-get install -y python3
RUN apt-get install -y python3-pip

# Install dependencies:
COPY requirements.txt .
RUN pip install -r requirements.txt

# Run the application:
COPY ["model-stub.py", "model.py", "./"]
CMD ["python3", "model-stub.py"]