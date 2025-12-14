# Password Manager Project

A [Python](https://www.python.org/) desktop application built with [Tkinter](https://docs.python.org/3/library/tkinter.html) and [SQLite](https://www.sqlite.org/index.html).

This project was made as a final project for our first semetral sophomore year to demonstrate advanced programming concepts, including graphical user interfaces, persistent database management, and modular code structure.

## Components

- `PassManager.py`: Main module containing the application logic, GUI rendering, and database interactions.
- `passwords.db`: Local SQLite database file generated automatically to store credentials.
- `assets`: Contains UI resources (`locked_icon.ico`, `unlocked_icon.ico`, `pass_icon.png`).

## Dependencies

This project uses [pip](https://pypi.org/project/pip/) to manage external dependencies.
Most libraries used (`tkinter`, `sqlite3`, `os`) are part of the standard Python library.
However, for image processing, `Pillow` is required.

Useful commands:

- `pip install pillow`: installs the required image processing library.
- `python PassManager.py`: starts the application.
- `python --version`: checks if your environment meets the 3.6+ requirement.

# Project ACP

This project was created to apply our knowledge in Python programming and showcase how it can be used in developing practical desktop utilities. It showcases our skills in designing a relational database schema, implementing CRUD operations, and building an interactive GUI to simplify credential management.

It features:
- Secure Master Password Login System
- Dynamic "Subpage" Categorization (Work, Socials, etc.)
- Full CRUD capabilities (Create, Read, Update, Delete)
- Persistent local storage using SQLite3
- Privacy masking for sensitive fields

## Planned Features (In Progress)
- Stronger Encryption (Hashing/Bcrypt implementation)
- Search bar functionality for accounts
- Dark Mode toggle

## Getting Started

### Requirements
- Python 3.6+
- Pillow Library
- Windows / macOS / Linux OS

## Built With
- [Python Language](https://www.python.org/)
- [Tkinter GUI](https://docs.python.org/3/library/tkinter.html)
- [SQLite Database](https://www.sqlite.org/)
- [Pillow Library](https://python-pillow.org/)

## How to run [Terminal / VS Code]
- Find the `Password-Manager-Project` folder.
- Open your terminal or Command Prompt in this folder.
- Ensure you have the required library installed by running `pip install pillow`.
- Run the command `python PassManager.py`.
- **First Time Login:**
    - The default master password is `udumbass`.
    - You can change this in the source code variable `__pass_code`.
- **Database:**
    - A `passwords.db` file will be created automatically in the same folder upon the first launch.
- Check the source code comments if you need to debug specific modules or change the `resolve_path` logic.