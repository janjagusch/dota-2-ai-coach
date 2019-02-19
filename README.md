# Dota 2 AI Coach

**We use cutting edge AI to improve your Dota 2 skills.**  

Ok, enough with the buzzwords. This repository provides aggregated in-game information about professional DOTA 2 matches. We developed this project during [Hackdays Rhein-Neckar 2019](https://hack-days.de/rhein-neckar/home) over a period of three days (14.02.2019 - 18.02.2019).  

Sponsor and data-/ infrastructure provider is the Esports department of [SAP](https://www.sap.com/index.html) in collaboration with [Team Liquid](https://www.teamliquidpro.com/).

In short, the program compiles a series of SAP SQL queries, provided a match identifier, and executes them on a SAP HANA database. The results are then provided through an easy-to-use API.

## Getting Started

These instructions will get you a copy of the project up and running on your local machine for development and testing purposes.

### Data

The data provided consists of combat logs for Team Liquid during [The International 2018](https://liquipedia.net/dota2/The_International/2018) as well as additional meta information about the game. Unfortunately, the data cannot be shared publicly.

### Prerequisites

The packages required for running this program are:

```
flask
numpy
pandas
pyhdb
```

You can install them through the provided ```requirements.txt``` file.

### Connecting to HANA

Place your HANA credentials in the ```.env``` file.

## Deployment

Start the service from ```coach_api_server.py```.

### Using the API
URL Path | HTTP Verb | Request Body | Request Headers | Response Body | Description
-|-|-|-|-|-|
/match_ids | GET | None | None | List of match ids (int) | Returns all match ids in the database
/first_blood | GET | match id (int) | None | | Returns first blood information for match id
/kill_sequences | GET | match id (int) | None | | Returns kill sequences for match id
/intensity | GET | match id (int) | None | {"dire" {name: "Dire", objects: []}, "radiant": {name: "Radiant", objects: []}, seconds_interval: []} | Returns match intensity by team in 10 second intervals

## Authors

* **[Jan-Benedikt Jagusch](https://www.linkedin.com/in/jjagusch/)**
  * *Big Data Engineer, Data Scientist*
  * GitHub - [jbj2505](https://github.com/jbj2505)
* **Ringo Stahl**
  * *Full Stack Developer*
  * GitHub - [crnchbng](https://github.com/crnchbng)
* **[Marius Bock](https://www.linkedin.com/in/marius-bock-046167108/)**
  * *Data Scientist*
  * GitHub - [mariusbock](https://github.com/mariusbock)
* **Katharina Spinner**
  * *Front End Developer*
  * GitHub - [Rahtainka](https://github.com/Rahtainka)
* **[Mariia Khodaeva](https://www.linkedin.com/in/mariia-khodaeva-813b8a169/)**
  * *Dota 2 Expert and Project Manager*

## Acknowledgments

* Thanks to [Hackdays](https://hack-days.de/) - especially to [Oliver Bruemmer](https://www.linkedin.com/in/oliverbruemmer/) - for organizing this event.
* Thanks to [SAP](https://www.sap.com/index.html) for challenging us with this exciting project.
