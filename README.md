# Prism OpenAPI

## Getting started

```shell
git clone https://github.com/matthew-shaw/prism-openapi.git
cd prism-openapi
```

### With Node.js

```shell
nvm install
npm install
npx prism mock openapi.yaml
```

### With Docker

```shell
docker compose up --build
```

## Running tests

```shell
pytest test_petstore_api.py
```
