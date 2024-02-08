import tkinter as tk
from tkinter import filedialog
import serial.tools.list_ports
from tkinter import ttk
import threading
import serial
import time
from keras.models import load_model
import numpy as np
from sklearn.preprocessing import MinMaxScaler

# Define ser
ser = None

# Make file_path and model_path global
file_path = ''
model_path = ''
com_port = ''

# Define path_entry
path_entry = None
model_entry = None
result_label = None

# Define the scaler for input normalization
scaler_X = MinMaxScaler()
scaler_y = MinMaxScaler()

def browse_file():
    global file_path
    file_path = filedialog.askopenfilename()
    path_entry.delete(0, tk.END)
    path_entry.insert(tk.END, file_path)

def browse_model():
    global model_path
    model_path = filedialog.askopenfilename(initialdir='./models/', title='Select Model', filetypes=(('Model Files', '*.h5'),))
    model_entry.delete(0, tk.END)
    model_entry.insert(tk.END, model_path)

def refresh_com_ports():
    com_ports = [port.device for port in serial.tools.list_ports.comports()]
    com_port_dropdown['values'] = com_ports

def select_com_port(event):
    global com_port
    com_port = com_port_dropdown.get()

def predict_loop():
    global model_path, ser
    ser = serial.Serial(com_port, 9600, timeout=1)
    time.sleep(2)

    last_request_time = time.time()  # Initialize last request time
    while True:
        current_time = time.time()

        # Send a request to Arduino only once every minute
        if current_time - last_request_time >= 60:
            last_request_time = current_time

            # Send a request to Arduino
            ser.write(b'1')  # Send '1' as a request

            # Read the response from Arduino
            response = ser.readline().decode('utf-8').strip()

            # Process the response
            try:
                temperature, humidity = response.split(',')
                temperature = float(temperature)
                humidity = float(humidity)
                temperature = 30.6
                humidity = 60.9

                # Load the saved model
                model = load_model(model_path)

                # Use the temperature and humidity as model input
                input_values = [humidity, temperature]

                # Scale the new data using the same scaler used for the training data
                X_new_scaled = scaler_X.transform(np.array(input_values).reshape(1, -1))

                # Use the model to predict the output for the new data
                y_new_scaled = model.predict(X_new_scaled)

                # Inverse transform the scaled output to get the actual value
                y_new = scaler_y.inverse_transform(y_new_scaled)

                # Send the prediction back to the Arduino
                ser.write(str(y_new[0]).encode('utf-8'))

                # Print the predicted value
                print("Predicted Value:", y_new[0])
            except:
                print("Invalid data received from Arduino.")

        time.sleep(1)  # Wait for 1 second before sending the next request


def start_server():
    global result_label, ser

    # Check if file_path, model_path, and com_port are set
    if not model_path:
        result_label.config(text="Model file not selected")
        return
    if not com_port:
        result_label.config(text="COM port not selected")
        return

    # Create a text box to display the serial monitor
    monitor_label = tk.Label(root, text="Serial Monitor:")
    monitor_label.grid(column=0, row=5, padx=10, pady=10)
    monitor_text = tk.Text(root, height=10, width=50)
    monitor_text.grid(column=1, row=5, padx=10, pady=10)

    # Define the serial monitor function
    def serial_monitor():
        while True:
            try:
                # Read the serial monitor and print raw data coming from Arduino
                data = ser.readline().decode('utf-8')
                monitor_text.insert(tk.END, data + '\n')
                monitor_text.see(tk.END)
            except:
                pass

    # Start the serial monitor in a separate thread
    threading.Thread(target=serial_monitor, daemon=True).start()

    # Start the prediction loop in a separate thread
    threading.Thread(target=predict_loop, daemon=True).start()


root = tk.Tk()
root.geometry("500x400")
root.title("Arduino ML")

# Create a label for the file path
path_label = tk.Label(root, text="Select CSV File:")
path_label.grid(column=0, row=0, padx=10, pady=10)

# Create a text box for the file path
path_entry = tk.Entry(root, width=50)
path_entry.grid(column=1, row=0, padx=10, pady=10)

# Create a button to browse for the file
browse_button = tk.Button(root, text="Browse", command=browse_file)
browse_button.grid(column=2, row=0, padx=10, pady=10)

# Create a label for the model path
model_label = tk.Label(root, text="Select Model File:")
model_label.grid(column=0, row=1, padx=10, pady=10)

# Create a text box for the model path
model_entry = tk.Entry(root, width=50)
model_entry.grid(column=1, row=1, padx=10, pady=10)

# Create a button to browse for the model
browse_button = tk.Button(root, text="Browse", command=browse_model)
browse_button.grid(column=2, row=1, padx=10, pady=10)

# Create a label for the COM port
com_port_label = tk.Label(root, text="Select COM Port:")
com_port_label.grid(column=0, row=2, padx=10, pady=10)

# Create a dropdown for the COM port
com_port_dropdown = ttk.Combobox(root, width=50)
com_port_dropdown.grid(column=1, row=2, padx=10, pady=10)
refresh_com_ports()
com_port_dropdown.bind("<<ComboboxSelected>>", select_com_port)

# Create a button to refresh the COM ports
refresh_button = tk.Button(root, text="Refresh", command=refresh_com_ports)
refresh_button.grid(column=2, row=2, padx=10, pady=10)

# Create a button to start the server
start_button = tk.Button(root, text="Start Server", command=start_server)
start_button.grid(column=1, row=3, padx=10, pady=10)

# Create a label for the result
result_label = tk.Label(root, text="Predicted Output: ")
result_label.grid(column=1, row=4, padx=10, pady=10)

root.mainloop()
