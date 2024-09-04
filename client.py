import requests

response = requests.post(
    "http://127.0.0.1:5000/post/",
    json={"title": "Postgres", "description": "Postgres can be dificult to handle sometimes", "owner": "cool_man"},
)
print(response.status_code)
print(response.json())

response = requests.post(
    "http://127.0.0.1:5000/post/",
    json={"title": "Hello", "description": "Hello world", "owner": "cool_chell"},
)
print(response.status_code)
print(response.json())

response = requests.get("http://127.0.0.1:5000/post/1")
print(response.status_code)

print(response.json())


response = requests.patch(
    "http://127.0.0.1:5000/post/1",
    json={"name": "new_name_3", "description": "new_password"}

)
print(response.status_code)
print(response.json())

response = requests.get(
    "http://127.0.0.1:5000/post/1",

)
print(response.status_code)
print(response.json())


response = requests.delete(
    "http://127.0.0.1:5000/post/1",

)
print(response.status_code)
print(response.json())

response = requests.get(
    "http://127.0.0.1:5000/post/1",

)
print(response.status_code)
print(response.json())
