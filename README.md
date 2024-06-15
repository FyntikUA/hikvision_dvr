# DVR Camera Status Monitoring

This script monitors the status of cameras connected to a DVR and logs any changes in their status, particularly when the camera shows "NO VIDEO" or goes offline. It also logs connection issues with the DVR.

## Prerequisites

- Python 3.x
- `requests` library
- `schedule` library

## Installation

1. **Clone the repository or download the script:**

    ```sh
    git clone https://github.com/FyntikUA/hikvision_dvr
    cd https://github.com/FyntikUA/hikvision_dvr
    ```

2. **Create a virtual environment:**

    ```sh
    python -m venv venv
    ```

3. **Activate the virtual environment:**

    - On Windows:
        ```sh
        .\venv\Scripts\activate
        ```
    - On MacOS/Linux:
        ```sh
        source venv/bin/activate
        ```

4. **Install the required libraries:**

    ```sh
    pip install -r requirements.txt
    ```

## Usage

1. **Run the script:**

    ```sh
    python monitor_cameras.py
    ```

2. **Check the log file:**

    The script will create a log file named `baza_camera_log.txt` in the same directory, which will contain logs of the camera statuses and connection issues.

## Configuration

- Update the `dvr_ip`, `dvr_port`, `username`, and `password` variables in the script with your DVR's connection details.

## File Structure

```plaintext
.
├── monitor_cameras.py  # Main script
├── requirements.txt    # List of required libraries
└── README.md           # This README file


