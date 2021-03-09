# Steg Maker

Simple web interface for [steghide](https://github.com/StefanoDeVuono/steghide).

## Installation

For the simplest method, just do this:

```bash
pip install flask
```

For an isolated installation, the process is a bit more involved:

```bash
# First install the virtual package environment manager
pip install virtualenv

# Next create a new virtual environment
virtualenv venv

# Activate the virtual environment in bash.
# There are other scripts for other shells, like activate.fish and .ps1
source venv/bin/activate

# Once inside venv, pip will install packages isolated from your system
pip install flask

# When you're done with flask, exit the virtual environment
deactivate
```

## Usage

If you're using `virtualenv`, then first run `source venv/bin/activate`. Run `deactivate` or exit the shell to leave the virtual environment.

Execute `flask run`, then visit http://127.0.0.1:5000 in your browser.
