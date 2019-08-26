# Fantano API
[![Documentation Status](https://readthedocs.org/projects/fantano-api/badge/?version=latest)](https://fantano-api.readthedocs.io/en/latest/?badge=latest)

An API for accessing Anthony Fantano's music reviews.

### Implementation Details and Notes

This project is hosted on AWS using Elastic Beanstalk in a Docker container. Uptime is currently non-existent given that it is not fully finished, but once there is a working version that I can host, an endpoint will be provided.

### TODO

-   Improve the YT parser -> get EP reviews and NOT GOOD ratings.
-   Update ReadTheDocs
-   Diagram API endpoints

### Sample Usage:

Getting every review that recieved a perfect 10:

```python
import requests
endpoint = '<URL-TO-BE-DETERMINED>/ratings/10'
r = requests.get(endpoint)
```

### Documentation

Documentation is (very) in progress and hosted [here](fantano-api.readthedocs.io).

## Modules:
-   requests
-   flask
-   flask-restful
-   gunicorn
