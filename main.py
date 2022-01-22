import json
import os
import subprocess
import time
import requests


def cf_oauth_token():
    login = subprocess.run(
        f'cf login -a https://api.cf.sap.hana.ondemand.com -o "CPI-Global-Canary_aciat001"  -s prov_eu10_aciat001 -u prism@global.corp.sap -p Prisminfra529#5')
    # print(login)

    oauth_token = subprocess.run("cf oauth-token", stdout=subprocess.PIPE)

    oauth_token_string = str(oauth_token.stdout)

    return oauth_token_string[2:-3]

def app_guid(app):
    login = subprocess.run('cf login -a https://api.cf.sap.hana.ondemand.com -o "CPI-Global-Canary_aciat001"  -s '
                           'prov_eu10_aciat001 -u prism@global.corp.sap -p Prisminfra529#5')
    # print(login)

    output = subprocess.run(f"cf app {app} --guid", stdout=subprocess.PIPE)

    output_in_str = str(output.stdout)  # prints the standard output of the guid

    # print(output_in_str[2:-3])

    return output_in_str[2:-3]

def read_config():
    with open('config.json') as data_file:
        config_file = json.load(data_file)
    return config_file

config = read_config()
# guid = app_guid(app=config["app_name"])

guid = app_guid(os.getenv("MTMS"))
oauth_token = cf_oauth_token()


def scale_down_mtms(guid):
    url = f"https://api.cf.sap.hana.ondemand.com/v3/processes/{guid}/actions/scale"

    payload = json.dumps({
        "instances": 2
    })
    headers = {
        'Authorization': f'{oauth_token}',
        'Content-Type': 'application/json',
        'Cookie': 'JTENANTSESSIONID_kr19bxkapa=FPtRDK1dM3D1lD56pq9oAq9mvHn19ohxqXjClhqrbLI%3D'
    }

    response = requests.request("POST", url, headers=headers, data=payload)

    print(response.text)

def scale_up_mtms(guid):
    url = f"https://api.cf.sap.hana.ondemand.com/v3/processes/{guid}/actions/scale"

    payload = json.dumps({
        "instances": 3
    })
    headers = {
        'Authorization': f'{oauth_token}',
        'Content-Type': 'application/json',
        'Cookie': 'JTENANTSESSIONID_kr19bxkapa=FPtRDK1dM3D1lD56pq9oAq9mvHn19ohxqXjClhqrbLI%3D'
    }

    response = requests.request("POST", url, headers=headers, data=payload)

    print(response.text)


# scale_down_mtms(guid=guid)

# scale_up_mtms(guid)

def scale_down_and_up(guid):
    scale_down_mtms(guid)
    # time.sleep(900)
    time.sleep(int(os.getenv("DOWNTIME")))
    scale_up_mtms(guid)


scale_down_and_up(guid)
