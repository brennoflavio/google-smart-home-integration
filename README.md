# Google Smart Home Integration

This project aims to allow usage Google Home with open source tools, like Nextcloud.
It will be a set of scripts and instcutions to integrate Google Assistant with other tools.

## Calendar

`calendar_sync.py` is a script that syncs Google Calendar with Nextcloud Calendar. The idea is that
you'll use Google Assistant to create an event in your Google Calendar, and upon running this script
in a cron job, it will fetch the event, insert it in your Nextcloud Calendar and delete the event in Google.

First, copy the .env.example file and fill out with your data. To find your calendar id, go to settings and
find it there.

You'll need a GCP Project, a service account with permissions an Google Calendar API enabled. Then you export
the service account key as json, grab the email from there, and share you calendar with the service account
email.

You'll need to register the calendar using the service account, run the function `register_calendar` to do it.

Then setup a cron job to run this every 5 minutes and everything should work. If not, open an issue.
