# Activity Tracking Aplication

This is a flask application that is built to allow users signup and log their activities. Each user has to register with a unique email after which they can log activities and update them as required.
A Flask-based activity logging app using OOP and SQLite.

## Set Up

To run this application locally, make sure you are in the project folder on your terminal then install the dependencies using

```powershell-interactive
$ pip install -r requirements.txt
```

Run the application using

```azurepowershell
$ python -m flask run
```

Your app should be running on port 5000

<http://127.0.0.1:5000>

## Table Schema

This App has just two models having a one-to-many relationship and make use of the sqlite database:

- **AppUser** :Table for saving users. One user can have 0 or many tasks
- **Task**- Table for saving tasks of users.

## Credits

- This projects makes use of OOP style heavily for the backend. The inspiration for this came from OOP Course Manager.

## Hosting

This app is hosted on render and can be accessed from this link [here]()
