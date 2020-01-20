# fastapi-example
FastAPI in Sesam microservice - example

### A connector demonstrating basic use of FastAPI to make a Sesam connector 

#### An example of system config   
```
{
  "_id": "fastapi-demo",
  "type": "system:microservice",
  "docker": {
    "environment": {
      "LOG_LEVEL": "DEBUG",
      "PORT": "8080"
    },
    "image": "mofsesam/fastapi-example:develop",
    "port": 8080
  }
}

```
 
#### An example of input pipe 
```

```


#### An example of pipe with transform 
```

```


#### An example of pipe with transform to 
```

```


### Advanced

The docker image is made from https://github.com/tiangolo/uvicorn-gunicorn-fastapi-docker
The general comments, configuration files and environment variables are applicable.

#### A note on FastAPI self documentaion and exploration
One of the selling point of FastAPI is self documentaion and exploration. This is most useful for local development and testing in a Sesam connector context. 

You can change local permissions to allow Anonymous "Read microservice proxy" to access microservice in a webbrowser, but the proxy nature will cause problems.
https://github.com/sesam-community/msoft-planner
https://fastapi.tiangolo.com/advanced/sub-applications-proxy/

TIP: The automatically constructed openapi.json file can be downloaded and used e.g. to make a Postman collection (must be converted from json to yaml)



