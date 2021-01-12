# auctionhouse_wow

## Setup
run 
```bash
pip3 install -r requirements
```
Default ``settings`` file should be on same level as main.py
```json
{
    "realm": "server_name",
    "region": "eu/us",
    "locale": "en_US",
    "client_id": "XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX",
    "client_secret": "XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX"
}
```

Locale is one of following: ``it_IT`` ``ru_RU`` ``en_GB`` ``zh_TW`` ``ko_KR`` ``en_US`` ``es_MX`` ``pt_BR`` ``es_ES`` ``zh_CN`` ``fr_FR`` ``de_DE``, will change the language for item search. (Default is ``en_US``)

Get client_id/client_secret here:

https://develop.battle.net/access/ or https://develop.battle.net/access/clients (if connected)

Click 'create' or https://develop.battle.net/access/clients/create (if connected)

```
client name: anything you want
redirect urls: empty
check I don't have service urls
Intended use: Auction house
```
then validate, and click on your new app

Copy client_id and client_secret to the ``settings`` file

## Run the program
```bash
python3 main.py [list of ids]
```
Example:
```bash
python3 main.py 76061 161134 67151
```
will get you this result:
```
WRITE: Not written, same data from same hour.
=============================================
Reins of Poseidus
67151         5750.0         1
67151         5750.0         1
...                                           # Actual results are here, this is just a condensed version
67151        19990.0         1
67151        19990.0         1
=============================================
Spirit of Harmony
76061          190.0         1
76061          190.0         1
...                                           # Actual results are here, this is just a condensed version
76061        19000.0         8
76061       438131.0         4
=============================================
Mecha-Mogul Mk2
161134      129000.0         1
161134      129000.0         1
...                                           # Actual results are here, this is just a condensed version
161134      129000.0         1
161134      999999.0         1
```
