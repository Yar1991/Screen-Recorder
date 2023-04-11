# Screen Recorder

Built with openCV, customtkinter, and other packages, a super simple screen recorder.
Just choose a folder where to save the recording, click "Start" and there you go.
You might adjust the frames or the recording time limit if needed.

## Installation:

```bash
python -m venv "name of your environment folder" # creating environment
```

```bash
source "name of your environment folder"/Scripts/activate # activate the environment
```

```bash
pip install -r requirements.txt # installing dependencies
```

### In case you want to create an .exe, there are a couple of steps to make:

```bash
pip show customtkinter # get location to the customtkinter directory
```

```bash
pyinstaller --noconfirm --onedir --windowed --icon="icon.ico" --add-data "<customTkinter location path>/customtkinter;customtkinter/" main.py
```
