import requests

FILE_ID = "18ofUcldVfP_8a3brjGqZBSbzq-5F6yvt"

url = f"https://drive.google.com/uc?export=download&id={FILE_ID}"

response = requests.get(url)

print(response.text[:1000])