# aggregator-back

Backend part of vehicle aggregator project 

CREATE VIRTUAL ENVIROMENT

`python -m venv env`

ACTIVATE VIRTUAL ENVIROMENT (Linux, Mac?)

`source env/bin/activate`

INSTALL LIBRARIES

`pip install -r requirements.txt`

CREATE database.db file (SQLITE)

`python model-stub.py`

NOW WE HAVE FILE database.db in current directory

RUN API IN DEV MODE:

`uvicorn main:app --reload`

SHOW DOCUMENTIONS

- http://127.0.0.1:8000/auth/docs#/
- http://127.0.0.1:8000/company/docs#/
- http://127.0.0.1:8000/vehicle/docs#/
