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

## 2. Create a virtual environment (recommended)

A virtual environment keeps this project's dependencies separate from
anything else on your system. From the project folder, run:

```bash
python -m venv .venv
```

Activate it:

- **Windows (PowerShell):**
  ```bash
  .venv\Scripts\activate
  ```
- **Mac/Linux:**
  ```bash
  source .venv/bin/activate
  ```

You'll know it worked if you see `(.venv)` appear at the start of your
terminal prompt.

## 3. Install project dependencies

With your virtual environment active, install everything listed in
`requirements.txt`:

```bash
pip install -r requirements.txt
```

This installs:
- **`keyboard`** — detects keypresses (used to quit the simulation with `Q`)
- **`rich`** — styles and formats the dashboard's terminal output (colors,
  panels, layout)

## 4. Run the dashboard

```bash
python run_dashboard.py
```

Follow the on-screen prompt (`Y`/`N`) to start the simulation. Once running,
press **`Q`** at any time to exit.

## Troubleshooting

- **"No module named 'keyboard'" or "No module named 'rich'"** — your virtual
  environment likely isn't active, or dependencies weren't installed yet.
  Re-run Steps 2–3.
- **`keyboard` requires admin/root privileges on Mac/Linux** — if you get a
  permissions error when pressing `Q`, try running the script with elevated
  privileges (e.g. `sudo python run_dashboard.py` on Mac/Linux).
- **VS Code doesn't seem to use the right Python** — open the Command Palette
  (`Ctrl+Shift+P`), search for **"Python: Select Interpreter"**, and choose
  the one inside your project's `.venv` folder.
