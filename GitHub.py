from flask import Blueprint, jsonify, redirect, url_for, request
import requests
import json
import os
import numpy as np

github = Blueprint("github", __name__)

GITHUB_API = "https://api.github.com"
API_TOKEN = os.getenv("GIT_TOKEN")

# form a request URL
url = GITHUB_API + "/gists"
print("Request URL: %s" % url)

# set headers,parameters,payload
headers = {"Authorization": "token %s" % API_TOKEN}
params = {"scope": "gist"}
payload = {
    "description": "my gists",
    "public": True,
}


@github.route("/github/gists/", methods=["POST", "GET"])
def git():
    if request.method == "POST":
        result = json.loads(request.data.decode("utf-8"))
        payload.update(result)
        res = requests.post(
            url, headers=headers, params=params, data=json.dumps(payload)
        )
        j = json.loads(res.text)
        return jsonify({"id": j["id"]})
    else:
        run = True
        gist_array = []
        page = 1
        while run:
            data = requests.get(
                f"{url}?page={page}&per_page=100", headers=headers, params=params
            )
            result = json.loads(data.content.decode("utf-8"))
            page += 1
            gist_array.extend(result)
            if len(result) < 100:
                run = False
        return jsonify(gist_array)


@github.route("/github/gist/<id>", methods=["GET"])
def gist(id):
    print(id)
    res = requests.get(url + f"/{id}", headers=headers, params=params)
    result = json.loads(res.content.decode("utf-8"))
    return result
