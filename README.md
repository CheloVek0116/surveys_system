# Django Test App

## Building

It is best to use the python `virtualenv` tool to build locally:

```sh
$ python3 -m venv venv
$ source venv/bin/activate
$ pip install -r requirements.txt
$ python manage.py makemigrations
$ python manage.py migrate
$ python manage.py runserver
```

Server running on `http://localhost:8000`



## URLs
```
# admin urls
http://localhost:8000/api/admin_surveys/<int:pk>/ - detail survey [GET, DELETE, PUT]
http://localhost:8000/api/admin_surveys/ - list of all surveys [GET, POST]
    POST(add new survey)
        data = {
            "name": "test one",
            "start_date": "2020-12-18",
            "end_date": "2020-12-19",
            "description": "description",
            "questions": [
                {
                    "name": "Your name?",
                    "question_type": "TEXT"
                },
                {
                    "name": "python or c#",
                    "question_type": "CHOICE",
                    "choices": [
                        {
                            "text": "python"
                        },
                        {
                            "text": "c#"
                        }
                    ]
                },
                {
                    "name": "select birds",
                    "question_type": "MULTIPLE_CHOICE",
                    "choices": [
                        {
                            "text": "pigeon"
                        },
                        {
                            "text": "tiger"
                        },
                        {
                            "text": "eagle"
                        }
                    ]
                }
            ]
        }


# client urls
http://localhost:8000/api/client_surveys/?user_id=1 - list of all surveys [GET]
http://localhost:8000/api/client_surveys/completed_surveys/?user_id=1 - completed surveys [GET]
http://localhost:8000/api/client_surveys/<int:pk>/?user_id=1 - detail survey(if completed with ansewers) [GET]
http://localhost:8000/api/client_surveys/<int:pk>/response/?user_id=1 - response to the survey [POST]
    POST(response)
    data = {
        "answers": [
            {
                "pk": 19,
                "answer": {
                    "text": "Alex"
                },
                "question_type": "TEXT"
            },
            {
                "pk": 8,
                "answer": {
                    "pk": 7,
                    "text": "python"
                },
                "question_type": "CHOICE"
            },
            {
                "pk": 3,
                "question_type": "MULTIPLE_CHOICE",
                "answer": [
                    {
                        "pk": 6,
                        "text": "pigeon"
                    },
                    {
                        "pk": 8,
                        "text": "eagle"
                    }
                ]
            }
        ]
    }
```
