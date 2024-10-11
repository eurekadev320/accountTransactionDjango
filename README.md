# Setup

## Requirements
* Python 3.7+

## Installation And Run
Copy .env.example into .env and fill up **SECRET_KEY**
```
pip install -r requirements.txt
python manage.py migrate
python manage.py createsuperuser    # creating the super user for admin site access
python manage.py runserver
```

# Implementation
1. **django** library
2. **django-rest** library for REST API implementation
3. Strict **type definition** and **validation check** using **Serializer** and **typing** libraries


# APIs
1. Account Creation  
```
URL: http://localhost:8000/accounts/ (GET)

Request: {
  "email": "user@example.com"
}

Response: {
  "uuid": "bf21637e-b0b5-4b3a-8fe3-179be1635941",
  "email": "user@example.com",
  "balance": 0,
  "created_at": "2023-03-20T10:03:02.539500Z",
  "updated_at": "2023-03-20T10:03:02.539500Z"
}
```
2. Account Detail (Get Balance)  
```
URL: http://localhost:8000/accounts/{uuid}/ (GET)

Response: {
  "uuid": "bf21637e-b0b5-4b3a-8fe3-179be1635941",
  "email": "user@example.com",
  "balance": 15,
  "created_at": "2023-03-20T10:03:02.539500Z",
  "updated_at": "2023-03-20T10:03:02.539500Z"
}
```
3. Send money to another account
```
URL: http://localhost:8000/accounts/{uuid}/send/ (POST)

Request: {
  "receiver": "receiver@email.com",  # Receiver account email
  "amount": 15
}

Response: {
  "uuid": "bf21637e-b0b5-4b3a-8fe3-179be1635941",
  "email": "user@example.com",
  "balance": 15,
  "created_at": "2023-03-20T10:03:02.539500Z",
  "updated_at": "2023-03-20T10:03:02.539500Z"
}
```
4. Transaction History
```
URL: http://localhost:8000/accounts/{uuid}/transactions/ (GET)

Response: [
  {
    "uuid": "e32a2e63-a9e8-4cf9-8c4a-38b335a02b78",
    "target": {
      "uuid": "7f2e0e5c-2aab-4bf5-93be-c8a4bd08003c",
      "email": "test@gmail.com"
    },
    "type": "receive",
    "amount": 1,
    "created_at": "2023-03-20T05:56:07.940452Z",
    "updated_at": "2023-03-20T05:56:07.940452Z"
  }
]
```

# Unit Testing
```
pytest
```

## Swagger API Docs
http://localhost:8000/docs/


## Admin Site
http://localhost:8000/admin/