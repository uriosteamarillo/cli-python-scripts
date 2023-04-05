#!/usr/bin/python
import subprocess
import time
import sys
import json
import csv


# CALCULO EL INTERVALO

from datetime import datetime, timedelta

# Get the current datetime in UTC
now = datetime.utcnow()

# Subtract one day to get yesterday's date
yesterday = now - timedelta(days=1)

# Set the start time to midnight (0:00:00)
start_time = datetime(yesterday.year, yesterday.month, yesterday.day, 0, 0, 0, 0)

# Set the end time to just before midnight (23:59:59.999999)
end_time = datetime(yesterday.year, yesterday.month, yesterday.day, 23, 59, 59, 999999)

# Format the interval in ISO 8601 format
interval = f"{start_time.isoformat()}Z/{end_time.isoformat()}Z"

# Print the interval
print(interval)






# Load the JSON file into a Python object
with open("queryCola.json", "r") as f:
    data = json.load(f)

# Modify the value of "name"
data["interval"] = interval

# Save the modified object back to the JSON file
with open("queryCola.json", "w") as f:
    json.dump(data, f)


result = subprocess.run('gc -p santanderArgentina analytics conversations aggregates  query create --file queryCola.json', stdout=subprocess.PIPE, shell=True)

# Print the command output
f= result.stdout.decode('utf-8')

json_data = json.loads(f)

now = datetime.now()

# Format the date as a string that can be used as a filename
filename = now.strftime("%Y-%m-%d_%H-%M-%S.csv")

# Open CSV file for writing
with open(filename, 'w', newline='') as file:

    # Create CSV writer
	writer = csv.writer(file)

    # Write header row
	header = [ 'media_type', 'queue_id', 'interval',
    'nBlindTransferred', 'nConnected', 'nConsult', 'nConsultTransferred',
    'nError', 'nOffered', 'nOutbound', 'nOutboundAbandoned',
    'nOutboundAttempted', 'nOutboundConnected', 'nOverSla',
    'nStateTransitionError', 'nTransferred', 'tAbandon_max',
    'tAbandon_min', 'tAbandon_count', 'tAbandon_sum', 'tAcd_max',
    'tAcd_min', 'tAcd_count', 'tAcd_sum', 'tAcw_max', 'tAcw_min',
    'tAcw_count', 'tAcw_sum', 'tAgentResponseTime_max',
    'tAgentResponseTime_min', 'tAgentResponseTime_count',
    'tAgentResponseTime_sum', 'tAlert_max', 'tAlert_min',
    'tAlert_count', 'tAlert_sum', 'tAnswered_max',
    'tAnswered_min', 'tAnswered_count', 'tAnswered_sum',
    'tContacting_max', 'tContacting_min', 'tContacting_count',
    'tContacting_sum', 'tDialing_max', 'tDialing_min',
    'tDialing_count', 'tDialing_sum', 'tFlowOut_max',
    'tFlowOut_min', 'tFlowOut_count', 'tFlowOut_sum',
    'tHandle_max', 'tHandle_min', 'tHandle_count', 'tHandle_sum',
    'tHeld_max', 'tHeld_min', 'tHeld_count', 'tHeld_sum',
    'tHeldComplete_max', 'tHeldComplete_min',
    'tHeldComplete_count', 'tHeldComplete_sum', 'tIvr_max',
    'tIvr_min', 'tIvr_count', 'tIvr_sum', 'tMonitoring_max',
    'tMonitoring_min', 'tMonitoring_count', 'tNotResponding_max',
	'tNotResponding_min', 'tNotResponding_count', 'tNotResponding_sum',
	'tShortAbandon_max', 'tShortAbandon_min', 'tShortAbandon_count', 'tShortAbandon_sum',
	'tTalk_max', 'tTalk_min', 'tTalk_count', 'tTalk_sum', 'tTalkComplete_max', 'tTalkComplete_min', 
	'tTalkComplete_count', 'tTalkComplete_sum', 'tUserResponseTime_max', 'tUserResponseTime_min', 
	'tUserResponseTime_count', 'tUserResponseTime_sum', 'tVoicemail_max', 'tVoicemail_min', 'tVoicemail_count', 
	'tVoicemail_sum', 'tWait_max', 'tWait_min', 'tWait_count', 'tWait_sum']
	writer.writerow(header)
	print(len(header))

    # Loop through results
	for result in json_data['results']:
		group = result['group']
		media_type = group['mediaType']
		queue_id = group.get('queueId', '')

        # Loop through data
		for data in result['data']:
			interval = data['interval']
			metrics = data['metrics']
			row = [media_type, queue_id, interval]
			arr0 = [0] * 96
			row = row + arr0
        # Loop through metrics
			for metric in metrics:
				metric_name = metric['metric']
				stats = metric['stats']

				# Add stats to row
				for stat_name, stat_value in stats.items():
					#row.append(stat_value)
					if metric_name.startswith("t"):
						index = header.index(metric_name +"_" +stat_name)
					else:
						index = header.index(metric_name)
					
					row[index] =stat_value
					# Write row to CSV
		print(row)
		writer.writerow(row)
