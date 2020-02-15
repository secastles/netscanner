# netscanner
A simple script to:
- Automate scanning of local network with nmap
- Store found hosts/mac addresses in a SQLite database
- Send email notification when new hosts are found

Prerequisites: nmap and python-nmap

Must be run using sudo in order to provide necessary rights to nmap.

Example running from console (verbose logging):
`sudo python3 netscanner.py`

Example running in cron (every 15 minutes):

`sudo crontab -e`

`*/15 * * * * /home/netscanner/venv/bin/python3 /home/netscanner/netscanner.py`
 
 SQLite database is created and stored in same folder as the script.
 
 Rename `settings_example.py` to `settings.py`
