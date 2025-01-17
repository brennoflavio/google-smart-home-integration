import google_helpers
import nextcloud_helpers as nextcloud_helpers
from datetime import datetime, timedelta, timezone


def sync_tasks():
    tasks = google_helpers.get_tasks()

    for task in tasks:
        task_id = task["id"]
        task_due = task["due"]
        task_summary = task["title"]

        if not task_due:
            task_due = datetime.now(tz=timezone(timedelta(hours=-3)))

        nextcloud_helpers.create_task(task_summary, task_due)
        google_helpers.delete_task(task_id)


if __name__ == "__main__":
    sync_tasks()
