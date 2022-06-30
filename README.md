# alocai

Alocai technical assignment.

# Run

To run the assignment you'll need **docker**, **docker-compose** and **curl**.

From the root directory of the project, run the command.

```sh
docker-compose up --build
```

# To see if it works

You'll need a file with data in this repo located in folder data.

Run command.

```sh
curl -F "file=@data/data.csv" localhost:8000/upload
```

# Run tests

Run command 

```sh
docker-compose exec server pytest
```
