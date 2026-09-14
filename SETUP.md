# MistResonance Dashboard — Setup Guide

This guide walks you through installing everything needed to run this project,
even if you're new to Python.

## 1. Install Python

Check if Python is already installed by opening a terminal (Command Prompt,
PowerShell, or Terminal) and running:

```bash
python --version
```

If you see a version number (e.g. `Python 3.11.4`), skip to Step 2.

If you get an error like "python is not recognized," download and install
Python from [python.org/downloads](https://www.python.org/downloads/).

**Windows users:** during installation, make sure to check the box that says
**"Add python.exe to PATH"** — this is easy to miss and causes the same
"not recognized" error afterward if skipped.


## 2. Install project dependencies

Install everything listed in
`requirements.txt`:

```bash
pip install -r requirements.txt
```

This installs:
- **`keyboard`** — detects keypresses (used to quit the simulation with `Q`)
- **`rich`** — styles and formats the dashboard's terminal output (colors,
  panels, layout)

## 3. Run the dashboard

```bash
python run_dashboard.py
```

Follow the on-screen prompt (`Y`/`N`) to start the simulation. Once running,
press **`Q`** at any time to exit.

## Troubleshooting

- **"No module named 'keyboard'" or "No module named 'rich'"** — Dependencies weren't installed yet.
  Re-run Steps 2–3.
- **`keyboard` requires admin/root privileges on Mac/Linux** — if you get a
  permissions error when pressing `Q`, try running the script with elevated
  privileges (e.g. `sudo python run_dashboard.py` on Mac/Linux).