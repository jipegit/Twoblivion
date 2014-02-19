# Twoblivion

Twoblivion is a free tool to automatically delete your old tweets and direct messages

## Author 

Jean-Philippe Teissier - @Jipe_ 

## How to install

Copy all files from Github

## Dependencies

* pip install python-twitter
* pip install python-dateutil

python-twitter is not compatible with Python3 yet

## Setup

1. Create an application. See https://dev.twitter.com/ 

2. Go to your application's settings -> OAuth settings and copy/paste your "Consumer key" and your "Consumer key" to the YOUR_APP_CONSUMER_KEY and YOUR_APP_CONSUMER_SECRET variables in the source code

3. Go to your application's settings -> Application Type, and change the Access parameter to "Read, Write and Access direct messages". Update the settings

3. Go back to your application's details and click on "Recreate my access token". Copy/paste your "Access token" and your "Access token secret" to the YOUR_ACCESS_TOKEN_SECRET and YOUR_ACCESS_TOKEN in the source code. Alternatively you can pass them as arguments with -k/--accesstokenkey and -s/accesstokensecret

4. Get your twitter ID from your username. https://www.google.fr/search?q=get+twitter+id+from+username

5. (optional) Set the TEST_DATE variable to whatever you want (or use the option -d/--date). Set the YOUR_USER_ID variable to your user_id. (or use the option -u/--userid)


## How to run

python2.7 twoblivion.py -h

eg. twoblivion.py -m -d "2013-09-01"

## Changelog

### 0.4
 * FIX: date comparison function

### 0.3
 * Massive code refactoring
 * Additional checks on the mandatory parameters

### 0.2
 * Converted to Python3
 * Options added to only delete Tweets or DM
 * Error handling has been improved
 * Some functions have been renamed
 * Readme update

### 0.1
 * Initial alpha release

## License

Twoblivion
Copyright (C) 2013 Jean-Philippe Teissier

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <http://www.gnu.org/licenses/>.
