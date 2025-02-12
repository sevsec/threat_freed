# Threat Freed
## Summary
Threat Freed: I realize that's a tongue-twister. This is a Python module that will grab threat information (domains, IPs, URLs) from free, open source locations. This is a proof of concept, for funsies. The module will dump information to the terminal, to json files, or to SQLite database files. These can be used in conjunction with your favorite SIEM, database workbench, or in the terminal.

## Features
The module will grab all feeds given in `cfg/threat_freed.cfg`. There are three output options:
1. Print to the stdout (redirect is suggested)
2. Write to feed-specific, json-formatted files under threat_json
3. Write to feed-specific, sqlite-formatted files under threat_dbs

A default request timeout has been defined in the class constructor, but I'm debating adding it per threat source. Not much else besides that.

I've left the datasets in the directories to show what results can be expected. 

## Installation
This was created for Linux, so Windows/Mac support is uncertain. You will need requests and sqlite3 libs.

## Usage
Everything but the initial constructor is commented out by default. If you attempt to run the class as-is, it won't do anything. Uncomment the lines that have been commented out if you're looking for some quick, easy functionality. This module is meant to be used in conjunction with other services or automation, but can be used as-is.

## TODO
We'll see.

## Notes
Got improvements? They're welcome.
