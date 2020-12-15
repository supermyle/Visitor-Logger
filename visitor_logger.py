#!/usr/bin/python3
#Author Supermyle
#Final Project visitor_logger
#Programming for IT
#This program accessess the access_log_path defined in main()
#Unzips all zipped access logs and deletes them after being unzipped
#Creates a list of unique ip addresses from the logs 
#Logs time and unique user count to stats.log file and updates JSON in the server_root path defined in main
#The data is then used to display a visitor count on https://megadatagames.com/ with the time it was last updated
#This program can be run as a cron job using crontab for scheduling

import os
import fnmatch
import json
from datetime import datetime

#Create stats.log file to hold records containing time of execution and amount of unique users at that time
def create_file():
	#Create file stats.log if it does not exist
	fname = open("stats.log", "w")
	fname.close()

#Write to stats.log file the current time at execution and the amount of unique users at that time
def write_stats_log(unique_users):
	#Open file for appending
	fname = open("stats.log", "a")

	#Datetime object containing current date and time
	now = datetime.now()

	#[dd/mm/YY:H:M:S]
	dt_string = now.strftime("[%d/%b/%Y:%H:%M:%S]")

	#Write user count and time to file
	append_text = dt_string + " Unique users: " + str(unique_users) + "\n"
	fname.write(append_text)
	fname.close()

#Write JSON file with last updated time and the amount of visitors at that time
def write_json(server_root, unique_users):
	print("Visitors:", unique_users)

	#Datetime object containing current date and time
	now = datetime.now()

	#dd/mm/YY at H:M:S AM/PM
	dt_string = now.strftime("%d/%m/%Y at %I:%M:%S %p")

	print("Last updated", dt_string)

	#Create JSON with visitor and time data
	data = {}
	data['visitorData'] = []
	data['visitorData'].append({
		'visitors': unique_users,
		'lastUpdate': dt_string
	})

	json_file = server_root + "visitors.json"
	with open(json_file, 'w') as outfile:
		json.dump(data, outfile)

#Return count of users
def usercount(log_dir):
	#List of unique_users to be used to get length of to be returned
	unique_users = []
	#For every file in the access log directory
	for fname in os.listdir(log_dir):
		#If the filename contains the string "access.log" alone or with numbers after
		if fnmatch.fnmatch(fname, 'access.log*'):
			access_log = open(log_dir + fname, "r")
			for entry in access_log:
				#Split entry into a list on spaces
				log_data = entry.split(' ')
				#Only add ip_addr to dictionary if it's not already in there
				if log_data[0] not in unique_users:
					unique_users.append(log_data[0])
	return len(unique_users)

#Unzip all access.log gzip files and force delete them in log directory passed
def unzip_logs(log_dir):
	for fname in os.listdir(log_dir):
		if fname.endswith('.gz'):
			os.system('gzip -df ' + log_dir + fname)
	
#Main function that handles program flow
def main():
	print("Launching visitor_logger.py") 
	access_log_path = '/var/log/apache2/'
	server_root = '/var/www/html/megadatagames/public/'
	unzip_logs(access_log_path)
	unique_users = usercount(access_log_path)

	#Create stats.log file if it doesn't exist
	if not os.path.exists("stats.log"):
		create_file()

	write_stats_log(unique_users)
	write_json(server_root, unique_users)

#Executed when invoked directly rather than if program was a module
if __name__ == "__main__":
	main()
