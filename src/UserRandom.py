import uuid

import requests


class RandomUser:
    def __self__(self):
        self.data = None

    def get_data(self):
        response = requests.get("https://randomuser.me/api/")
        response.raise_for_status()
        self.data = response.json()["results"][0]

    def format_data(self):
        if not self.data:
            raise ValueError("Data not loaded. Call get_data() first.")

        location = self.data["location"]
        formatted_data = {
            "id": uuid.uuid4(),
            "first_name": self.data["name"]["first"],
            "last_name": self.data["name"]["last"],
            "gender": self.data["gender"],
            "address": f"{location['street']['number']} {location['street']['name']}, "
            f"{location['city']}, {location['state']}, {location['country']}",
            "post_code": location["postcode"],
            "email": self.data["email"],
            "username": self.data["login"]["username"],
            "dob": self.data["dob"]["date"],
            "registered_date": self.data["registered"]["date"],
            "phone": self.data["phone"],
            "picture": self.data["picture"]["medium"],
        }

        return formatted_data


if __name__ == "__main__":
    user = RandomUser()
    user.get_data()
    formatted_data = user.format_data()
    print(formatted_data)
