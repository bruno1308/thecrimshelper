
# The Crims Helper
Helper to aid you through the game

As of now, the helper is capable of:

* Finding the optimal robbery given the possible options
* Commiting the robbery
* Going to Raves and recovering the energy with the best cost-benefit drug available
* Going to the Hospital whenever the addiction reaches a threshold
* Repeat

## Getting Started

These instructions will get you a copy of the project up and running on your local machine.

### Prerequisites

What things you need to install the software
 * pip
 * python 2.7

### Configuring
 * Open config.py and you will find:
 
```
MIN_SUCCESS_TO_ROBBERY = 100
USERNAME = ""
PASSWORD = ""
AUTO_LEAVE_PRISON = True
TIME_BETWEEN_ACTIONS = 0
MAX_ADDICTION = 3
MIN_ADDICTION = 0.5
```
* USERNAME: Put your username here
* PASSWORD: Put your password here
* MIN_SUCCESS_TO_ROBBERY: The minimum chance of success acceptable by the helper when going to rob, used to find the best robbery 
* AUTO_LEAVE_PRISON: True to bribe the guard and leave prison
* TIME_BETWEEN_ACTIONS: Time between game interactions in seconds (I suggest using 2 or 3)
* MAX_ADDICTION: Max acceptable addiction before going to hospital and restoring it to 0
* MIN_ADDICTION: Not yet used

IMPORTANT

* Add a nightclub that you can join and has at least 1 drug available and put it on top of your favorite list


### Installing

* First, install the project requirements

```
pip install -r requirements.txt
```

* Change config.txt with your account details
* Add a nightclub that you can join and has at least 1 drug available and put it on top of your favorite list
* Run the main file

```
python main.py
```

or, if you don't wan't to put your info in config.py:

```
python main.py username password
```

If it complains html5lib was not found, run:

```
pip install --ignore-installed six --user
sudo -H pip install html5lib --ignore-installed
```

## Authors

* **Bruno Lopes** 


## License

This project is licensed under the MIT License - see the [LICENSE.md](LICENSE.md) file for details

## Acknowledgments

* This project should be used on your own risk
