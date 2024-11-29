# Cone Detection Project

---

## **Requirements**
To run this project, you need:
1. **Ubuntu/Linux System**.
2. **Python 3.10 or higher** installed.

---

## **Project Setup**
1. **Clone the Project**:
   Open a terminal and run:
   ```bash
   git clone <https://github.com/Ray9090/OpenCV-Cone-Detection.git>
   cd OpenCV-Cone-Detection
   ```

2. **Run the Setup Script**:
   This script will install all necessary dependencies automatically.
   ```bash
   chmod +x setup_env.sh
   sudo ./setup_env.sh
   ```
---

## **Running the Project**
1. Activate the virtual environment:
   ```bash
   source venv/bin/activate
   ```

2. Run the script:
   ```bash
   chmod +x source/cone.py
   python source/cone.py
   ```

3. Check the Output:
   - The processed image with detected cones will be saved in the `output` folder.

---

## **Folder Structure**
```
OpenCV-Cone-Detection/
├── source/
│   └── cone.py              # Main Python script
├── image/
│   └── image1.png           # Input images
├── output/                  # Output images (created automatically)
├── setup_env.sh             # Setup script for installing dependencies
└── requirements.txt         # Python dependencies
```

## **FTransfer the project folder over SSH connection**
```
scp <local_file_path/OpenCV-Cone-Detection> pi4@141.44.76.85:~
```
Removed <local_file_path/OpenCV-Cone-Detection> with the actual file path from the host device.

Enjoy using the **Cone Detection Project**! 🎉
