import tkinter as tk
from tkinter import filedialog
import pandas as pd
from sklearn.tree import DecisionTreeRegressor
from sklearn.metrics import mean_squared_error, r2_score
from sklearn.model_selection import train_test_split
import pickle

# make file_path and model_path global
file_path = ''
model_path = ''

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

root = tk.Tk()
root.geometry("400x300")
root.title("Model Prediction")

# Create a label for file path
path_label = tk.Label(root, text="Select Data File: ")
path_label.grid(column=0, row=0, padx=10, pady=5, sticky=tk.W)

# Create an entry for file path
path_entry = tk.Entry(root, width=30)
path_entry.grid(column=1, row=0, padx=10, pady=5)

# Create a button to browse for a file
browse_button = tk.Button(root, text="Browse", command=browse_file)
browse_button.grid(column=2, row=0, padx=10, pady=5)

# Create a label for model path
model_label = tk.Label(root, text="Select Model File: ")
model_label.grid(column=0, row=1, padx=10, pady=5, sticky=tk.W)

# Create an entry for model path
model_entry = tk.Entry(root, width=30)
model_entry.grid(column=1, row=1, padx=10, pady=5)

# Create a button to browse for a model file
browse_model_button = tk.Button(root, text="Browse", command=browse_model)
browse_model_button.grid(column=2, row=1, padx=10, pady=5)

# Create an entry for input values
input_label = tk.Label(root, text="Enter Input Values (separated by comma): ")
input_label.grid(column=0, row=2, padx=10, pady=5, sticky=tk.W)

input_entry = tk.Entry(root, width=30)
input_entry.grid(column=1, row=2, padx=10, pady=5)

# Create a button to test the model
test_button = tk.Button(root, text="Test Model", command=test_model)
test_button.grid(column=1, row=3, padx=10, pady=5)

# Create the result label
result_label = tk.Label(root, text="")
result_label.grid(column=0, row=4, columnspan=3, padx=10, pady=5)

root.mainloop()


