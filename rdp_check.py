import argparse
import subprocess
import ipaddress
import logging
import time
from termcolor import colored


def check_rdp_connection(target, domain, username, password, debug=False):
    
    command = [
        'xfreerdp',
        f'/v:{target}',
        f'/d:{domain}',
        f'/u:{username}',
        f'/p:{password}',
        '/cert-ignore',
        '+auth-only'
    ]

    if debug:
        logging.info(f"Executing command: {' '.join(command)}")

    try:
        result = subprocess.run(command, capture_output=True, timeout=10)

        if debug:
            print(colored(f"stdout:\n{result.stdout.decode()}", 'yellow'))
            print(colored(f"stderr:\n{result.stderr.decode()}", 'yellow'))

        
        if "exit status 0" in result.stdout.decode() or \
           "Authentication only, exit status 0" in result.stdout.decode() or \
           "freerdp_abort_connect:freerdp_set_last_error_ex ERRCONNECT_CONNECT_CANCELLED [0x0002000B]" in result.stderr.decode():
            print(colored(f'[RDP allowed] {target}: Successful authentication for user {username}', 'green'))
            return True
        else:
            print(colored(f'[RDP error] {target}: Access denied', 'red'))
            return False

    except subprocess.TimeoutExpired:
        print(colored(f'[Timeout] {target}: Connection timed out after 10 seconds', 'yellow'))
        return False
    except Exception as e:
        print(f"Error connecting to {target}: {str(e)}")
        return False


def main():
    parser = argparse.ArgumentParser(description="RDP connection checker.")
    parser.add_argument('-t', '--target', help="IP address or DNS name of the target host.")
    parser.add_argument('-T', '--targets', help="File containing a list of IP addresses, subnets in CIDR format, or DNS names.")
    parser.add_argument('-u', '--username', required=True, help="Username for RDP login.")
    parser.add_argument('-p', '--password', required=True, help="Password for RDP login.")
    parser.add_argument('-d', '--domain', required=True, help="FQDN of the domain.")
    parser.add_argument('--debug', action='store_true', help="Enable debug logging.")
    args = parser.parse_args()

    # Enable logging
    logging.basicConfig(level=logging.DEBUG if args.debug else logging.INFO)

    targets = []
    if args.target:
        targets.append(args.target)
    elif args.targets:
        try:
            with open(args.targets, 'r') as f:
                for line in f:
                    line = line.strip()
                    if '/' in line:  # Если это подсеть
                        network = ipaddress.ip_network(line, strict=False)
                        targets.extend(str(ip) for ip in network.hosts())
                    else:
                        targets.append(line)
        except ValueError as e:
            logging.error(f"Invalid subnet or IP address: {e}")
            return
        except FileNotFoundError:
            logging.error(f"File not found: {args.targets}")
            return

    for target in targets:
        logging.info(f"Checking RDP for {target}...")
        success = check_rdp_connection(
            target, args.domain, args.username, args.password, args.debug)
        time.sleep(1)  # Добавляем паузу между проверками

if __name__ == "__main__":
    main()
