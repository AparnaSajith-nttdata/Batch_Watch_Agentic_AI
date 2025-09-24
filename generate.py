import random
from datetime import datetime, timedelta

# Constants
NUM_JOBS =30
NUM_DAYS =100
BOX_NAMES = [f"BOX_{i}" for i in range(5)] # Assuming5 boxes

# Job status
STATUS_SUCCESS = "SUCCESS"
STATUS_FAILURE = "FAILURE"
STATUS_LONG_RUNNING = "LONG_RUNNING"

# Function to generate job information
def generate_job_info(job_name, box_name, run_date):
 status = random.choices([STATUS_SUCCESS, STATUS_FAILURE, STATUS_LONG_RUNNING], weights=[0.7,0.2,0.1])[0]
 start_time = datetime.combine(run_date, datetime.min.time()) + timedelta(hours=random.randint(0,23), minutes=random.randint(0,59))
 if status == STATUS_LONG_RUNNING:
 end_time = start_time + timedelta(hours=random.randint(2,5)) # Long running jobs take2 to5 hours
 elif status == STATUS_SUCCESS:
 end_time = start_time + timedelta(minutes=random.randint(1,30)) # Successful jobs take up to30 minutes
 else:
 end_time = start_time + timedelta(minutes=random.randint(1,15)) # Failed jobs fail within15 minutes
 box_jump = random.randint(0,2) # Number of times the job's box is changed
 original_box = box_name
 if box_jump > 0:
 # Simulate box jump by changing the box name
 box_name = random.choice([b for b in BOX_NAMES if b != original_box])
 return {
 "job_name": job_name,
 "original_box": original_box,
 "box_name": box_name,
 "run_date": run_date,
 "status": status,
 "start_time": start_time.strftime("%Y-%m-%d %H:%M:%S"),
 "end_time": end_time.strftime("%Y-%m-%d %H:%M:%S"),
 "schedule": f"{random.randint(0,23)}:{random.randint(0,59)}", # Simple schedule representation
 "box_jump": box_jump,
 }

# Generate data for NUM_JOBS jobs over NUM_DAYS days
data = []
for job_id in range(NUM_JOBS):
 job_name = f"JOB_{job_id}"
 box_name = random.choice(BOX_NAMES)
 for day_offset in range(NUM_DAYS):
 run_date = (datetime.now() - timedelta(days=day_offset)).date()
 data.append(generate_job_info(job_name, box_name, run_date))

# Output the generated data
for log in data:
 print(f"Job Name: {log['job_name']}, Original Box: {log['original_box']}, Final Box: {log['box_name']}, Run Date: {log['run_date']}, Status: {log['status']}, Start Time: {log['start_time']}, End Time: {log['end_time']}, Schedule: {log['schedule']}, Box Jump: {log['box_jump']}")

# Optionally, save this data to a file
# with open("autosys_logs.txt", "w") as f:
# for log in data:
# f.write(f"Job Name: {log['job_name']}, Original Box: {log['original_box']}, Final Box: {log['box_name']}, Run Date: {log['run_date']}, Status: {log['status']}, Start Time: {log['start_time']}, End Time: {log['end_time']}, Schedule: {log['schedule']}, Box Jump: {log['box_jump']}\n")
