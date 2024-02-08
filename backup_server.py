import tkinter as tk
from tkinter import filedialog
import pandas as pd
from sklearn.tree import DecisionTreeRegressor
from sklearn.metrics import mean_squared_error, r2_score
from sklearn.model_selection import train_test_split
import pickle
import serial.tools.list_ports
from tkinter import ttk
import threading
import serial
import numpy as np
from sklearn.preprocessing import MinMaxScaler
from tensorflow.keras.models import load_model
import time
#define ser
#ser = serial.Serial()
#define scaler_y
scaler_y = MinMaxScaler()


# make file_path and model_path global
file_path = ''
model_path = ''
com_port = ''
model = None

#define path_entry
path_entry = None
model_entry = None
result_label = None

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

def test_model(input_values):
    global model
    # load the model
    try:
        with open(model_path, 'rb') as file:
            model = pickle.load(file)
    except:
        return None

    # make the prediction
    try:
        prediction = model.predict([input_values])
        return prediction[0]
    except:
        return None

def refresh_com_ports():
    com_ports = [port.device for port in serial.tools.list_ports.comports()]
    com_port_dropdown['values'] = com_ports

def select_com_port(event):
    global com_port
    com_port = com_port_dropdown.get()
    #global ser
    #define ser
    #ser = serial.Serial(com_port, 9600)

def predict_loop():
    global model, model_path, scaler_y
    global ser
    #define ser
    ser = serial.Serial(com_port, 9600, timeout=1)
    time.sleep(2)
    while True:
        #ping arduino to send data by sending 1
        
        '''input_values = [float(value) for value in input_values]
        #print the input values
        print(input_values)
        # Load the saved model
        model = load_model(model_path)

        # Scale the new data using the same scaler used for the training data
        scaler_X = MinMaxScaler()
        X_new_scaled = scaler_X.fit_transform(np.array(input_values).reshape(-1, 1))

        # Reshape the input data into 3D tensor with shape (n_samples, timesteps, n_features)
        X_new_reshaped = X_new_scaled.reshape((X_new_scaled.shape[0], 1, X_new_scaled.shape[1]))

        # Use the model to predict the output for the new data
        y_new_scaled = model.predict(X_new_reshaped)

        # Inverse transform the scaled output to get the actual values
        y_new = scaler_y.inverse_transform(y_new_scaled)

        # send the prediction back to the arduino
        ser.write(str(y_new).encode('utf-8'))

        # print the predicted value
        print(y_new)'''


def start_server():
    global result_label
    # check if file_path, model_path, and com_port are set
    if not model_path:
        result_label.config(text="Model file not selected")
        return
    if not com_port:
        result_label.config(text="COM port not selected")
        return

    # initialize serial communication
    '''try:
        ser = serial.Serial(com_port, 9600)
    except:
        result_label.config(text="Failed to initialize serial communication")
        return'''

    # create a text box to display the serial monitor
    monitor_label = tk.Label(root, text="Serial Monitor:")
    monitor_label.grid(column=0, row=5, padx=10, pady=10)
    monitor_text = tk.Text(root, height=10, width=50)
    monitor_text.grid(column=1, row=5, padx=10, pady=10)

    # define the serial monitor function
    def serial_monitor():
        while True:
            try:
                #read the serial monitor and print raw data coming from arduino
                data = ser.readline().decode('utf-8')
                monitor_text.insert(tk.END, data + '\n')    
                monitor_text.see(tk.END)
            except:
                pass

    # start the serial monitor in a separate thread
    threading.Thread(target=serial_monitor, daemon=True).start()

    # start the prediction loop in a separate thread
    threading.Thread(target=predict_loop, daemon=True).start()



root = tk.Tk()
root.geometry("500x400")
root.title("Arduino ML")

# create a label for the file path
path_label = tk.Label(root, text="Select CSV File:")
path_label.grid(column=0, row=0, padx=10, pady=10)

# create a text box for the file path
path_entry = tk.Entry(root, width=50)
path_entry.grid(column=1, row=0, padx=10, pady=10)

# create a button to browse for the file
browse_button = tk.Button(root, text="Browse", command=browse_file)
browse_button.grid(column=2, row=0, padx=10, pady=10)

# create a label for the model path
model_label = tk.Label(root, text="Select Model File:")
model_label.grid(column=0, row=1, padx=10, pady=10)

# create a text box for the model path
model_entry = tk.Entry(root, width=50)
model_entry.grid(column=1, row=1, padx=10, pady=10)

# create a button to browse for the model
browse_button = tk.Button(root, text="Browse", command=browse_model)
browse_button.grid(column=2, row=1, padx=10, pady=10)

# create a label for the com port
com_port_label = tk.Label(root, text="Select COM Port:")
com_port_label.grid(column=0, row=2, padx=10, pady=10)

# create a dropdown for the com port
com_port_dropdown = ttk.Combobox(root, width=50)
com_port_dropdown.grid(column=1, row=2, padx=10, pady=10)
refresh_com_ports()
com_port_dropdown.bind("<<ComboboxSelected>>", select_com_port)

# create a button to refresh the com ports
refresh_button = tk.Button(root, text="Refresh", command=refresh_com_ports)
refresh_button.grid(column=2, row=2, padx=10, pady=10)

# create a button to start the server
start_button = tk.Button(root, text="Start Server", command=start_server)
start_button.grid(column=1, row=3, padx=10, pady=10)

# create a label for the result
result_label = tk.Label(root, text="Predicted Output: ")
result_label.grid(column=1, row=4, padx=10, pady=10)

root.mainloop()

