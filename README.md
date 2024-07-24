# Embedding API

### How to install This app
  - step 1:
    Install python 3.10 from https://www.python.org/downloads/release/python-3100/
  - Step 2:
    download pdm (python dependency manager) from https://pdm-project.org/latest/ or run pip install --user pdm
  - Step 3:
    Copy Json file which contains definations to main directory of the project(do not rename that json file).
  - Step 4:
    on terminal write  
    ```sh 
        pdm install
    ```
  - Step 5:
    to run api server 
    ```sh
        pdm run localserver
    ```
  - Step 6:
    http://127.0.0.1:3000/docs#/


# Docker build and run 

### build

```sh
    docker build -t embedding_api .
```

### run
```sh
    docker run -d -p 3000:3000 aalwazrah/embedding_api:latest

```


