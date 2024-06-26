#!/usr/bin/env python3
from jwt import JWT, jwk_from_pem
import time
import requests

pem = "aalp-self-hosted-runner.2024-06-21.private-key.pem"
client_id = "Iv23lixzRYO8eKFZQCxt"
installation_id = "52081584"  # Replace with your actual installation ID

# Open PEM
with open(pem, 'rb') as pem_file:
    signing_key = jwk_from_pem(pem_file.read())

payload = {
    # Issued at time
    'iat': int(time.time()),
    # JWT expiration time (in sec, 10 minutes maximum)
    'exp': int(time.time()) + 60,
    # GitHub App's client ID
    'iss': client_id
}

# Create JWT
jwt_instance = JWT()
jwt = jwt_instance.encode(payload, signing_key, alg='RS256')

# Set the URL for the request
url = f"https://api.github.com/app/installations/{installation_id}/access_tokens"

# Set the headers
headers = {
    "Accept": "application/vnd.github+json",
    "Authorization": f"Bearer {jwt}",
    "X-GitHub-Api-Version": "2022-11-28"
}

# Send the POST request
response = requests.post(url, headers=headers)

# Get the "token" field from the response
token = response.json().get("token")

# get token for creating the runners
org = "accel-sim"  # Replace with your organization name

# Set the URL for the request
url = f"https://api.github.com/orgs/{org}/actions/runners/registration-token"

# Set the headers
headers = {
    "Accept": "application/vnd.github+json",
    "Authorization": f"Bearer {token}",
    "X-GitHub-Api-Version": "2022-11-28"
}

# Send the POST request
response = requests.post(url, headers=headers)

token = response.json().get("token")
print(token)