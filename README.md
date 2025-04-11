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

## How to extract information from DB
It is recommended to use command line interface or browser to extract information. You can follow a few options.
- CLI
```bash
curl http://localhost:8080/v1/swift-codes/KCCPPLPW1AM
```

You can also follow these command with flag `-o` to save the output to a file, i.e.: `-o swift_code.json`. It will create a file with the name `swift_code.json` in the current directory.

- Browser

Simply connect to the localhost:8080 following by v1/swift-codes/{swift_code} and you will be able to see extracted information, i.e.:
```bash
http://localhost:8080/v1/swift-codes/KCCPPLPW1AM
```

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