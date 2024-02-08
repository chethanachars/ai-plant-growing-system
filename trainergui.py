import tkinter as tk
from tkinter import filedialog
import pandas as pd
import numpy as np
from sklearn.linear_model import LinearRegression
from sklearn.tree import DecisionTreeRegressor
from sklearn.ensemble import RandomForestRegressor
from sklearn.svm import SVR
from sklearn.model_selection import train_test_split

import pickle

class RegressionModel:
    def __init__(self, name, model):
        self.name = name
        self.model = model
        
    def __str__(self):
        return self.name

# Create the tkinter app
root = tk.Tk()
root.title("Regression Model Trainer")

# Create the file selection label
file_label = tk.Label(root, text="Select CSV File:")
file_label.grid(column=0, row=0, padx=10, pady=5, sticky=tk.W)

# Create the file selection button
def browse_file():
    global file_path
    file_path = filedialog.askopenfilename()
    
browse_button = tk.Button(root, text="Browse", command=browse_file)
browse_button.grid(column=1, row=0, pady=5, sticky=tk.W)

# Create the model selection label
model_label = tk.Label(root, text="Select Regression Model:")
model_label.grid(column=0, row=1, padx=10, pady=5, sticky=tk.W)

# Create the model selection dropdown
models = [
    RegressionModel("Linear Regression", LinearRegression()),
    RegressionModel("Decision Tree Regression", DecisionTreeRegressor()),
    RegressionModel("Random Forest Regression", RandomForestRegressor()),
    RegressionModel("Support Vector Regression", SVR())
]
selected_model = tk.StringVar()
selected_model.set(models[0])
model_dropdown = tk.OptionMenu(root, selected_model, *models)
model_dropdown.grid(column=1, row=1, pady=5, sticky=tk.W)

# Create a button to train the model
train_button = tk.Button(root, text="Train Model",
                         command=lambda: train_model(file_path, selected_model.get()))
train_button.grid(column=0, row=2, pady=5, sticky=tk.W)

# Create the result labels
mse_label = tk.Label(root, text="")
mse_label.grid(column=0, row=3, padx=10, pady=5, sticky=tk.W)

r2_label = tk.Label(root, text="")
r2_label.grid(column=0, row=4, padx=10, pady=5, sticky=tk.W)

accuracy_label = tk.Label(root, text="")
accuracy_label.grid(column=0, row=5, padx=10, pady=5, sticky=tk.W)

# Function to train the model
def train_model(file_path, selected_model):
    # Load the data
    data = pd.read_csv(file_path)
    
    # Split the data into input and output
    X = data.iloc[:, :-1]
    y = data.iloc[:, -1]
    
    # Split the data into training and testing sets
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2)
    
    # Train the selected model
    model = selected_model.model
    model.fit(X_train, y_train)
    
    # Evaluate the model on the test set
    y_pred = model.predict(X_test)
    mse = mean_squared_error(y_test, y_pred)
    r2 = r2_score(y_test, y_pred)
    accuracy = model.score(X_test, y_test)
    
    # Update the result labels
    mse_label.configure(text="MSE: " + str(mse))
    r2_label.configure(text="R2 Score: " + str(r2_score))
    accuracy_label.configure(text="Accuracy: " + str(accuracy*100) + "%")

    # Save the model
    filename = selected_model.get() + ".sav"
    pickle.dump(model, open(filename, 'wb'))

# Create a button to train the model
train_button = tk.Button(root, text="Train Model", command=train_model)
train_button.grid(column=0, row=2, padx=10, pady=5)

# Create the result labels
mse_label = tk.Label(root, text="")
mse_label.grid(column=0, row=3, padx=10, pady=5, sticky=tk.W)

r2_label = tk.Label(root, text="")
r2_label.grid(column=0, row=4, padx=10, pady=5, sticky=tk.W)

accuracy_label = tk.Label(root, text="")
accuracy_label.grid(column=0, row=5, padx=10, pady=5, sticky=tk.W)

# Run the main loop
root.mainloop()

# Close the window
root.destroy()

