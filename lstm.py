import pandas as pd
import numpy as np
from sklearn.preprocessing import MinMaxScaler
from sklearn.model_selection import train_test_split
from keras.models import Sequential
from keras.layers import LSTM, Dense
from keras.callbacks import ModelCheckpoint
import tkinter as tk
from tkinter import filedialog, messagebox

# Create a Tkinter window
window = tk.Tk()
window.title("LSTM Model Training")
window.geometry('300x150')

# Function to select the dataset file
def select_file():
    global dataset_path
    dataset_path = filedialog.askopenfilename(initialdir = "/", title = "Select file", filetypes = (("CSV files", "*.csv"), ("All files", "*.*")))
    if dataset_path:
        messagebox.showinfo("Dataset Selected", "Dataset selected successfully!")

# Function to train the LSTM model and save it
def train_model():
    # Load the dataset
    try:
        df = pd.read_csv(dataset_path)
    except:
        messagebox.showerror("Error", "Please select a valid dataset file!")
        return

    # Remove the time attribute
    df = df.drop(columns=['time'])

    # Split the dataset into input (X) and output (y) variables
    X = df[['temperature_2m', 'relativehumidity_2m']].values
    y = df[['rain', 'soil_temperature_0_to_7cm', 'soil_moisture']].values

    # Scale the data
    scaler_X = MinMaxScaler()
    X_scaled = scaler_X.fit_transform(X)

    scaler_y = MinMaxScaler()
    y_scaled = scaler_y.fit_transform(y)

    # Split the data into train and test sets
    X_train, X_test, y_train, y_test = train_test_split(X_scaled, y_scaled, test_size=0.2, random_state=42)

    # Reshape the input data into 3D tensor with shape (n_samples, timesteps, n_features)
    X_train = X_train.reshape((X_train.shape[0], 1, X_train.shape[1]))
    X_test = X_test.reshape((X_test.shape[0], 1, X_test.shape[1]))

    # Define the LSTM model
    model = Sequential()
    model.add(LSTM(units=50, input_shape=(1, 2)))
    model.add(Dense(units=3))

    # Compile the model
    model.compile(optimizer='adam', loss='mse')

    # Define a callback to save the best model during training
    checkpoint = ModelCheckpoint('models/' + dataset_path.split('/')[-1][:-4] + '_best.h5', monitor='val_loss', verbose=1, save_best_only=True, mode='min')

    # Train the model
    model.fit(X_train, y_train, epochs=50, batch_size=32, validation_data=(X_test, y_test), callbacks=[checkpoint])

    # Save the final model
    model.save('models/' + dataset_path.split('/')[-1][:-4] + '.h5')

    # Calculate the accuracy of the model on the test dataset avoid divide by zero error
    y_pred = model.predict(X_test)
    y_pred = scaler_y.inverse_transform(y_pred)
    y_test = scaler_y.inverse_transform(y_test)

    accuracy_rain = 100 - np.mean(np.abs((y_test[:, 0] - y_pred[:, 0]) / y_test[:, 0])) * 100
    accuracy_soil_temp = 100 - np.mean(np.abs((y_test[:, 1] - y_pred[:, 1]) / y_test[:, 1])) * 100
    accuracy_soil_moisture = 100 - np.mean(np.abs((y_test[:, 2] - y_pred[:, 2]) / y_test[:, 2])) * 100
    # Display the accuracy of the model
    messagebox.showinfo("Model Trained", "Model trained successfully!\n\nAccuracy on test dataset:\nRain: " + str(round(accuracy_rain, 2)) + "%\nSoil Temperature: " + str(round(accuracy_soil_temp, 2)) + "%\nSoil Moisture: " + str(round(accuracy_soil_moisture, 2)) + "%")

# Create a button to select the dataset file
btn_select_file = tk.Button(window, text="Select Dataset", command=select_file)
btn_select_file.grid(column=0, row=0)

# Create a button to train the LSTM model
btn_train_model = tk.Button(window, text="Train Model", command=train_model)
btn_train_model.grid(column=0, row=1)

# Start the GUI
window.mainloop()

