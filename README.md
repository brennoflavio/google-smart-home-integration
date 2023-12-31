# Google Smart Home Integration

This project aims to allow usage Google Home with open source tools, like Nextcloud.
It will be a set of scripts and instcutions to integrate Google Assistant with other tools.

## Authorization

This project provices a simple Flask Server to authenticate to Google. You'll need a GCP project
with Calendar and Tasks API enabled, and an Oauth APP to generate credentials. Here's simple steps:

- Go to the Google Cloud Console: console.cloud.google.com
- Create a new Project.
- Enable the Google Tasks and Calendar APIs for your project.
- In the left sidebar, go to "APIs & Services" -> "OAuth consent screen".
- Fill out the form and save.
- In the left sidebar, go to "APIs & Services" -> "Credentials".
- Click "Create Credentials" at the top -> "OAuth client ID".
- Choose "Desktop app" as the Application Type. Give it a name and save.
- Download the credentials.

When creating your Oauth app, you'll need an https server with redirect routes running.

## Sync data

There is 2 one way sync in this repo that is meant to use as cron jobs:
- calendar
- tasks

They fetch data from Google, create the respective data in your Nextcloud and then deletes the data from Google.
This way when you say "Ok google create event test", the event will be created in Google Calendar, but then synced
to Nextcloud Calendar, so the end effect is like Google creating the event in your calendar.

## Google Keep

Google Keep does not have an Oauth API for free, so we rely on a mobile token and `gkeepapi` library. To use it, you'll
need to generate a master token and save it in the environemnt variable `GOOGLE_KEEP_MASTER_TOKEN`, and also save your
Google Account email in the variable `GOOGLE_KEEP_USER`. The steps includes
creating an app password and running a Docker command. You can find it [here](https://github.com/djsudduth/keep-it-markdown/issues/72#issuecomment-1793495242)

There is 2 things that are synced from Keep: Shopping list and Notes.

You can specificy a Shopping List name from Keep and a Task List from Nextlcoud to sync your shopping list, and for Notes it will sync to your Nextcloud Notes app.
