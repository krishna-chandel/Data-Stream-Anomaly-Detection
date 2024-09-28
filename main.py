import tkinter as tk
from tkinter import ttk
import random
import numpy as np
import time
from collections import deque
import threading
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk

# Function to generate a real-time data stream with anomalies
def generate_data_stream(mean=0, std_dev=1, seasonality_period=50, noise_level=0.5, anomaly_interval=10):
    time_step = 0
    while True:
        # Simulate a base signal 
        seasonal_component = np.sin(2 * np.pi * time_step / seasonality_period)
        noise = random.gauss(0, noise_level)

        # Generate the data point
        data_point = mean + seasonal_component + std_dev * noise

        # Inject anomalies at specific intervals
        if time_step % anomaly_interval == 0:
            data_point += random.uniform(10, 50)  # Inject anomaly

        yield data_point
        time_step += 1
        time.sleep(0.1)  # Simulate real-time data arrival

# Anomaly Detector Class
class AdaptiveMovingAverageAnomalyDetector:
    def __init__(self, window_size=50, threshold_factor=2):
        self.window_size = window_size
        self.threshold_factor = threshold_factor
        self.data_window = deque(maxlen=window_size)
        self.moving_avg = None
        self.moving_std_dev = None

    def update(self, new_value):
        self.data_window.append(new_value)

        if len(self.data_window) == self.window_size:
            self.moving_avg = np.mean(self.data_window)
            self.moving_std_dev = np.std(self.data_window)

            is_anomaly = abs(new_value - self.moving_avg) > self.threshold_factor * self.moving_std_dev
            
            return is_anomaly, self.moving_avg, self.moving_std_dev
        
        return False, None, None

# GUI 
class AnomalyDetectionApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Real-Time Anomaly Detection")

        # frame for the Treeview and Scrollbar
        frame = tk.Frame(root)
        frame.pack(expand=True, fill='both')

        # Treeview with vertical scrollbar
        self.tree = ttk.Treeview(frame, columns=("Data", "Avg", "Std Dev"), show='headings')
        self.tree.heading("Data", text="Data Point")
        self.tree.heading("Avg", text="Moving Average")
        self.tree.heading("Std Dev", text="Std Dev")

        # Adding scrollbar
        self.scrollbar = ttk.Scrollbar(frame, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscrollcommand=self.scrollbar.set)

        # Packing the Treeview and Scrollbar
        self.tree.pack(side=tk.LEFT, expand=True, fill='both')
        self.scrollbar.pack(side=tk.RIGHT, fill='y')

        # Matplotlib figure and axis
        self.fig, self.ax = plt.subplots(figsize=(5, 3))
        self.canvas = FigureCanvasTkAgg(self.fig, master=root)
        self.canvas.get_tk_widget().pack(expand=True, fill='both')

        # Navigation Toolbar
        self.toolbar = NavigationToolbar2Tk(self.canvas, root)
        self.toolbar.update()
        self.canvas.get_tk_widget().pack(expand=True, fill='both')

        self.detector = AdaptiveMovingAverageAnomalyDetector(window_size=30, threshold_factor=2)
        self.data_points = []
        self.avg_points = []

        self.running = True
        threading.Thread(target=self.run_data_stream, daemon=True).start()

    def run_data_stream(self):
        for data_point in generate_data_stream(mean=0, std_dev=1, seasonality_period=50, noise_level=0.5, anomaly_interval=10):
            is_anomaly, avg, std_dev = self.detector.update(data_point)
            self.update_gui(data_point, avg, std_dev, is_anomaly)

    def update_gui(self, data_point, avg, std_dev, is_anomaly):
        # Inserting data into the treeview
        entry_id = self.tree.insert("", "end", values=(f"{data_point:.2f}", f"{avg:.2f}" if avg is not None else "N/A", f"{std_dev:.2f}" if std_dev is not None else "N/A"))

        # Change the background color based on anomaly detection
        if is_anomaly:
            self.tree.item(entry_id, tags=('anomaly',))
            self.tree.tag_configure('anomaly', background='red')
        else:
            self.tree.item(entry_id, tags=('normal',))
            self.tree.tag_configure('normal', background='white')

        # Scroll to the last entry
        self.tree.see(entry_id)

        # Update data points for visualization
        self.data_points.append(data_point)
        if avg is not None:
            self.avg_points.append(avg)
        else:
            self.avg_points.append(np.nan)  # Handle case when avg is None

        # Update plot
        self.ax.clear()
        self.ax.plot(self.data_points, label='Data Points', color='blue')
        self.ax.plot(self.avg_points, label='Moving Average', color='orange')
        if is_anomaly:
            self.ax.scatter(len(self.data_points) - 1, data_point, color='red', label='Anomaly', zorder=5)
        self.ax.legend()
        self.ax.set_title('Real-Time Data Stream')
        self.ax.set_xlabel('Time Steps')
        self.ax.set_ylabel('Value')

        # Set x-axis limits for scrolling
        if len(self.data_points) > 100:  
            self.ax.set_xlim(len(self.data_points) - 100, len(self.data_points))

        self.canvas.draw()  # Redraw the canvas with updated data

        self.root.update_idletasks()
        self.root.update()

    def on_closing(self):
        self.running = False
        self.root.destroy()

# Main Execution
if __name__ == "__main__":
    root = tk.Tk()
    app = AnomalyDetectionApp(root)
    root.protocol("WM_DELETE_WINDOW", app.on_closing)
    root.mainloop()
