# Web Scraper Job Queue

## Dependencies

Python3  
Flask  
PostGreSQL  
SQLAlchemy  
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
`curl -X POST http://localhost:8080/new/URL`

replace `URL` with the site you wish to scrape

Example:  
`curl -X POST http://localhost:8080/new/www.google.com`   

### Check Status:
`curl -X POST http://localhost:8080/status/id`

replace `ID` with task ID returned from `/new`.

Example:  
`curl -X POST http://localhost:8080/status/1`   

## File structure

    .
    ├── server.py 				 # Flask RESTful web API
    ├── model.py          	 	 # Database model
    └── helpers.py           	 # Worker functions
