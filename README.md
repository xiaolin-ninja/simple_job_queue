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
    $ createdb sites
    $ python server.py init

Re-run server after first init:
    $ python server.py

Servers runs on: http://localhost:8080/

## Usage

### Add Task:
`curl -X POST http://localhost:8080/add_job/URL`

replace `URL` with the site you wish to scrape

Example:  
`curl -X POST http://localhost:8080/add_job/www.google.com`   
returns task ID

### Check Status:
`curl -X POST http://localhost:8080/status/id`

replace `ID` with task ID.

Example:  
`curl -X POST http://localhost:8080/status/1`   

## File structure

    .
    ├── server.py                # Flask RESTful web API
    ├── model.py          	 	 # Database model
    └── ????           # Test webhooks data