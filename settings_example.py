# Rename me to settings.py

# Location of the python-nmap module. I needed to add this to the sys.path
# in order to properly run the script with sudo.
# The script must be run with sudo in order for nmap to function correctly.
# However, sudo also needs to carry over the environment variables once the venv is started.
# This works:
# >>> source ./venv/bin/activate
# >>> sudo -E python3 netscanner.py
# This doesn't work:
# >>> sudo python3 netscanner.py
# because it doesn't find the python-nmap module in the sys.path.
# The sys.path modification makes it easier to run with cron (i.e. sudo crontab -e)
NMAP_PATH = 'venv/lib/python3.7/site-packages/nmap'

# IPs or IP range to scan. See nmap documentation for more details.
NET_ADDR = '192.168.1.0/24'
# nmap scan arguments
NMAP_ARGS = '-F -sN -PE -PA21,22,23,80,3389'
# Seems to throw errors reading the mac if you don't exclude the scanning device's IP
# Make sure to add the scanning device's IP address which is hopefully static
# Comma separated list of IPs to exclude
EXCLUDE_IPS = '<this computer''s ip address>'

# Path to your nmap installation if you're on Windows (I used this for testing)
WIN_NMAP_PATH = 'C:\\Program Files (x86)\\Nmap'

# Notifications configuration; currently only setup for gmail
EMAIL_ADDR = "<email address used to send notifications>"
EMAIL_PASS = "<gmail app password>"
NOTIFY_EMAIL = "<email address that receives notifications>"
