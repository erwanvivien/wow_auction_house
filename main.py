import os
import json
import requests
import datetime
import sys


def read_file(path):
    f = open(path, "r")
    string = f.read()
    f.close()
    return string


def write_file(path, string, timestamp=False):
    time = datetime.datetime.now()
    path_time = path + "_" + time.strftime("%Y-%m-%d_%H") + "h.json"

    if os.path.exists(path_time):
        print("WRITE: Not written, same data from same hour.")
        return read_file(path_time)

    # Always overwrite default
    f = open(path + ".json", "w")
    f.write(string)
    f.close()

    # Creates times save if needed.
    if timestamp:
        f = open(path_time, "w")
        f.write(string)
        f.close()

    return string


def create_access_token(client_id, client_secret, region='eu'):
    data = {
        'grant_type': 'client_credentials'
    }

    response = requests.post(f'https://{region}.battle.net/oauth/token',
                             data=data, auth=(client_id, client_secret))

    return response


# reads the 'settings' file
settings = json.loads(read_file("settings"))
# print(settings)


region = settings["region"]
realm_name = settings["realm"]
client_id = settings["client_id"]
client_secret = settings["client_secret"]

# try creating a token
try:
    token = create_access_token(client_id, client_secret).json()[
        "access_token"]
except:
    print("Token was not given by Blizz API")
    exit()

# Gets the whole auction house for a realm
r = requests.get(
    f"https://{region}.api.blizzard.com/data/wow/realm/{realm_name}?namespace=dynamic-{region}&locale=en_GB&access_token={token}")

# Get the base request url
try:
    base_url = r.json()["connected_realm"]["href"].split("?")[0]
except:
    print("json was bad")
    print(r.text)
    exit()
# print(base_url)

r = requests.get(
    f"{base_url}/auctions?namespace=dynamic-{region}&locale=en_US&access_token={token}")

# saving the request to region-server and region-server-date
auctions = write_file(f"{region}-{realm_name}",
                      r.text, True)


auctions_json = json.loads(auctions)
ids = [int(x) for x in sys.argv[1:]]
act_list = []
# Parse all the AH for the items we have
for auction in auctions_json["auctions"]:
    if auction["item"]["id"] in ids:
        try:
            price = auction["buyout"] / 10000
        except:
            price = auction["unit_price"] / 10000

        act_list += [(auction["item"]["id"], price, auction["quantity"])]

act_list.sort()
# print(act_list)
prev = 0
for auction in act_list:
    if (auction[0] != prev):
        prev = auction[0]
        print("=============================================")
        r = requests.get(
            f"https://{region}.api.blizzard.com/data/wow/item/{prev}?namespace=static-{region}&locale=en_US&access_token={token}")
        print(r.json()["name"])

    print(auction[0], end='')

    mid_space = 20 - len(str(auction[0])) - len(str(auction[1]))
    print(' ' * mid_space, end='')

    print(auction[1], end='')

    mid_space = 10 - len(str(auction[2]))
    print(' ' * mid_space, end='')

    print(auction[2], end='\n')


# r = requests.get(f"https://{region}.battle.net/oauth/token")
# print(r.json())

# https://{region}.api.blizzard.com/data/wow/realm/{realm_name}?namespace=dynamic-{region}&locale=en_GB&access_token={token}

# https://{region}.api.blizzard.com/data/wow/connected-realm/{realm_id}/auctions?namespace=dynamic-{region}&locale=en_US&access_token={token}
# {base_url}/auctions?namespace=dynamic-{region}&locale=en_US&access_token={token}

# https://{region}.api.blizzard.com/data/wow/item/{item_id}?namespace=static-{region}&locale=en_US&access_token={token}
