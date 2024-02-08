import tkinter as tk
import serial.tools.list_ports
import csv
#import missing libraries or undefined functions veriables in this code
import queue
import threading


class SerialPortApp:
    def __init__(self, master):
        self.master = master
        self.master.geometry("400x300")
        self.master.resizable(False, False)

        # Create variables
        self.com_port_var = tk.StringVar()
        self.baud_rate_var = tk.IntVar(value=9600)
        self.status_var = tk.StringVar(value="Waiting for input")

        # Create widgets
        self.com_port_label = tk.Label(master, text="COM Port:")
        self.com_port_dropdown = None
        self.baud_rate_label = tk.Label(master, text="Baud Rate:")
        self.baud_rate_entry = tk.Entry(master, textvariable=self.baud_rate_var)
        self.start_button = tk.Button(master, text="Start", command=self.start_data_collection)
        self.stop_button = tk.Button(master, text="Stop", command=self.stop_data_collection)
        self.status_label = tk.Label(master, textvariable=self.status_var)
        self.refresh_button = tk.Button(master, text="Refresh Ports", command=self.refresh_ports)

        # Add widgets to grid
        self.com_port_label.grid(row=0, column=0, padx=5, pady=5, sticky="w")
        self.baud_rate_label.grid(row=1, column=0, padx=5, pady=5, sticky="w")
        self.com_port_dropdown = tk.OptionMenu(master, self.com_port_var, *self.list_serial_ports())
        if self.com_port_dropdown['menu'].index("end") > 0:
            self.com_port_dropdown.grid(row=0, column=1, padx=5, pady=5)
        else:
            self.status_var.set("No serial ports available")
        self.baud_rate_entry.grid(row=1, column=1, padx=5, pady=5)
        self.start_button.grid(row=2, column=0, padx=5, pady=5)
        self.stop_button.grid(row=2, column=1, padx=5, pady=5)
        self.status_label.grid(row=3, column=0, columnspan=2, padx=5, pady=5)
        self.refresh_button.grid(row=4, column=0, padx=5, pady=5)

        # Create serial thread and data queue
        self.serial_thread = None
        self.data_queue = None

    def list_serial_ports(self):
        """Return a list of available serial ports"""
        return [port.device for port in serial.tools.list_ports.comports()]

    def start_data_collection(self):
        """Start collecting data from the selected serial port"""
        port = self.com_port_var.get()
        baud_rate = self.baud_rate_var.get()

        # Create data queue and start serial thread
        self.data_queue = queue.Queue()
        self.serial_thread = SerialThread(port, baud_rate, self.data_queue)
        self.serial_thread.start()

        # Disable start button and com port dropdown
        self.start_button.config(state="disabled")
        self.com_port_dropdown.config(state="disabled")

        self.status_var.set(f"Collecting data from {port} at {baud_rate} baud...")

    def stop_data_collection(self):
        """Stop collecting data and save to file"""
        self.serial_thread.stop()
        self.serial_thread.join()

        # Enable start button and com port dropdown
        self.start_button.config(state="normal")
        self.com_port_dropdown.config(state="normal")

        self.status_var.set("Data collection stopped")

        # Process any new data that has been collected
        try:
            while True:
                data = self.data_queue.get_nowait()
                self.status_label.config(text=data)
        except queue.Empty:
            pass

        # Save data to CSV file
        self.save_to_csv()

    def save_to_csv(self):
        """Save collected data to CSV file"""
        data = []
        try:
            while True:
                data.append(self.data_queue.get_nowait())
        except queue.Empty:
            pass

        if data:
            filename = f"data_{self.com_port_var.get()}_{self.baud_rate_var.get()}.csv"
            with open(filename, "w", newline="") as f:
                writer = csv.writer(f)
                writer.writerow(["Data"])
                writer.writerows([[d] for d in data])

    def refresh_ports(self):
        """Refresh the list of available serial ports"""
        self.com_port_dropdown['menu'].delete(0, "end")
        ports = self.list_serial_ports()
        if ports:
            for port in ports:
                self.com_port_dropdown['menu'].add_command(label=port, command=tk._setit(self.com_port_var, port))
        else:
            self.status_var.set("No serial ports available")

    def on_closing(self):
        """Stop the serial thread and close the application"""
        if self.serial_thread:
            self.serial_thread.stop()
            self.serial_thread.join()
        self.master.destroy()


class SerialThread(threading.Thread):
    def __init__(self, port, baud_rate, data_queue):
        super().__init__()
        self.port = port
        self.baud_rate = baud_rate
        self.data_queue = data_queue
        self.stop_event = threading.Event()
        self.serial_port = None

    def run(self):
        try:
            self.serial_port = serial.Serial(self.port, self.baud_rate, timeout=1)
            while not self.stop_event.is_set():
                data = self.serial_port.readline().strip().decode()
                if data:
                    self.data_queue.put(data)
        except serial.SerialException as e:
            print(e)
        finally:
            if self.serial_port and self.serial_port.is_open:
                self.serial_port.close()

    def stop(self):
        self.stop_event.set()
