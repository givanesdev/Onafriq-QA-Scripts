import json
import sys

import requests


class OnafriqAPI:
    BASE_URL = "https://restful-booker.herokuapp.com"

    # common headers
    HEADERS = {
        'Content-Type': 'application/json'
    }

    # Function to create a booking
    def create_booking(self) -> int:
        payload = {
            "firstname": "Henry",
            "lastname": "Stanly",
            "totalprice": 350,
            "depositpaid": True,
            "bookingdates": {
                "checkin": "2024-04-15",
                "checkout": "2024-04-20"
            },
            "additionalneeds": "Massage, Morning breakfast, Fitness coach workout."
        }

        response = requests.post(f"{self.BASE_URL}/booking", headers=self.HEADERS, data=json.dumps(payload))
        if response.status_code == 200 or response.status_code == 201:
            response_data = response.json()
            print("Created Booking With id :", response_data['bookingid'])
            return int(response_data['bookingid'])
        else:
            print(f"Failed to create booking :: {response.text}")
            return 0

    # Function to get the booking details
    def get_booking(self, booking_id: int) -> dict:
        response = requests.get(f"{self.BASE_URL}/booking/{booking_id}", headers=self.HEADERS)
        if response.status_code == 200:
            response_data = response.json()
            print(
                f"Found Booking with id :: {booking_id} checkout :: {response_data['bookingdates']['checkout']}"
                f" additionalneeds :: {response_data['additionalneeds']}")
            return response_data
        else:
            print(f"Failed to get booking with ID {booking_id} :: {response.text}")
            return {}

    # Function to update the booking
    def update_booking(self, booking_id: int, booking: dict) -> int:
        # Authenticate to get the token
        auth_response = requests.post(f"{self.BASE_URL}/auth", headers=self.HEADERS,
                                      data=json.dumps({"username": "admin", "password": "password123"}))

        if auth_response.status_code == 200:
            print(f"We have an oauth token :: {auth_response.json()['token']}")
            token = auth_response.json()['token']
            headers_with_auth = {
                'Content-Type': 'application/json',
                'Cookie': f'token={token}'
            }
            booking["additionalneeds"] = f"{booking['additionalneeds']} He checked in 2 days late, so we extended his stay by two days."
            booking['bookingdates']["checkout"] = "2024-4-22"
        else:
            print(f"Failed to authenticate  {auth_response.text}")
            return 0

        url = f"{self.BASE_URL}/booking/{booking_id}"
        response = requests.put(url, headers=headers_with_auth, data=json.dumps(booking))

        if response.status_code == 200:
            response_data = response.json()
            print(
                f"Updated Booking with id :: {booking_id} checkout :: {response_data['bookingdates']['checkout']}"
                f" additionalneeds :: {response_data['additionalneeds']}")
            return 1
        else:
            print(f"Failed to update booking with ID {booking_id} : {response.text}")
            return 0


if __name__ == "__main__":
    try:
        api = OnafriqAPI()
        bid = api.create_booking()
        if bid > 0:
            bk = api.get_booking(bid)
            if len(bk) != 0:
                rt = api.update_booking(bid, bk)
                if rt == 1:
                    print("We have created, retrieved and updated the booking successfully")
                else:
                    print("We have created, retrieved but failed to update the booking")
            else:
                print("We have created  but failed to retrieve the booking")
        else:
            print("We have failed to create the booking")
    except KeyboardInterrupt:
        sys.exit(0)