import tkinter as tk
import os

# Create the main window
root = tk.Tk()
root.title("Realtime Sensor Data Optimization and Predictions")
root.geometry("500x600")

# Set background color
bg_color = "#f2f2f2"
root.configure(bg=bg_color)

# Create a title label
title_label = tk.Label(root, text="Choose a model to train:", font=("Arial", 18), bg=bg_color, fg="#333")
title_label.pack(pady=20)

# Create a frame to hold the buttons
button_frame = tk.Frame(root, bg=bg_color)
button_frame.pack(pady=10)

# Create five buttons for each model
button_width = 20
button_height = 2
button_bg = "#f5f5f5"
button_fg = "#333"

dt_button = tk.Button(button_frame, text="Train Decision Tree", width=button_width, height=button_height, bg=button_bg, fg=button_fg, font=("Arial", 12), command=lambda: os.system('python dt.py'))
lstm_button = tk.Button(button_frame, text="Train LSTM", width=button_width, height=button_height, bg=button_bg, fg=button_fg, font=("Arial", 12), command=lambda: os.system('python lstm.py'))
#Test_lstm_button = tk.Button(button_frame, text="Test LSTM", width=button_width, height=button_height, bg=button_bg, fg=button_fg, font=("Arial", 12), command=lambda: os.system('python tlstm.py'))
#gb_button = tk.Button(button_frame, text="Train Gradient Boosting", width=button_width, height=button_height, bg=button_bg, fg=button_fg, font=("Arial", 12), command=lambda: os.system('python gb.py'))
lr_button = tk.Button(button_frame, text="Train Linear Regression", width=button_width, height=button_height, bg=button_bg, fg=button_fg, font=("Arial", 12), command=lambda: os.system('python LR.py'))
rf_button = tk.Button(button_frame, text="Train Random Forest", width=button_width, height=button_height, bg=button_bg, fg=button_fg, font=("Arial", 12), command=lambda: os.system('python randomui.py'))
ds_button = tk.Button(button_frame, text="create new dataset", width=button_width, height=button_height, bg=button_bg, fg=button_fg, font=("Arial", 12), command=lambda: os.system('python dataset.py'))
#opt_button = tk.Button(button_frame, text="optimize a dataset dataset", width=button_width, height=button_height, bg=button_bg, fg=button_fg, font=("Arial", 12), command=lambda: os.system('python optimaizer.py'))
#new_ds_button = tk.Button(button_frame, text="create more consistent new dataset", width=button_width, height=button_height, bg=button_bg, fg=button_fg, font=("Arial", 12), command=lambda: os.system('python new_dataset.py'))

# Pack the buttons onto the window
dt_button.pack(pady=5)
lstm_button.pack(pady=5)
#gb_button.pack(pady=5)
lr_button.pack(pady=5)
rf_button.pack(pady=5)
ds_button.pack(pady=5)
#opt_button.pack(pady=5)
#new_ds_button.pack(pady=5)
#Test_lstm_button.pack(pady=5)

# Create a frame to hold the other buttons
other_button_frame = tk.Frame(root, bg=bg_color)
other_button_frame.pack(pady=20)

# Create a button to test the models
test_button = tk.Button(other_button_frame, text="Test Models", width=button_width, height=button_height, bg=button_bg, fg=button_fg, font=("Arial", 12), command=lambda: os.system('python test_models.py'))
test_button.pack(side=tk.LEFT, padx=10)

# Create a button to open the server dashboard
dashboard_button = tk.Button(other_button_frame, text="Server Dashboard", width=button_width, height=button_height, bg=button_bg, fg=button_fg, font=("Arial", 12), command=lambda: os.system('python gui1.py'))
dashboard_button.pack(side=tk.RIGHT, padx=10)

# Run the main loop
root.mainloop()
