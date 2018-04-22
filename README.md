# Web Scraper Task Manager

## Dependencies

PostGreSQL
Python3
Flask
Redis

## Getting Started

    $ virtualenv env
    $ source env/bin/activate
    $ pip install -r requirements.txt
    $ createdb jobs
    $ python model.py
    $ python server.py

Servers runs on: http://localhost:8080/

## Usage

### Add Task:
`curl -X POST http://localhost:8080/add_job -d url=URL`

replace `URL` with the site you wish to scrape

Example:  
`curl -X POST http://localhost:8080/add_job -d url=www.google.com`   
returns task ID

### Check Status:
`curl -X POST http://localhost:8080/status -d id=ID`

replace `ID` with task ID.

Example:  
`curl -X POST http://localhost:8080/add_job -d id=1`   

## File structure

    .
    ├── server.py                # Flask RESTful web API
    ├── model.py          	 	 # Database model
    └── ????           # Test webhooks data