import re
from datetime import datetime

NGINX_REGEX = re.compile(
    r'(?P<ip>\S+) \S+ \S+ '
    r'\[(?P<time>[^\]]+)\] '
    r'"(?P<method>\S+) (?P<path>\S+) \S+" '
    r'(?P<status>\d+) (?P<size>\d+)'
)

SYSLOG_REGEX = re.compile(
    r'(?P<month>\w{3}) (?P<day>\d{1,2}) '
    r'(?P<time>\d{2}:\d{2}:\d{2}) '
    r'(?P<host>\S+) '
    r'(?P<process>[\w\-]+)(?:\[\d+\])?: '
    r'(?P<message>.+)'
)

logs = ["nginx.log", "syslog.log"]

#Loop through lines and append it to a list
def read_logs(filepath):
    with open(filepath, "r") as file:
        line = []
        for f in file:
            line.append(f.strip())       
        return line
    
#Search through each line in the syslog and match the capturing group
def parse_syslog_line(line):
    match = SYSLOG_REGEX.search(line)
    if not match:
        return {}
    return match.groupdict()

#Search through each line in the nginx log and match the capturing group
def parse_nginx_line(line):
    match = NGINX_REGEX.search(line)
    if not match:
        return {}
    return match.groupdict()

#Format time and date correctly
def normalize_syslog_time(month, day, time):
    now = datetime.now()
    raw = f"{now.year} {month} {day} {time}"
    date = datetime.strptime(raw, "%Y %b %d %H:%M:%S")
    return date.isoformat()

#Format time and date correctly
def normalize_nginx_time(raw_time):
    date = datetime.strptime(raw_time, "%d/%b/%Y:%H:%M:%S %z")
    return date.isoformat()

#Make the paths to read log
nginx_lines = read_logs(f"../sample_logs/nginx.log")
syslog_lines = read_logs(f"../sample_logs/syslog.log")

#Go through each line and then parse the full dictionary with the correct time
for line in nginx_lines:
    parsed = parse_nginx_line(line)
    if parsed:
        parsed["time"] = normalize_nginx_time(parsed["time"])
        print(parsed)

for line in syslog_lines:
    parsed = parse_syslog_line(line)
    if parsed:
        parsed["time"] = normalize_syslog_time(parsed["month"], parsed["day"], parsed["time"])
        print(parsed)