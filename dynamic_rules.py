import os
import re
import smtplib
from email.message import EmailMessage
from subprocess import run

# Path to required files
LOG_FILE = "/var/log/auth.log"
BLOCKED_IPS_FILE = "/home/your_user/firewall_project/data/blocked_ips.txt"
WHITELIST = ["127.0.0.1", "192.168.1.1"]

def send_alert(ip):
    """Sends an email alert for blocked IPs."""
    msg = EmailMessage()
    msg.set_content(f"Alert: Suspicious activity detected and blocked from IP {ip}")
    msg["Subject"] = "Firewall Alert"
    msg["From"] = "your_email@example.com"
    msg["To"] = "admin@example.com"

    try:
        with smtplib.SMTP("smtp.gmail.com", 587) as server:
            server.starttls()
            server.login("your_email@example.com", "your_password")
            server.send_message(msg)
        print(f"Alert sent for IP {ip}")
    except Exception as e:
        print(f"Failed to send email: {e}")

def block_ip(ip):
    """Blocks an IP using iptables and logs it."""
    with open(BLOCKED_IPS_FILE, "a+") as f:
        f.seek(0)
        if ip in f.read():
            print(f"IP {ip} is already blocked.")
            return
        f.write(f"{ip}\n")
    
    run(["iptables", "-A", "INPUT", "-s", ip, "-j", "DROP"], check=True)
    print(f"Blocked IP: {ip}")
    send_alert(ip)

def monitor_logs():
    """Monitors logs for suspicious activity and blocks IPs."""
    with open(LOG_FILE, "r") as log:
        for line in log:
            match = re.search(r"Failed password.*from (\d+\.\d+\.\d+\.\d+)", line)
            if match:
                ip = match.group(1)
                if ip not in WHITELIST:
                    block_ip(ip)

def firewall_menu():
    """Interactive menu for firewall management."""
    while True:
        print("\nFirewall Menu:")
        print("1. Block IP")
        print("2. Unblock IP")
        print("3. View Logs")
        print("4. Exit")
        choice = input("Enter choice: ")

        if choice == "1":
            ip = input("Enter IP to block: ")
            block_ip(ip)
        elif choice == "2":
            ip = input("Enter IP to unblock: ")
            run(["iptables", "-D", "INPUT", "-s", ip, "-j", "DROP"], check=True)
            print(f"Unblocked IP: {ip}")
        elif choice == "3":
            with open(BLOCKED_IPS_FILE, "r") as f:
                print("Blocked IPs:")
                print(f.read())
        elif choice == "4":
            print("Exiting firewall menu.")
            break
        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    firewall_menu()
