<div align="center">
  
# 📥 Comepress
  #### Super trivial app to optimize your web project by converting all PNG, JPG and JPEG images to Next-Gen WebP format
![image](https://user-images.githubusercontent.com/25067102/185523884-85b1731c-c4c7-4b90-bf39-c1eab6107a54.png)

  Just drag and drop your files or folders and that's it!
  
  # Save up to 80% space!
  #### That means faster site loading for users and smaller project size! 
</div>

# Installation 👨‍💻

## Linux 🐧

1. Download the Linux version from here: https://github.com/NayamAmarshe/comepress/releases/latest
2. Extract the 7z file.
3. Double click and run the `comepress` executable file.

## MacOS 🍎

Coming Soon

## Windows 🐌

Coming Soon

# Build Instructions 🛠

Please help me generate builds for MacOS and Windows. 

1. Install dependencies: 
```bash
pip3 install pyqt5 pyinstaller
```
2. To run comepress as is, run: 
```bash
python3 comepress.py
```
3. To build comepress: 
```bash
pyinstaller comepress.py --add-data "./res/*:res" --onefile --icon='res/inbox_tray_3d.ico' --windowed
```

An executable file will be created in `dist` folder.
