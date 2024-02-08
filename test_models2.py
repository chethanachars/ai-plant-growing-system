import tkinter as tk
from tkinter import filedialog
import pandas as pd
from sklearn.tree import DecisionTreeRegressor
from sklearn.metrics import mean_squared_error, r2_score
from sklearn.model_selection import train_test_split
import pickle
import serial.tools.list_ports
from tkinter import ttk


# make file_path and model_path global
file_path = ''
model_path = ''
com_port = ''

def browse_file():
    global file_path
    file_path = filedialog.askopenfilename()
    path_entry.delete(0, tk.END)
    path_entry.insert(tk.END, file_path)

def browse_model():
    global model_path
    model_path = filedialog.askopenfilename(initialdir='./models/', title='Select Model', filetypes=(('Model Files', '*.sav'),))
    model_entry.delete(0, tk.END)
    model_entry.insert(tk.END, model_path)

def test_model():
    # read the input values
    try:
        input_values = [float(x.strip()) for x in input_entry.get().split(',')]
    except:
        result_label.config(text="Invalid input format")
        return

    # load the model
    try:
        with open(model_path, 'rb') as file:
            model = pickle.load(file)
    except:
        result_label.config(text="Model file not found or invalid model file")
        return

    # make the prediction
    try:
        prediction = model.predict([input_values])
        result_label.config(text="Predicted Output: {}".format(prediction[0]))
    except:
        result_label.config(text="Error in making prediction")

def refresh_com_ports():
    com_ports = [port.device for port in serial.tools.list_ports.comports()]
    com_port_dropdown['values'] = com_ports

def select_com_port(event):
    global com_port
    com_port = com_port_dropdown.get()

def start_server():
    # check if file_path, model_path, and com_port are set
    if not file_path:
        result_label.config(text="Data file not selected")
        return
    if not model_path:
        result_label.config(text="Model file not selected")
        return
    if not com_port:
        result_label.config(text="COM port not selected")
        return

    # initialize serial communication
    try:
        ser = serial.Serial(com_port, 9600)
    except:
        result_label.config(text="Failed to initialize serial communication")
        return

    # load the model
    try:
        with open(model_path, 'rb') as file:
            model = pickle.load(file)
    except:
        result_label.config(text="Model file not found or invalid model file")
        return

    # continuously read input from serial port and make predictions
    while True:
        try:
            # read input from serial port
            input_str = ser.readline().decode('utf-8').strip()
            input_values = [float(x.strip()) for x in input_str.split(',')]

            # make the prediction
            prediction = model.predict([input_values])

            # send the prediction back to the arduino
            ser.write(str(prediction[0]).encode('utf-8'))

            # update the result label
            result_label.config(text="Predicted Output: {}".format(prediction[0]))
        except:
            result_label.config(text="Error in making prediction")

root = tk.Tk()
root.geometry("500x400")
root.title("Model Prediction Server")

# Create a label for file path
path_label = tk.Label(root, text="Select Data File: ")
path_label.grid(column=0, row=0, padx=10, pady=10)

# Create a text entry box for file path
path_entry = tk.Entry(root, width=50)
path_entry.grid(column=1, row=0, padx=10, pady=10)

# Create a button to browse file
browse_button = tk.Button(root, text="Browse", command=browse_file)
browse_button.grid(column=2, row=0, padx=10, pady=10)

# Create a label for model path
model_label = tk.Label(root, text="Select Model File: ")
model_label.grid(column=0, row=1, padx=10, pady=10)

# Create a text entry box for model path
model_entry = tk.Entry(root, width=50)
model_entry.grid(column=1, row=1, padx=10, pady=10)

# Create a button to browse model
browse_button = tk.Button(root, text="Browse", command=browse_model)
browse_button.grid(column=2, row=1, padx=10, pady=10)

# Create a label for input values
input_label = tk.Label(root, text="Input Values: ")
input_label.grid(column=0, row=2, padx=10, pady=10)

# Create a text entry box for input values
input_entry = tk.Entry(root, width=50)
input_entry.grid(column=1, row=2, padx=10, pady=10)

# Create a button to test model
test_button = tk.Button(root, text="Test Model", command=test_model)
test_button.grid(column=2, row=2, padx=10, pady=10)

# Create a label for result
result_label = tk.Label(root, text="Result: ")
result_label.grid(column=0, row=3, padx=10, pady=10)

# Create a button to refresh com ports
refresh_button = tk.Button(root, text="Refresh COM Ports", command=refresh_com_ports)
refresh_button.grid(column=0, row=4, padx=10, pady=10)

# Create a dropdown for com ports
com_port_dropdown = ttk.Combobox(root, width=50)
com_port_dropdown.grid(column=1, row=4, padx=10, pady=10)
com_port_dropdown.bind("<<ComboboxSelected>>", select_com_port)

# Create a button to start server
start_button = tk.Button(root, text="Start Server", command=start_server)
start_button.grid(column=2, row=4, padx=10, pady=10)

root.mainloop()
