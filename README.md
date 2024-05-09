# simple_multi_app_server

## Introduction
A simple example of combining nginx, gunicorn and flask using docker-compose to serve multiple flask apps.

Suppose you have multiple self-contained flask apps that can run independently and you would like to put them all under the same domain, but using different suffixes for their endpoints. 
For instance if you have app1 and app2, both with a `/compute` endpoint, you would like to serve the `/compute` endpoint from app1 under `yourdomain/app1/compute` and the `/compute` endpoint of app2 under `yourdomain/app2/compute`.
This repo shows how you can do that using gunicorn, nginx and docker-compose.

This repo can be tested locally running the launch.sh script. Since it uses docker-compose all you need to have is a working version of docker.
When you test this repo locally, it will run everything under localhost, so the two test apps will be running under `localhost/app1` and `localhost/app2`

## Repo explanation

You will see there's three flask apps in the repo: app1, app2, and main_app
main_app is supposed to map to the main index of your domain, and will point to app1 and app2.
app1 and app2 will be completely self-contain and serve under yourdomain/app1 and yourdomain/app2. 

The main tricks to get this working are:
1. The apps use always `url_for()` to point to a particular endpoint. This ensures they will reach the correct endpoint whatever prefix is used.
2. We're using the global variable SCRIPT_NAME when launching the unicorn server, this is really what makes it possible to have an app running under a `/prefix`

This code will work however complex the endpoints are in your apps, if they are self-contained (e.g. you can run the flask application independently) they will map to the same prefix.

To understand how this code works I would recommend to test one of the apps independently first as a flask server and then using gunicorn.

For instance you can: 

`cd app1`

and run 

`app.py`

You will see the app is not serving under `localhost:5000` a prefix and you can reach both `localhost:5000/` and `localhost:5000/compute`

then close the flask server and run 

`SCRIPT_NAME=/app1 gunicorn --bind 0.0.0.0:5000 wsgi:app`

Now everything will run under the prefix `/app1`, so the index of the app is reachable at `localhost:5000/app1` and the `/compute` endpoint is reachable at `localhost:5000/app1/compute`

Finally, with docker-compose and nginx we demonstrate how app1 and app2 can both work under their own prefixes, and we add a simple load-balancer which will be able to forward requests to multiple instances of the same services. Also, we map everything under port 80 which is the default for http.

You can test that calling:

`launch.sh`

Now you can reach 
* app1 at `localhost/app1`
* its compute function at `localhost/app1/compute`
* app2 at `localhost/app1`
* the `/compute` endpoint for app2 at `localhost/app2/compute`
* and finally main_app which is just the entry point at `localhost` 

