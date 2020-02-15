import logging
import os
import sys
import traceback
from pathlib import Path

# Deal with running the script with sudo (need to add the nmap dir to the sys.path)
import settings as s
cur_dir = os.path.abspath(os.path.dirname(__file__))
sys.path.append(str(Path(cur_dir) / s.NMAP_PATH))

import nmap
import db_sqlite as db
import notifications


# Setup logging
LOG_LEVEL = "DEBUG"
logging.basicConfig(level=LOG_LEVEL, format='%(asctime)s - %(levelname)s - [%(name)s] - %(message)s')
logger = logging.getLogger()

# Necessary for Windows to get nmap running
if os.name == 'nt':
    os.environ["PATH"] += os.pathsep + s.WIN_NMAP_PATH


def run_port_scan():
    try:
        nm = nmap.PortScanner()
        nm.scan(s.NET_ADDR, arguments=s.NMAP_ARGS + " --exclude " + s.EXCLUDE_IPS)
        logger.info(nm.command_line())
    except:
        logger.error("Unexpected error with nmap: {}".format(sys.exc_info()[0]))
        logger.error("Traceback follows:")
        logger.error(traceback.print_exc())
        logger.warning("Shutting down after error.")
        raise
    else:
        host_count = 0
        notification_payload = "This is your regular test of the process."
        logger.info("nmap found the following hosts:")
        try:
            for host in nm.all_hosts():
                # Write out to logs
                host_count += 1
                logger.info('----------------------------------------------------')
                logger.info('Host : %s (%s)' % (host, nm[host].hostname()))
                logger.info('State : %s' % nm[host].state())
                logger.info('MAC : %s' % nm[host]['addresses']['mac'])
                for proto in nm[host].all_protocols():
                    logger.info('Protocol : %s' % proto)

                    lport = nm[host][proto].keys()
                    for port in sorted(lport):
                        logger.info('    port : %s\tstate : %s' % (port, nm[host][proto][port]['state']))
                logger.info('----------------------------------------------------')

                # Insert host into database, but check if exists first
                if not db.host_exists(nm[host]['addresses']['mac']):
                    # Build notification payload
                    notification_payload = notification_payload + "\n" + nm[host]['addresses']['mac'] \
                        + "  -  " + nm[host].hostname()
                    # Insert new db record
                    db.insert_host(nm[host]['addresses']['mac'], nm[host].hostname())
        except:
            logger.error("Unexpected error with writing nmap logs: {}".format(sys.exc_info()[0]))
            # Even if we hit an error we still want to try to send the notification
            if not notification_payload == "":
                notifications.send_notifications("New hosts found on network", notification_payload)
            raise
        else:
            logger.info("Found {} total hosts.".format(host_count))
            return notification_payload


def main():
    logger.info("Scanning...")
    try:
        notification_payload = run_port_scan()
        if not notification_payload == "":
            notifications.send_notifications("New hosts found on network", notification_payload)
        logger.info("Scan complete.")
    except:
        logger.error("Unexpected error: {}".format(sys.exc_info()[0]))
        db.close_connection()
        notifications.send_notifications("There was an error in scanner", traceback.print_exc())
        sys.exit(0)


if __name__ == '__main__':
    main()
