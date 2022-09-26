# What is 'taskly'?
To-do list API project.

Built using Django DRF.<br>
Supports OpenApi.

# Steps to get up and running.
1) `git clone git@github.com:mspagon/taskly.git`
2) `cd taskly`
3) `docker-compose up`

## Documentation
API documentation is supplied at the endpoint `/api/docs/` via OpenAPI.

## Test out the API using /api/docs/
Requests to the API can be made alongside the documentation by going to `/api/docs/`

# API usage examples:

### Create a User:
Before you use the API, you must create a user.
```
curl --location --request POST '0.0.0.0:8000/api/user/create/' \
--header 'Content-Type: application/json' \
--data-raw '{
    "name": "John Doe",
    "email": "test@example.com",
    "password": "secure_password"
}'
```

### Get a Token:
To make a request to `/api/task/` you must supply a token.
```
curl --location --request POST '0.0.0.0:8000/api/user/token/' \
--header 'Content-Type: application/json' \
--data-raw '{
    "email": "test@example.com",
    "password": "secure_password"
}'
```

### Add a Task:
```
Args:
  title       (string): Required
  description (string): Optional
  date_due    (string): Optional
```

```
curl --location --request POST '0.0.0.0:8000/api/task/' \
--header 'Authorization: Token 716c8535e12f98398cbe605804e7cf98a9d84e02' \
--header 'Content-Type: application/json' \
--data-raw '{
  "title": "Call Nancy.",
  "description": "Remind her to book an appointment.",
  "date_due": "2022-10-23T00:00:00.000Z"
}'
```

### List tasks:
```
curl --location --request GET '0.0.0.0:8000/api/task/' \
--header 'Authorization: Token 716c8535e12f98398cbe605804e7cf98a9d84e02'
```

### Get a single task:
```
curl --location --request GET '0.0.0.0:8000/api/task/1' \
--header 'Authorization: Token 716c8535e12f98398cbe605804e7cf98a9d84e02'
```
### Mark a task as complete
`date_completed` will be set to the **current time** when `is_completed` is set to `True`.
```
curl --location --request PATCH '0.0.0.0:8000/api/task/1/' \
--header 'Authorization: Token 716c8535e12f98398cbe605804e7cf98a9d84e02' \
--header 'Content-Type: application/json' \
--data-raw '{
  "is_completed": true
}'
```
### Unmark a task as complete
`date_completed` will be set to **null** when `is_completed` is set to `False`.
```
curl --location --request PATCH '0.0.0.0:8000/api/task/1/' \
--header 'Authorization: Token 716c8535e12f98398cbe605804e7cf98a9d84e02' \
--header 'Content-Type: application/json' \
--data-raw '{
  "is_completed": false
}'
```
### Filter tasks by date_due
```
curl --location --request GET '0.0.0.0:8000/api/task?start_date=2022-10-23T00:00:00Z&end_date=2022-10-26T00:00:00Z' \
--header 'Authorization: Token 716c8535e12f98398cbe605804e7cf98a9d84e02'
```

### Filter tasks by is_complete
```
curl --location --request GET '0.0.0.0:8000/api/task?is_completed=false' \
--header 'Authorization: Token 716c8535e12f98398cbe605804e7cf98a9d84e02'
```
