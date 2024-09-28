**Efficient Data Stream Anomaly Detection**
===========================================

**Overview**
------------

This script detects anomalies in a real-time data stream using an adaptive moving average algorithm. It uses a graphical user interface (GUI) to display the incoming data points, their moving averages, and any detected anomalies visually.

### **Key Features**

*   Real-time data generation with seasonal components and anomalies.
    
*   Adaptive moving average algorithm to identify anomalies.
    
*   A user-friendly GUI to visualize data points and anomalies.
    
*   Scrolling capability to view recent data points.
    

**Code Breakdown**
------------------

### **Importing Required Libraries**

![image](https://github.com/user-attachments/assets/d7793718-3014-492a-9d9f-e3887b0c01d7)


*   **tkinter**: Used to create the GUI.
    
*   **ttk**: Provides themed widgets for a better look.
    
*   **random**: Helps in generating random numbers.
    
*   **numpy**: A library for numerical operations, especially useful for calculations.
    
*   **time**: Used for creating delays in the data generation.
    
*   **deque**: A double-ended queue, used to maintain a sliding window of data for the moving average calculation.
    
*   **threading**: Allows running the data generation in the background without freezing the GUI.
    
*   **matplotlib**: Used for plotting the data points and moving averages.
    

### **Data Stream Generation Emulation Function**

![image](https://github.com/user-attachments/assets/c908c592-6514-4b5a-ac50-8fdb6ef956ce)

**Explanation:**

*   This function generates a continuous stream of data points simulating real-world data.
    
*   It creates seasonal variations using a sine wave and adds random noise.
    
*   Anomalies are introduced at specified intervals by increasing the data point value.
    
*   The function uses the yield statement to return one data point at a time, simulating real-time arrival with a delay.
    

### **Anomaly Detection Class**

![image](https://github.com/user-attachments/assets/5d3354a1-d3da-4381-9e57-f2bfd4e65b03)


**Explanation:**

*   This class implements the adaptive moving average algorithm for anomaly detection.
    
*   **Initialization**: Sets up the window size (how many data points to consider for the average) and a threshold factor to define what constitutes an anomaly.
    
*   **update method**: Adds new data points to a sliding window and calculates the moving average and standard deviation.
    
    *   An anomaly is detected if the new data point deviates from the moving average by more than a defined factor of the standard deviation.
        

### **GUI Application Class**

**Explanation:**

*   **Initialization**: Sets up the main window for the application.
    
*   **Treeview**: Displays the data points, their moving averages, and standard deviations.
    
*   **Matplotlib Figure**: Creates a plot to visualize the data points and detected anomalies.
    
*   **Toolbar**: Provides tools for navigating the plot (like zooming).
    
*   **Data Storage**: Initializes lists to store data points and their averages for plotting.
    
*   **Threading**: Starts a background thread to continuously run the data stream.
    
    

### **Main Execution**

![image](https://github.com/user-attachments/assets/1704131e-12a3-48aa-b4d4-6dcb23a4b7f9)

**Explanation:**

*   This block initializes the main application window and starts the GUI event loop.
    
*   It ensures that the application runs until the user decides to close it.
    

**Algorithm Explanation**
-------------------------

### **Adaptive Moving Average**

*   The adaptive moving average is a statistical method used to detect anomalies in data streams.
    
*   It calculates the average of a specified number of recent data points (window size) and determines if a new data point is significantly different from this average based on standard deviation.
    
*   If the difference exceeds a threshold (a multiple of the standard deviation), it is flagged as an anomaly.
    

### **Effectiveness**

*   This method is effective for real-time anomaly detection because it adapts to changes in the data over time, allowing it to identify both sudden spikes and gradual shifts in the data stream.
    

**Error Handling and Data Validation**
--------------------------------------

*   The code includes basic error handling, ensuring that the program does not crash due to unexpected data values.
    
*   The moving average and standard deviation calculations only occur when enough data points are collected (i.e., when the data window is full).
    
*   In the update\_gui method, the program checks for None values and replaces them with "N/A" to avoid display errors.
    

Github Link - [Link](https://github.com/krishna-chandel/Data-Stream-Anomaly-Detection)
