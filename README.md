<div align="center">
  
# 📥 Comepress
  #### Super trivial app to optimize your web project by converting all PNG, JPG and JPEG images to Next-Gen WebP format
![image](https://user-images.githubusercontent.com/25067102/185523884-85b1731c-c4c7-4b90-bf39-c1eab6107a54.png)

  Just drag and drop your files or folders and that's it!
</div>

# Reduce your image bundle size by 40-80%
#### That means faster site loading for users and smaller project size! 

## Here's a small comparison:
| Without Comepress | With Comepress |
|-------------------|----------------|
|![image](https://user-images.githubusercontent.com/25067102/185750498-91c1bf0a-d094-4caf-9eda-5054a5c990dc.png)|![image](https://user-images.githubusercontent.com/25067102/185750604-d87f63e4-37da-4f36-91b8-717aaffd48b9.png)|
# With Comepress I easily got over 43% space gain!

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
