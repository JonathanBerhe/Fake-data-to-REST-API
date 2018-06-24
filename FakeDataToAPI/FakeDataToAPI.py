
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

def create_pv_fake_data(MAX_NUMBER_FAKE_INFO):  

    faker = Faker()
    
    data = list()

    for _ in range(MAX_NUMBER_FAKE_INFO):
        json_data = {
        'codPv': 'AP040' + str(faker.random_int(min=0, max=9) + faker.random_int(min=0, max=9) + faker.random_int(min=0, max=9)),
        'address': str(faker.street_address()),
        'city': faker.city(),
        'software': 'PPEU04.09B',
        'hardware': "PPEU SC 2014",
        'ip': str(faker.ipv4_public(network=False, address_class=None))
        }    
        data.append( json.dumps(json_data) )

    return data

def create_patch_fake_data(MAX_NUMBER_FAKE_INFO):  

    faker = Faker()
    
    data = list()

    for _ in range(MAX_NUMBER_FAKE_INFO):


        json_data = {
        'name': 'PATCH_' + faker.uri_page(),
        'description': 'some actions',
        'path': 'Telemanut',
        'reboot': faker.boolean(chance_of_getting_true=50)
        }    
        data.append( json.dumps(json_data) )


    return data


def send_fake_data(pv_data, patch_data):
    pv_api      = 'http://localhost:4000/api/pv'
    patch_api   = 'http://localhost:4000/api/patch' 

    # Send data and take the results
    for pv in pv_data:
        pv_result = http_post(pv_api, pv)

    for patch in patch_data:
        patch_result = http_post(patch_api, patch)

    result = [{
        'code': pv_result,
        'name': 'PV DATA'
        },
        {
        'code': patch_result,
        'name': 'PATCH DATA'
        }]

    return result


def print_time(start):
    end = time.monotonic()
    print("Duration query: {}".format(timedelta(seconds=end - start)))
    return


def print_result(confirm=list()):
    tabs = "\t\t"
    
    for i in range(len(confirm)):
        if (confirm[i]['code'] != 200):
            print("TYPE DATA " + confirm[i]['name'] + " Error to send data to db!" + tabs + "DETAIL: " + str(confirm[i]['code']))
        else:
            print("TYPE DATA " + confirm[i]['name'] + " Upload data with success!" + tabs + "DETAIL: " + str(confirm[i]['code']))


def take_input_parameters():
    try:
        # Step 1. number of pv 
        pv_to_insert = int(input("Inserire il numero dei puntivendita-fake da inviare al db: "))
        if(pv_to_insert < 500):
            print("Verranno generati ed inseriti {} finti punti vendita. \n".format(pv_to_insert))
        else:
            pv_to_insert = input("Inserire correttamente il numero(<500) dei pv: \n")
    
        # Step 2. number of patches
        patch_to_insert = int(input("Inserire il numero dei patch-fake da inviare al db: "))
        if(patch_to_insert < 500):
            print("Verranno generati ed inseriti {} finte patch. \n".format(patch_to_insert))
        else:
            patch_to_insert = input("Inserire correttamente il numero(<500) delle patch: \n")

        return [pv_to_insert, patch_to_insert]

    except Exception as e:
        print("Errore durante l'inserimento dei parametri richiesti ")
        return -1

def main():
    start = time.monotonic()
    print("Start FakeDataToAPI.py")

    params = take_input_parameters()
    
    pv_data = create_pv_fake_data(params[0])
    patch_data = create_patch_fake_data(params[1])
    
    # Send data using restful api
    print_result(confirm=send_fake_data(pv_data, patch_data))


    #  Wait some input..
    print_time(start)
    if input():
        return

if __name__ == "__main__":
    main()