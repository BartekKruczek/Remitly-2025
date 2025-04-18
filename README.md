# Remitly-2025
Repository for Remitly 2025 Internship task

## How to build the project
It is highly recommended to use docker application for this launch. In order to make it running, please consider using following command:
```
docker compose up --build
```

It will launch a postgres database and containerized version of the application on ports 5432 and 8080 respectively. Inside
containerized app, poetry is used to manage dependencies. What is more, they are stored in newly created virtual environment.

## How to run tests
All tests are being executed by [pytest-asyncio](https://pypi.org/project/pytest-asyncio/) framework. To run them, you have to firstly create docker container (follow steps above). You don't have to install locally dependencies, just execute it with:
```
docker exec -it remitly_api poetry run pytest tests/
```
It will call tests within created instance. If everything lights up green, that means endpoints are working and you can try to extract information from the database.

## How does it work
Long story short, the application is being containerized with docker. It is using FastAPI framework to create endpoints and PostgreSQL database to store information about swift codes. The application is running on port 8080, while the database is running on port 5432. The application is using SQLAlchemy ORM to interact with the database. Below you can see how containeralized application looks like:
![img1](/imgs/docker/1.png)

## Implemented endpoints
There are 4 in total FastAPI endpoints:
- **/v1/swift-codes/{swift_code}** (GET) - returns information about the swift code
- **/v1/swift-codes/country/{countryISO2code}** (GET) - returns all information about the swift codes for the given country ISO2 code
- **/v1/swift-codes** (POST) - creates a new data structure in database. It requires a JSON body passed in the request. Example CLI command:
```
curl -X POST http://localhost:8080/v1/swift-codes \
  -H "Content-Type: application/json" \
  -d '{
    "swift_code": "NEWCODE123XXX",
    "bank_name": "New Bank",
    "address": "Nowy Adres 1, Miasto",
    "country_iso2": "PL",
    "country_name": "POLAND",
    "is_headquarter": true
}'
```
- **/v1/swift-codes/{swift_code}** (DELETE) - deletes information about the swift code. Note: you have to pass `-X DELETE` flag

## How to extract information from DB
It is recommended to use command line interface (CLI) to extract information. Please, consider following example command:
```
curl http://localhost:8080/v1/swift-codes/KCCPPLPW1AM
```

You can also follow these command with flag various additional flags. For now, few have been tested:
- `-o` to save the output to a file, i.e.: `-o swift_code.json`. It will create a file with the name `swift_code.json` in the current directory.
- `-X DELETE` to delete the swift code from the database. It will remove the swift code from the database and return a success message. Without it, the code will execute a GET request.
- `-d` to pass a JSON body in the request. It is used for POST requests.
- `-s` to suppress any additional metadata, it is recommended to use it with `| jq .`.
- `-sS` to suppress any additional metadata and show errors. It is recommended to use it with `| jq .`.

By default, requested information is beeing send in JSON format. To display it in CLI as a pretty-printed JSON, you can use [jq](https://jqlang.org) tool. The only change that is needed is to add `| jq .` at the end of the command, i.e.: `<command> | jq .`. 

## PostgreSQL
Database itself is running on port 5432. You can connect with it using PostgreSQL client or CLI. Credentials are:
- login: postgres
- password: password
- database_name: swift_db
- postgres_db: mydb
- ports: 5432:5432

You can use the following command to connect to the database:
```
psql -h localhost -p 5432 -U postgres -d mydb
```

To verify it's correctness, feel free to display first 10 rows of the table:
```sql
SELECT * FROM swift_db LIMIT 10;
```

## Clean up
For the safety reasons, there is no implemented any automatic clean up command. In order to stop the application, and thus the database, user should do it manually. To recreate whole environment/experiments, previously created containers should be removed, which also kills the database.