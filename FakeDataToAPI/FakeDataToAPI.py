
from faker import Faker
from datetime import timedelta
import time
import requests
import json

def http_post(url, data):
    headers = {'content-type': 'application/json'}

    try:
        http = requests.post(url=url, data=data, headers=headers )
        code = http.status_code
    except Exception as e:
        print("Fatal error: {0}".format(e))
        return None

    return code

def create_maschine_fake_data(MAX_NUMBER_FAKE_INFO):  

    faker = Faker()
    
    data = list()

    for _ in range(MAX_NUMBER_FAKE_INFO):
        json_data = {
        'maschine': 'MASCHINE00' + str(faker.random_int(min=0, max=9) + faker.random_int(min=0, max=9) + faker.random_int(min=0, max=9)),
        'address': str(faker.street_address()),
        'city': faker.city(),
        'software': 'genericOS',
        'hardware': "SERVER",
        'ip': str(faker.ipv4_public(network=False, address_class=None))
        }    
        data.append( json.dumps(json_data) )

    return data

def create_package_fake_data(MAX_NUMBER_FAKE_INFO):  

    faker = Faker()
    
    data = list()

    for _ in range(MAX_NUMBER_FAKE_INFO):
        json_data = {
        'name': 'PACKAGE_' + faker.uri_page(),
        'description': 'some actions',
        'path': 'root',
        'reboot': faker.boolean(chance_of_getting_true=50)
        }    
        data.append( json.dumps(json_data) )

    return data


def send_fake_data(maschine_data, package_data):
    maschine_api      = 'http://localhost:4000/api/maschine'
    package_api   = 'http://localhost:4000/api/package' 

    # Send data and take the results
    for maschine in maschine_data:
        maschine_result = http_post(maschine_api, maschine)

    for package in package_data:
        package_result = http_post(package_api, package)

    result = [{
        'code': maschine_result,
        'name': 'MASCHINE DATA'
        },
        {
        'code': package_result,
        'name': 'PACKAGE DATA'
        }]

    return result


def print_time(start):
    end = time.monotonic()
    print(f"Duration query: {timedelta(seconds=end - start)}")
    return


def print_result(confirm=list()):
    tabs = "\t\t"
    
    for i in range(len(confirm)):
        if (confirm[i]['code'] != 200):
            print(f"TYPE DATA {confirm[i]['name']} Error to send data to db!{tabs}DETAIL: {str(confirm[i]['code']) }" )
        else:
            print(f"TYPE DATA {confirm[i]['name']} Upload data with success!{tabs}DETAIL: {str(confirm[i]['code'])}" )


def input_parameters():
    try:
        # Step 1. number of pv 
        maschine_to_insert = int(input("Inserire il numero delle maschine-fake da inviare al db: "))
        if(maschine_to_insert < 500):
            print(f"Verranno generati ed inseriti {maschine_to_insert} finti maschine. \n")
        else:
            maschine_to_insert = input("Inserire correttamente il numero(<500) delle maschine: \n")
    
        # Step 2. number of patches
        package_to_insert = int(input("Inserire il numero dei package-fake da inviare al db: "))
        if(package_to_insert < 500):
            print(f"Verranno generati ed inseriti {package_to_insert} finti package. \n")
        else:
            package_to_insert = input("Inserire correttamente il numero(<500) dei package: \n")

        return [maschine_to_insert, package_to_insert]

    except Exception as e:
        print("Errore durante l'inserimento dei parametri richiesti ")
        return -1

def main():
    start = time.monotonic()
    print("Start FakeDataToAPI.py")

    params = input_parameters()
    
    maschine_data = create_maschine_fake_data(params[0])
    package_data = create_package_fake_data(params[1])
    
    # Send data using restful api
    print_result(confirm=send_fake_data(maschine_data, package_data))

    #  Wait some input..
    print_time(start)
    if input():
        return

if __name__ == "__main__":
    main()