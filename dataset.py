import random
import pandas as pd
import tkinter as tk
from tkinter import messagebox
import uuid

class PlantGrowthDataGenerator:
    def __init__(self, master):
        self.master = master
        master.title("Plant Growth Data Generator")

        # Create widgets
        self.num_samples_label = tk.Label(master, text="Number of Samples:")
        self.num_samples_entry = tk.Entry(master, width=10)
        self.generate_button = tk.Button(master, text="Generate Data", command=self.generate_data)

        # Add widgets to layout
        self.num_samples_label.grid(row=0, column=0, padx=5, pady=5)
        self.num_samples_entry.grid(row=0, column=1, padx=5, pady=5)
        self.generate_button.grid(row=1, column=0, columnspan=2, padx=5, pady=5)

    def generate_data(self):
        # Get the number of samples from the user input
        try:
            num_samples = int(self.num_samples_entry.get())
        except ValueError:
            messagebox.showerror("Error", "Invalid number of samples.")
            return

        # Define the optimal ranges for the rain, soil temperature, and soil moisture
        optimal_rain = (2, 3)  # in millimeters
        optimal_soil_temp = (22, 25)  # in degrees Celsius
        optimal_soil_moisture = (53, 55)  # in percent

        # Generate the data for each column
        time = pd.date_range(start="2023-01-01", periods=num_samples, freq="H")
        temperature_2m = [round(random.uniform(20, 25), 2) for _ in range(num_samples)]
        relativehumidity_2m = [round(random.uniform(30, 70), 2) for _ in range(num_samples)]
        rain = [round(random.uniform(optimal_rain[0], optimal_rain[1]), 2) for _ in range(num_samples)]
        soil_temperature_0_to_7cm = [round(random.uniform(optimal_soil_temp[0], optimal_soil_temp[1]), 2) for _ in range(num_samples)]
        soil_moisture = [round(random.uniform(optimal_soil_moisture[0], optimal_soil_moisture[1]), 2) for _ in range(num_samples)]

        # Combine the columns into a DataFrame
        data = pd.DataFrame({
            "time": time,
            "temperature_2m": temperature_2m,
            "relativehumidity_2m": relativehumidity_2m,
            "rain": rain,
            "soil_temperature_0_to_7cm": soil_temperature_0_to_7cm,
            "soil_moisture": soil_moisture
        })

        # Generate a unique filename for the CSV file
        filename = f"plant_growth_data_{uuid.uuid4().hex[:8]}.csv"

        # Save the DataFrame to a CSV file with UTF-8 encoding
        data.to_csv(filename, index=False, encoding="utf-8")

        # Show success message
        messagebox.showinfo("Success", f"Data generated and saved to {filename}.")

# Create the Tkinter app and start the event loop
root = tk.Tk()
app = PlantGrowthDataGenerator(root)
root.mainloop()
