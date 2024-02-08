import tkinter as tk
from tkinter import filedialog, messagebox
import pandas as pd
from sklearn.tree import DecisionTreeRegressor
from sklearn.metrics import mean_squared_error, r2_score
from sklearn.model_selection import train_test_split
import pickle
import os

# make file_path global
file_path = ''

def browse_file():
    global file_path
    file_path = filedialog.askopenfilename()
    path_entry.delete(0, tk.END)
    path_entry.insert(tk.END, file_path)


def train_model():
    global file_path

    # check if a file has been selected
    if file_path == '':
        messagebox.showerror("Error", "Please select a CSV file.")
        return

    # read the data
    data = pd.read_csv(file_path)
    # remove all the rows with NaN values
    data.dropna(inplace=True)

    # drop the unwanted data time
    try:
        data.drop(['time'], axis=1, inplace=True)
    except:
        pass

    # split the data into input and output
    X = data.iloc[:, 0:2]
    y = data.iloc[:, 2:6]

    # split the data into train and test
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2)

    # fit the model
    model = DecisionTreeRegressor()
    model.fit(X_train, y_train)

    # predict the output for test data
    y_pred = model.predict(X_test)

    # calculate the mean squared error and r2 score
    mse = mean_squared_error(y_test, y_pred)
    r2 = r2_score(y_test, y_pred)

    # update the result labels if verancy is negative make it positive
    if mse < 0:
        mse = -mse
    mse_label.config(text="Mean Squared Error: {:.2f}".format(mse))
    if r2 < 0:
        r2 = -r2
    r2_label.config(text="R2 Score: {:.2f}".format(r2))

    # calculate and update the accuracy label if accuracy is negative make it positive
    accuracy = model.score(X_test, y_test)
    if accuracy < 0:
        accuracy = -accuracy
    accuracy_label.config(text="Accuracy: {:.2f}%".format(accuracy * 100))

    # save the model
    models_folder = 'models'
    if not os.path.exists(models_folder):
        os.makedirs(models_folder)

    filename = f'{models_folder}/decisiontree_{os.path.basename(file_path).split(".")[0]}.sav'
    with open(filename, 'wb') as file:
        pickle.dump(model, file)

    with open('models_index.csv', 'a') as file:
        # write the CSV file name and the model file name to models_index.csv
        file.write(os.path.basename(file_path).split(".")[0] + ',')
        file.write(filename + '\n')

    messagebox.showinfo("Success", "Model trained and saved successfully.")


root = tk.Tk()
root.geometry("400x300")
root.title("Sensor Data Optimization and Prediction")

# Create a label for file path
path_label = tk.Label(root, text="Select File: ")
path_label.grid(column=0, row=0, padx=10, pady=5, sticky=tk.W)

# Create an entry for file path
path_entry = tk.Entry(root, width=30)
path_entry.grid(column=1, row=0, padx=10, pady=5)

# Create a button to browse for a file
browse_button = tk.Button(root, text="Browse", command=browse_file)
browse_button.grid(column=2, row=0, padx=10, pady=5)

# Create a button to train the model
train_button = tk.Button(root, text="Train Model", command=train_model)
train_button.grid(column=1, row=1, padx=10, pady=5)

# Create a label for mean squared error
mse_label = tk.Label(root, text="Mean Squared Error: ")
mse_label.grid(column=0, row=2, padx=10, pady=5, sticky=tk.W)
# Create a label for variance score
r2_label = tk.Label(root, text="Variance Score: ")
r2_label.grid(column=0, row=3, padx=10, pady=5, sticky=tk.W)
# Create a label for accuracy
accuracy_label = tk.Label(root, text="Accuracy: ")
accuracy_label.grid(column=0, row=4, padx=10, pady=5, sticky=tk.W)

root.mainloop()

