[![Maintenance](https://img.shields.io/badge/Maintained%3F-yes-green.svg)]

# Twoblivion

Twoblivion is a free tool to automatically delete your old tweets and direct messages

## Author

Jean-Philippe Teissier - @Jipe_

## How to install

Clone the repo from Github

## Installing requirements

* `pip install -r requirements.txt`

or, if you're using Pipenv:

* `pipenv install`

⚠️ python-twitter does not support Twitter API 1.1 for Direct Messages ⚠️

See. [Issue 603](https://github.com/bear/python-twitter/issues/603)

A workaround for Direct Messages can be applied following the steps below.
Direct Messages older than 30 days WON'T be deleted.

FIX: You MUST patch `python-twitter`:
 * `pip show python-twitter`
 * open `api.py` and modify the class below:
 * GetDirectMessages: 
    url = '%s/direct_messages/events/list.json' % self.base_url

## Setup

1. Create an application. See https://dev.twitter.com/

2. Go to your application's settings -> Keys and Access Tokens and copy/paste your "Consumer key" and your "Consumer secret" to the YOUR_APP_CONSUMER_KEY and YOUR_APP_CONSUMER_SECRET variables in config.py (copy from config.py.sample)

3. Go to your application's settings -> Application Type, and change the Access parameter to "Read, Write and Access direct messages". Update the settings

3. Go back to your application's details and click on "Recreate my access token".
Copy/paste your "Access token" and your "Access token secret" to the YOUR_ACCESS_TOKEN and YOUR_ACCESS_TOKEN_SECRET in the source code. Alternatively you can pass them as arguments with -k/--accesstokenkey and -s/accesstokensecret

4. Get your twitter ID from your username. https://www.google.fr/search?q=get+twitter+id+from+username

5. (optional) Set the YOUR_USER_ID variable to your user_id. (or use the option -u/--userid)

## How to run

python twoblivion.py -h

eg. python twoblivion.py -m -d "2020-01-01"

## Known issues

The underlying Twitter library `python-twitter` has several known issues:
  * Direct Messages handling is **BROKEN** and does not support Twitter API 1.1
  * Rate limits handling often fails

## Changelog

### 0.6
 * Move config to config.py
 * Set sleep_on_rate_limit to True
 * Apply a temporary patch to python-twitter for Direct Messages
 * Add emojis everywhere

### 0.5.0
 * Default behavior deletes Tweets *AND* DMs
 * Some code health fixes

### 0.4.3
 * Default date set to now - 30 days

### 0.4.2
 * Shebang and typo

### 0.4.1
 * FIX: Sent Direct Messages were not deleted.

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
Copyright (C) 2015-2020 Jean-Philippe Teissier

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
