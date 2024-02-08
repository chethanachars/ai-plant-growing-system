import tkinter as tk
from tkinter import filedialog, messagebox
import pandas as pd
from sklearn.feature_selection import SelectKBest, f_regression
from sklearn.preprocessing import StandardScaler

# Define function to browse and select a CSV file
def browse_file():
    global file_path
    file_path = filedialog.askopenfilename()
    path_entry.delete(0, tk.END)
    path_entry.insert(tk.END, file_path)

# Define function to optimize the dataset and save to a new CSV file
def optimize_dataset():
    global file_path
    global optimized_file_path

    # Check if a file has been selected
    if file_path == '':
        messagebox.showerror("Error", "Please select a CSV file.")
        return

    # Read the data from the selected CSV file
    data = pd.read_csv(file_path)

    # Drop the "time" column
    data.drop(['time'], axis=1, inplace=True)

    # Split the data into input and output
    X = data.iloc[:, 0:4]
    y = data.iloc[:, 4:6]

    # Scale the input data
    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X)

    # Select the top 3 most important features
    selector = SelectKBest(f_regression, k=3)
    X_selected = selector.fit_transform(X_scaled, y)

    # Concatenate the selected input features and output variables into a new dataset
    optimized_data = pd.DataFrame(X_selected, columns=["temperature_2m", "relativehumidity_2m", "rain"])
    optimized_data["soil_temperature_0_to_7cm"] = data["soil_temperature_0_to_7cm"]
    optimized_data["soil_moisture"] = data["soil_moisture"]

    # Save the optimized dataset to a new CSV file
    optimized_file_path = file_path.replace(".csv", "_optimized.csv")
    optimized_data.to_csv(optimized_file_path, index=False)

    messagebox.showinfo("Success", "Dataset optimized and saved successfully.")

root = tk.Tk()
root.geometry("400x300")
root.title("Dataset Optimization")

# Create a label for file path
path_label = tk.Label(root, text="Select File: ")
path_label.grid(column=0, row=0, padx=10, pady=5, sticky=tk.W)

# Create an entry for file path
path_entry = tk.Entry(root, width=30)
path_entry.grid(column=1, row=0, padx=10, pady=5)

# Create a button to browse for a file
browse_button = tk.Button(root, text="Browse", command=browse_file)
browse_button.grid(column=2, row=0, padx=10, pady=5)

# Create a button to optimize the dataset
optimize_button = tk.Button(root, text="Optimize Dataset", command=optimize_dataset)
optimize_button.grid(column=1, row=1, padx=10, pady=5)

root.mainloop()
