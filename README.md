# lunchbot
A customizable bot for helping to decide what's for lunch

To test and debug locally, run

    make test
    
To run in a setup similar to "production" (Uvicorn workers behind a Gunicorn server), run

    make deploy

The service is hosted on [Heroku](https://what-about-lunch.herokuapp.com). Currently, only the menu of [Cafe Magdalen](https://www.oxfordsp.com/parklife/magdalen-centre/) can be parsed.

To get the weekly lunch menu, go to 

[https://what-about-lunch.herokuapp.com/cafe_magdalen](https://what-about-lunch.herokuapp.com/cafe_magdalen)

![](./examples/magdalen-lunch.png)

Or, if you're interested in a menu for a specific day - i.e. **wednesday**, go to 

[https://what-about-lunch.herokuapp.com/cafe_magdalen/wednesday](https://what-about-lunch.herokuapp.com/cafe_magdalen/wednesday)

To access the API docs (via Swagger and FastAPI) go [https://what-about-lunch.herokuapp.com/docs#/](https://what-about-lunch.herokuapp.com/docs#/).
