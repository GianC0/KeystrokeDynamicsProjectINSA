# keylogger
A Python Keylogger, saving the timestamp and the pressed key.

(1) Clone the git repository.

(2) Preferably create a virtual environment with Python 3. Then run 

```
pip install -r requirements.txt
```

to install all packages. 

(3) Then simply start the keylogger with the following command:

```
python keylogger.py
```

The keylogger will run in the background and record all pressed keys.

------
*Work entirely based on [tamaramueller keylogger](https://github.com/tamaramueller/keylogger). The changes introduced here adds a `on_release` function that checks when you stop pressing the key and adds indicators for the action that was executed (RELEASE and PRESS)*
