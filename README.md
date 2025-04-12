# Remitly-2025
Repository for Remitly 2025 Internship task

## How to build the project
It is highly recommended to use docker application for this launch. In order to make it running, please consider using following command:
```bash
docker compose up --build
```

It will launch a postgres database and containerized version of the application on ports 5432 and 8080 respectively. Inside
containerized app, poetry is used to manage dependencies. What is more, they are stored in newly created virtual environment.

## How does it work
TODO: describe how it works, all endpoints, how to use them, etc. Also how containerized app is connected to the database. Maybe
add some diagrams.

## Implemented endpoints
There are 4 in total FastAPI endpoints:
- **/v1/swift-codes/{swift_code}** (GET) - returns information about the swift code
- **/v1/swift-codes/country/{countryISO2code}** (GET) - returns all information about the swift codes for the given country ISO2 code
- **/v1/swift-codes/{swift_code}** (DELETE) - deletes information about the swift code. Note: you have to pass `-X DELETE` flag

## How to extract information from DB
It is recommended to use command line interface (CLI) to extract information. Please, consider following example command:
```bash
curl http://localhost:8080/v1/swift-codes/KCCPPLPW1AM
```

You can also follow these command with flag various additional flags. For now, few have been tested:
- `-o` to save the output to a file, i.e.: `-o swift_code.json`. It will create a file with the name `swift_code.json` in the current directory.
- `-X DELETE` to delete the swift code from the database. It will remove the swift code from the database and return a success message. Without it, the code will execute a GET request.

## PostgreSQL
Database itself is running on port 5432. You can connect with it using PostgreSQL client or CLI. Credentials are:
- login: postgres
- password: password
- database_name: swift_db
- postgres_db: mydb
- ports: 5432:5432

You can use the following command to connect to the database:
```bash
psql -h localhost -p 5432 -U postgres -d mydb
```

To verify it's correctness, fell free to display first 10 rows of the table:
```sql
SELECT * FROM swift_db LIMIT 10;
```

## How to run tests
TODO: describe how to run tests

## Clean up
For the safety reasons, there is no implemented any automatic clean up command. In order to stop the application, and thus the database, user should do it manually. To recreate whole environment/experiments, previously created containers should be removed, which also kills the database.