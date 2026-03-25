# EZZTools
*A GUI Wrapper made for Eric Zimmerman's Suite of Windows Forensics tools*
*Made by MxCovert06*

I started making this project as a way to understand how windows forensics operates. I found myself switching between each tool through the terminal and having a hard time tracking outputs every time I processed a file.

This is where I decided to make a small wrapper that helps operators import their selected file, process it, and then open it using their preffered tool (Currently supports EZViewer and Timeline Explorer). I am currently experimenting with other methods of importing and processing artifacts, so later updates will be focused about tailoring the various flags supported by tools.

## Installation
First, make sure to have the `customtkinter` module for python.

This can be done using `pip install customtkinter`

Next, you will also need the installation of EZtools provided by Eric at the official website. It is strongly recommended that you run the `Get-ZimmermanTools.ps1` file for installation as the python file is built around that installation type.

Once you have installed EZtools and have found the installation path, install the `EZEZTools.py file` and place it in the folder with all of the Zimmerman Tools. While there are some tools located in further folders, place it in the regular `Ztools` folder, the python script will account for tools that are located in their own folders.

When the Python file is placed in the `Ztools` folder, you can then run it by right-clicking the file, and then running the file with `Python`.

**ALERT: This will pop up a UAC prompt asking if you would like to elevate the process. This is needed for some of Eric Zimmerman's tools. You are free to see the source code and take a look at what is being done. Everything relating to system operation is at the top of the file for the sake of user clarity.**

You will see a GUI with several buttons and sidebar. This confirms proper installation!



