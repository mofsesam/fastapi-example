# fastapi-example
### A connector demonstrating basic use of FastAPI to make a Sesam connector 
FastAPI in Sesam microservice - example

## What is FastAPI?
[FastAPI](https://fastapi.tiangolo.com/) is a modern, fast (high-performance), web framework for building APIs with Python 3.6+ based on standard Python type hints.

In the context of Sesam connectors it is natural to compare FastAPI with Flask. FastAPI is built for the purpose of building REST APIs with JSON as primary render format. This makes FastAPI code cleaner and more readable than Flask for this purpose. FastAPI is self documenting and validating. It produces APIs that are fully compatible with OpenAPI (Swagger). You are forced to think about validation early, but it is easy to to do validation.

## Examples
The example routings shows some basic FastAPI features in a Sesam context. See the code for `app/main.py` for details.

#### An example of system config in Sesam node  
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
The PORT environment variable **must** be set and match the value set for port of microservice.  
The LOG_LEVEL environment variable defaults to INFO if not set.
 
#### An example of input pipe 
```
{
  "_id": "hello-fastapi-stream",
  "type": "pipe",
  "source": {
    "type": "json",
    "system": "fastapi-demo",
    "url": "/stream/items/100?step=10"
  },
  "transform": {
    "type": "dtl",
    "rules": {
      "default": [
        ["copy", "*"]
      ]
    }
  }
}

```


#### An example of pipe with transform 
```
{
  "_id": "fastapi-transform",
  "type": "pipe",
  "source": {
    "type": "embedded",
    "entities": [{
      "id": "892",
      "ticket": {
        "comment": "Testing to api from microservice in sesam, test1",
        "id": "892",
        "tags": ["test", "test2"]
      }
    }, {
      "id": "893",
      "ticket": {
        "comment": "Testing to api from microservice in sesam, test2",
        "id": "893",
        "tags": ["test", "test2"]
      }
    }, {
      "id": "894",
      "ticket": {
        "comment": "Testing api from microservice in sesam, test3",
        "id": "894",
        "tags": ["test", "test2"]
      }
    }]
  },
  "transform": [{
    "type": "http",
    "system": "fastapi-demo",
    "url": "/generic/"
  }, {
    "type": "dtl",
    "rules": {
      "default": [
        ["copy", "*"]
      ]
    }
  }],
  "pump": {
    "mode": "manual",
    "schedule_interval": 30
  }
}

```


#### An example of pipe with fastapi as sink
```
{
  "_id": "fastapi-endpoint",
  "type": "pipe",
  "source": {
    "type": "embedded",
    "entities": [{
      "_id": "892",
      "ticket": {
        "comment": "Testing api from microservice in sesam, test1",
        "id": "892",
        "tags": ["test", "test2"]
      }
    }, {
      "_id": "893",
      "ticket": {
        "comment": "Testing api from microservice in sesam, test2",
        "id": "893",
        "tags": ["test", "test2"]
      }
    }, {
      "_id": "894",
      "ticket": {
        "comment": "Testing api from microservice in sesam, test3",
        "id": "894",
        "tags": ["test", "test2"]
      }
    }]
  },
  "sink": {
    "type": "json",
    "system": "fastapi-demo",
    "url": "/generic/"
  },
  "transform": {
    "type": "dtl",
    "rules": {
      "default": [
        ["copy", "*"]
      ]
    }
  },
  "pump": {
    "mode": "manual",
    "schedule_interval": 30
  }
}

```


### Advanced

The docker image is made from https://github.com/tiangolo/uvicorn-gunicorn-fastapi-docker
The general comments, configuration files and environment variables are applicable.

#### A note on FastAPI self documentaion and exploration
One of the selling point of FastAPI is self documentaion and exploration. This is most useful for local development  in a Sesam connector context. 

You can change local permissions to allow Anonymous "Read microservice proxy" to access Sesam microservice in a webbrowser, but the proxy nature will cause problems. For hints see:
https://github.com/sesam-community/msoft-planner
https://fastapi.tiangolo.com/advanced/sub-applications-proxy/

#### A note on local development based on this example code
Set environment variables with set_local_env.bat (Windows)  
Use: docker-compose [build|up|down|push]  
When running with docker-compose up, go to http://localhost:8080/docs to see the interactiv OpenAPI (Swagger) documntation of example-api. TIP: The automatically constructed openapi.json file can be downloaded and used e.g. to make a Postman collection (must be converted from json to yaml)



