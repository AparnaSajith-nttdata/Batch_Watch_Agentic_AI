import csv
import random
from datetime import datetime, timedelta

job_names = ['DailyETL', 'WeeklyReport', 'DataSync', 'Cleanup']
statuses = ['Success', 'Failure', 'Running', 'Missed']

with open('sla_logs.csv', 'w', newline='') as csvfile:
    fieldnames = ['job_id', 'job_name', 'scheduled_start_time', 'actual_start_time', 'scheduled_end_time', 'actual_end_time', 'status', 'duration', 'sla_breach', 'error_message', 'alert_sent', 'comments']
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
    writer.writeheader()
    for i in range(1, 101):
        job_name = random.choice(job_names)
        status = random.choice(statuses)
        scheduled_start = datetime.now() - timedelta(days=random.randint(0, 10), hours=random.randint(0, 23))
        actual_start = scheduled_start + timedelta(minutes=random.randint(-5, 5))
        scheduled_end = scheduled_start + timedelta(hours=1)
        actual_end = actual_start + timedelta(minutes=random.randint(50, 70))
        duration = int((actual_end - actual_start).total_seconds() / 60)
        sla_breach = actual_end > scheduled_end
        error_message = '' if status == 'Success' else 'Error occurred'
        alert_sent = sla_breach or status != 'Success'
        comments = 'Dummy data'
        writer.writerow({
            'job_id': i,
            'job_name': job_name,
            'scheduled_start_time': scheduled_start.isoformat(),
            'actual_start_time': actual_start.isoformat(),
            'scheduled_end_time': scheduled_end.isoformat(),
            'actual_end_time': actual_end.isoformat(),
            'status': status,
            'duration': duration,
            'sla_breach': sla_breach,
            'error_message': error_message,
            'alert_sent': alert_sent,
            'comments': comments
        })