import tkinter as tk
from tkinter import messagebox


class ReconCenter:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Nmap Scan GUI")

        self.create_widgets()

    def create_widgets(self):
        # Create a parameter box to input scan parameters
        parameter_label = tk.Label(self.root, text="Scan Parameters:")
        parameter_label.pack()

        self.parameter_box = tk.Entry(self.root, width=50)
        self.parameter_box.pack()

        # Create buttons for each scan type
        scan_syn_button = tk.Button(
            self.root, text="SYN Scan", command=self.scan_syn)
        scan_syn_button.pack(pady=5)

        scan_tcp_connect_button = tk.Button(
            self.root, text="TCP Connect Scan", command=self.scan_tcp_connect)
        scan_tcp_connect_button.pack(pady=5)

        scan_udp_button = tk.Button(
            self.root, text="UDP Scan", command=self.scan_udp)
        scan_udp_button.pack(pady=5)

        scan_comprehensive_button = tk.Button(
            self.root, text="Comprehensive Scan", command=self.scan_comprehensive)
        scan_comprehensive_button.pack(pady=5)

        # Add more buttons for other scan types

    def scan_syn(self):
        messagebox.showinfo(
            "SYN Scan(-sS)", "A stealthy scan that sends SYN packets to the target ports. It determines which ports are open based on the responses received.")

    def scan_tcp_connect(self):
        messagebox.showinfo("TCP Connect Scan(-sT)",
                            "A full TCP connection scan that actively opens a connection to each target port. It is more detectable but can provide more accurate results.")

    def scan_udp(self):
        messagebox.showinfo(
            "UDP Scan(-sU)", "Scans for open UDP ports, which are often used for services like DNS, SNMP, and DHCP.")

    def scan_comprehensive(self):
        messagebox.showinfo("Comprehensive Scan(-sC)",
                            "Also known as the default or script scan, this scan runs a set of scripts from the Nmap Scripting Engine (NSE) against the target to identify common vulnerabilities and enumerate services.")
