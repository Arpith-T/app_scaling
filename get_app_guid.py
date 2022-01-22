import subprocess


def app_guid(app):
    login = subprocess.run('cf login -a https://api.cf.sap.hana.ondemand.com -o "CPI-Global-Canary_aciat001"  -s '
                           'prov_eu10_aciat001 -u prism@global.corp.sap -p Prisminfra529#5')
    # print(login)

    output = subprocess.run(f"cf app {app} --guid", stdout=subprocess.PIPE)

    output_in_str = str(output.stdout)  # prints the standard output of the guid

    # print(output_in_str[2:-3])

    return output_in_str[2:-3]


# app_guid(app="it-co")
# print(app_guid(app="it-gb"))

# app_guid()

def main():
    print(app_guid(app=input("Enter app name - ")))


if __name__ == "__main__":
    main()
