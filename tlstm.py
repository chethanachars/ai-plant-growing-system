#take two inputs and predict three outputs using pretrained model, using tkinter create a gui window with browse model button and two fields to input data and predict the output and show in the window
import tkinter as tk
from tkinter import filedialog
import pandas as pd
import numpy as np
from sklearn.preprocessing import MinMaxScaler
from keras.models import load_model

# Create a window
window = tk.Tk()

# Function for browsing the model file
def browse_model():
    global model_path
    model_path = filedialog.askopenfilename()
    model_entry.delete(0, tk.END)
    model_entry.insert(0, model_path)

# Function for predicting the output
def predict_output():
    # Load the saved model
    model = load_model(model_path)

    # Take the inputs
    X_new = np.array([[float(temperature_entry.get()), float(humidity_entry.get())]])

    # Scale the new data using the same scaler used for the training data
    scaler_X = MinMaxScaler()
    X_new_scaled = scaler_X.fit_transform(X_new)

    # Reshape the input data into 3D tensor with shape (n_samples, timesteps, n_features)
    X_new_reshaped = X_new_scaled.reshape((X_new_scaled.shape[0], 1, X_new_scaled.shape[1]))

    # Use the model to predict the output for the new data
    y_new_scaled = model.predict(X_new_reshaped)

    # Inverse transform the scaled output to get the actual values
    scaler_y = MinMaxScaler()
    scaler_y.min_, scaler_y.scale_ = scaler_X.min_[0], scaler_X.scale_[0]
    y_new = scaler_y.inverse_transform(y_new_scaled)


    # Print the predicted output
    rain_entry.delete(0, tk.END)
    rain_entry.insert(0, y_new[0][0])
    soil_temp_entry.delete(0, tk.END)
    soil_temp_entry.insert(0, y_new[0][1])
    soil_moisture_entry.delete(0, tk.END)
    soil_moisture_entry.insert(0, y_new[0][2])

# Create a label for the model path
model_label = tk.Label(window, text='Model Path:')
model_label.grid(row=0, column=0, padx=5, pady=5)

# Create a entry for the model path
model_entry = tk.Entry(window, width=50)
model_entry.grid(row=0, column=1, padx=5, pady=5)

# Create a button for browsing the model file
browse_button = tk.Button(window, text='Browse', command=browse_model)
browse_button.grid(row=0, column=2, padx=5, pady=5)

# Create a label for temperature
temperature_label = tk.Label(window, text='Temperature:')
temperature_label.grid(row=1, column=0, padx=5, pady=5)

# Create a entry for temperature
temperature_entry = tk.Entry(window, width=50)
temperature_entry.grid(row=1, column=1, padx=5, pady=5)

# Create a label for humidity
humidity_label = tk.Label(window, text='Humidity:')
humidity_label.grid(row=2, column=0, padx=5, pady=5)

# Create a entry for humidity
humidity_entry = tk.Entry(window, width=50)
humidity_entry.grid(row=2, column=1, padx=5, pady=5)

# Create a button for predicting the output
predict_button = tk.Button(window, text='Predict', command=predict_output)
predict_button.grid(row=3, column=1, padx=5, pady=5)

# Create a label for rain
rain_label = tk.Label(window, text='Rain:')
rain_label.grid(row=4, column=0, padx=5, pady=5)

# Create a entry for rain
rain_entry = tk.Entry(window, width=50)
rain_entry.grid(row=4, column=1, padx=5, pady=5)

# Create a label for soil temperature
soil_temp_label = tk.Label(window, text='Soil Temperature:')
soil_temp_label.grid(row=5, column=0, padx=5, pady=5)

# Create a entry for soil temperature
soil_temp_entry = tk.Entry(window, width=50)
soil_temp_entry.grid(row=5, column=1, padx=5, pady=5)

# Create a label for soil moisture
soil_moisture_label = tk.Label(window, text='Soil Moisture:')
soil_moisture_label.grid(row=6, column=0, padx=5, pady=5)

# Create a entry for soil moisture
soil_moisture_entry = tk.Entry(window, width=50)
soil_moisture_entry.grid(row=6, column=1, padx=5, pady=5)

# Run the window
window.mainloop()
