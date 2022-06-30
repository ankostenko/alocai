# alocai

Alocai technical assignment.

# Run

To run the assignment you'll need **docker**, **docker-compose** and **curl**.

From root directory of the project run command

```sh
docker-compose up --build
```

# To see if it works

Run command

```sh
curl -F "file=@data/data.csv" localhost:8000/upload
```

# Run tests

Run command 

```sh
docker-compose exec server pytest
```
