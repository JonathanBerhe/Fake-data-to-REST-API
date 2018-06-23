
from faker import Faker
from datetime import timedelta
import time
import requests
import json



def send_fake_data(MAX_NUMBER_FAKE_INFO):

    faker = Faker()
    headers = {'content-type': 'application/json'}

    for _ in range(MAX_NUMBER_FAKE_INFO):
        json_data = {
        'codPv': 'AP040' + str(faker.random_int(min=0, max=9) + faker.random_int(min=0, max=9) + faker.random_int(min=0, max=9)),
        'address': str(faker.street_address()),
        'city': faker.city(),
        'software': 'PPEU04.09B',
        'hardware': "PPEU SC 2014",
        'ip': str(faker.ipv4_public(network=False, address_class=None))
        }
        
        json_data = json.dumps(json_data)
        print(json_data)
        try:
            http = requests.post('http://localhost:4000/api/pv', data=json_data, headers=headers )
            code = http.status_code
        except Exception as e:
            print("Fatal error: {0}".format(e))
            return None

    return code


def print_time(start):
    end = time.monotonic()
    print("Duration query: {}".format(timedelta(seconds=end - start)))
    return


def print_result(confirm=int()):
    tabs = "\t\t"

    if (confirm != 200):
        print("OUTCOME" + "Error to send data to db!" + tabs + "DETAIL: " + str(confirm))
    else:
        print("OUTCOME" + "Upload data with success!" + tabs + "DETAIL: " + str(confirm))



def main():
    start = time.monotonic()
    print("Start FakeDataToAPI.py")
    
    # Send data using restful api
    #confirm = send_fake_data(300)

    print_result(confirm=send_fake_data(300))


    #  Wait some input..
    print_time(start)
    if input():
        return

if __name__ == "__main__":
    main()