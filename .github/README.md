# SFDS PIM MICROSERVICE.PY [![CircleCI](https://badgen.net/circleci/github/SFDigitalServices/pim-microservice-py/master)](https://circleci.com/gh/SFDigitalServices/pim-microservice-py) [![Coverage Status](https://coveralls.io/repos/github/SFDigitalServices/pim-microservice-py/badge.svg?branch=master)](https://coveralls.io/github/SFDigitalServices/pim-microservice-py?branch=master)
This microservice interacts with various data sources from Planning Information Map (PIM)

### Setup
#### Environment variables
`PLN_ARCGIS_PARCEL`: URL to Planning's ArcGIS Parcel server

### Sample Usage
Install Pipenv (if needed)
> $ pip install --user pipenv

Install included packages
> $ pipenv install

Start WSGI Server
> (pim-microservice-py)$ pipenv run gunicorn 'service.microservice:start_service()'

Open with cURL or web browser  
> Retrieve parcel data via address [(Documentation)](https://sfds-developer.apigee.io/docs/documentation/1/routes/parcels/get)  
> (example)$ curl http://127.0.0.1:8000/arcgis/parcels?address=1650%20mission%20street  
  
> Retrieve data via parcel number [(Documentation)](https://sfds-developer.apigee.io/docs/documentation/1/routes/records/%7Bparcel%7D/get)  
> (example)$ curl http://127.0.0.1:8000/records/[parcel id]?fields=year_built,building_area  
