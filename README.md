# station-prices-app-full

This repo contains all the code to run locally the station prices application.

## Running the backend

The backend is package inside docker containers.
Make sure you build the api image and to download the latest PostGIS image before running the docker-compose file.

## Running the frontend

The front is running on its own, to start it: go to the front folder and run: npm start
Make sure that node.js is installed in your computer
Make sure to add also a .env file in the front repository containing your Mapbox key in REACT_APP_API_KEY

## Database

The PostgreSQL container is using the db/ folder as a persistent volume

## Database Update

After starting the containers, go to update_scripts and run python update_stations.py
