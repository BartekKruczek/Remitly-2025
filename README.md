# Remitly-2025

## How to build the project
It is highly recommended to use docker application for this launch. In order to make it running, please consider using following command:
```bash
docker compose up --build
```

It will launch a postgres database and containerized version of the application on ports 5432 and 8080 respectively. Inside
containerized app, poetry is used to manage dependencies. What is more, they are stored in newly created virtual environment.

## How does it work


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