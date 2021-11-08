# Building image and running docker container

Put dockerfile inside your building directory along with required building files (`mode-stub.py, model.py, requirements.txt`)

After building an image: `docker build . -t /image_name/`

Run the image specifying volumes of Host and Container paths:  
`docker run -v C:\Users\username\pathname:/tmp __imagename__`

All the files created within the container will be saved in your specified host directory


`Note:
Anytime you change dockerfile, it is required to re-build your image`
