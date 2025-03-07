Instructions for running py script are below. Or you can download the python exe release here to avoid all of the below.

Step 1: Install Python

    Download Python from the official website: https://www.python.org/downloads/.
    Install Python and make sure to check the box that says “Add Python to PATH” during installation.

Step 2: Install Required Libraries

    Open a terminal (Command Prompt for Windows, Terminal for macOS or Linux).
    Install the libraries by typing the following commands one by one and pressing Enter:

pip install pandas
pip install fuzzywuzzy
pip install PyQt6
pip install odfpy

Step 3: Save the Files

    Create a folder on your computer, for example, name it MonsterHunterApp.
    Download and save the following files in the same folder:
        MHWItems.py
        ItemIDS.ods

Step 4: Run the Program

    Open a terminal or command prompt again.
    Navigate to the folder where your files are saved. For example, if it’s in C:\MonsterHunterApp, you would type:

cd C:\MonsterHunterApp

Run the Python script by typing:

    python MHWItems.py

Step 5: Use the App

A window will open. You can type item names, and the app will show matching items and their IDs.
