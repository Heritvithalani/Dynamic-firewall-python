import os
import subprocess

def setup_firewall():
    """Sets up the basic iptables firewall rules."""
    # Flush existing rules
    subprocess.run(["iptables", "-F"], check=True)
    subprocess.run(["iptables", "-X"], check=True)
    subprocess.run(["iptables", "-Z"], check=True)

    # Default policies
    subprocess.run(["iptables", "-P", "INPUT", "DROP"], check=True)
    subprocess.run(["iptables", "-P", "FORWARD", "DROP"], check=True)
    subprocess.run(["iptables", "-P", "OUTPUT", "ACCEPT"], check=True)

    # Allow loopback interface
    subprocess.run(["iptables", "-A", "INPUT", "-i", "lo", "-j", "ACCEPT"], check=True)

    # Allow established and related connections
    subprocess.run(["iptables", "-A", "INPUT", "-m", "state", "--state", "ESTABLISHED,RELATED", "-j", "ACCEPT"], check=True)

    # Save rules
    os.makedirs("/etc/iptables", exist_ok=True)
    with open("/etc/iptables/rules.v4", "w") as f:
        subprocess.run(["iptables-save"], stdout=f)

    print("Firewall setup complete.")

if __name__ == "__main__":
    setup_firewall()
