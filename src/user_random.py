import uuid
from typing import Any, Dict

import requests


def get_data() -> Dict[str, str]:
    response = requests.get("https://randomuser.me/api/")
    response.raise_for_status()
    data = response.json()["results"][0]
    return data


def format_data(data: Dict[str, Any]) -> Dict[str, Any]:
    location = data["location"]

    formatted_data = {
        "id": str(uuid.uuid4()),
        "first_name": data["name"]["first"],
        "last_name": data["name"]["last"],
        "gender": data["gender"],
        "address": f"{location['street']['number']} {location['street']['name']}, "
        f"{location['city']}, {location['state']}, {location['country']}",
        "post_code": location["postcode"],
        "email": data["email"],
        "username": data["login"]["username"],
        "dob": data["dob"]["date"],
        "registered_date": data["registered"]["date"],
        "phone": data["phone"],
        "picture": data["picture"]["medium"],
    }

    return formatted_data
