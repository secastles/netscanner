# netscanner
A simple script to:
- Automate scanning of local network with nmap
- Store found hosts/mac addresses in a SQLite database
- Send email notification when new hosts are found

Prerequisite: nmap and python-nmap

Must be run with sudo -E to preserve environment path

e.g. `sudo -E python3 netscanner.py`
