# moberries-test

# Local Development

Start the dev server for local development:
```bash
docker-compose up
```

Run a command inside the docker container:

```bash
docker-compose run --rm web [command]
```

Run tests:

```bash
docker-compose run --rm web python manage.py test pizza
```

API Endpoints:
```
"customers": "http://45.32.238.102:8000/api/v1/customers/",
"menu": "http://45.32.238.102:8000/api/v1/menu/",
"orders": "http://45.32.238.102:8000/api/v1/orders/"
```