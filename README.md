# Habit Tracking App

This repository offers a basic backend implementation for a habit tracking app. It uses a sqlite3 database for storage and a CLI command interface for initial testing and usage. 
Implementing a frontend or a RESTful API is recommended for further usage.


## Habit

A habit is the elementary element (activity), which is planned to perform in a certain intervall (periodicity). In this implementation it allows the following properties:

* **name**: up to 100 chars
* **note**: optional text, which can describe the habit or add other personal information for this habit
* **periodicity**: the interval in which the habit need to be performed (actually offers daily, weekly, monthly)

## Installation

This project uses Python 3.10. For the dependency handling and for the virtual environment we use **pipenv**.

To install **pipenv** open the command line and enter *(requires pip to be installed)*:

```
pip install pipenv
```

After installation of pipenv, **to inizialze the project and install the required modules**, change to the folder where the project was cloned to and enter in the command line:

```
pipenv install
```

To switch to the the **virtual environments shell** run the following command in the command line in the project folder:

```
pipenv shell
```
*It is recommed to run the shell. Alternativly, the run command can be used. For more information see the [pipenv documentation](https://pipenv.pypa.io/en/latest/)*

## Tests

This project uses **pytest** for the unit tests. To run the unit tests open the command line tool in the project folders root and run:

```
py.test
```
This will automatically locate the unit tests and run them. For running individual tests or use extended logging functionalities, please see the documentation on the [projects website](https://docs.pytest.org/en/7.3.x/).

***attention: for running it, you need to be in the virtual environment shell (see instructions under installation)***

## Usage

For the basic functionalities (CRUD, tracking, analytics) this app offers a CLI (command line interface). The following listings wil show you how to use the command line 
for all the basic functioanlities.

***attention: for running it, you need to be in the virtual environment shell (see instructions under installation)***

### CRUD 

The CRUD module offers all basic actions, to create, edit and delete a habit. To use it please use the following command:

```
py cli.py habit
```

**To add a new habit use the following command:**

```
py cli.py habit add "name" "periodicity"
```

*Parameter:*
* **name:** Name for the habit, must be uniqe
* **periodicity:** intervall, allowed values: d, w, m

*Optional Arguments*
* **--note=NOTE** (to add a note, must be string inside "")

*example*
```
py cli.py habit add "new habit" "d" --note="MY first created habit"
```

**To delete an exiting habit use the following command:**

```
py cli.py habit delete habit_id 
```

*Parameter:*
* **habit_id:** id of the habit to delete

*example*
```
py cli.py habit delete 1
```

**To pause / unpause an exiting habit use the following command:**

```
py cli.py habit pause habit_id 
py cli.py habit unpause habit_id
```

*Parameter:*
* **habit_id:** id of the habit to pause/unpause

*example*
```
py cli.py habit pause 1
```

**To update an exiting habit use the following command:**

* *Mind: at least one optional Argument must be passed too (the field which is intended to be updated)* *

```
py cli.py habit update habit_id --name=NAME
```

*Parameter:*
* **habit_id:** id of the habit to update

*Optional Arguments*
* **--name=NAME** (to update the name, new name must be unique, must be string inside "")
* **--note=NOTE** (to update thenote, must be string inside "")

*example*
```
py cli.py habit update 1 --name="Updated Habit" --note="Just submitted an updated note"
```

**To show all details about an existing habit use the following command:**

```
py cli.py habit show habit_id
```

*Parameter:*
* **habit_id:** id of the habit to show

*example*
```
py cli.py habit show 1
```

### Tracking

The tracking module offers the functionality to make a tracking for a habit. A tracking is an entry that this habit was performed and will be used for the 
evaluation for the streaks. To use it please use the following command:

```
py cli.py tracking
```

**To add a tracking use the following command:**

```
py cli.py tracking add habit_id
```

*Parameter:*
* **habit_id:** id of the habit which the tracking will be added for

*Optional Arguments*
* **--date=DATESTRING** (date string in the following format 'yyyy-mm-dd hh:mm:ss', if not set it wil use the actual time, allows to make a tracking for a different time )

*example*
```
py cli.py habit tracking add 1 --date="2023-06-01 12:00:00"
```

### Analytics

The analytics module offers the functionality for showing statistics about the habits and the streaks. To use it please use the following command:

```
py cli.py analytics
```

**To show all habits registered use the following command:**

```
py cli.py analytics show_all
```

*Optional Arguments*
* **--active=BOOLEAN** (boolean to set if the active or the inactive habits should be shown (paused/unpaused habits), default if not set it True=active habits)

*example*
```
py cli.py analytics show_all --active=False
```

**To show all habits for a certain periodicity use the following command:**

```
py cli.py analytics show_by_periodicity PERIODICITY
```
*Parameter:*
* **PERIODICITY:** identifier for the habits period to be shown. allowed values 'd', 'w', 'm'

*example*
```
py cli.py analytics show_by_periodicity "d"
```

**To show all habits streak use the following command:**

```
py cli.py analytics show_streaks
```

*Optional Arguments*
* **--habit_id=id** (id of a habit, to filter the list to a certain habit only)

*example*
```
py cli.py analytics show_streaks --habit_id=1
```
