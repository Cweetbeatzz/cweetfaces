from brownie import CweetFaces, network
from .helpers import get_account, get_face
from metadata import sample
from pathlib import Path
import requests
import json
import os

#########################################################
face_to_image_uri = {}


def main():
    account = get_account()
    prev_transaction = CweetFaces[-1]
    number_index_of_face = prev_transaction.tokenCounter()
    print(f"Created {number_index_of_face} Collectables")
    for tokenId in range(number_index_of_face):
        face = get_face(prev_transaction.tokenIdToFace(tokenId))
        metadata_file_name = (
            f"../metadata/{network.show_active()}/{tokenId}-{face}.json"
        )
        print(metadata_file_name)

        collectable_metadata = sample.sample_template

        if Path(metadata_file_name):
            print(f"{metadata_file_name} already exists")
        else:
            print(f"Creating MetaData File: {metadata_file_name}")

            collectable_metadata["name"] = face
            collectable_metadata["description"] = f"Silly Simile {face} Face"
            image_file_path = "../images/ + face.lower().replace(" "," - ") + .png "
            image_uri = None
            if os.getenv("UPLOAD_IPFS") == "true":
                image_uri = upload_to_ipfs(image_file_path)

            image_uri = image_uri if image_uri else face_to_image_uri[face]

            collectable_metadata["image_uri"] = image_uri

            with open(metadata_file_name, "w") as file:
                json.dump(collectable_metadata, file)
            upload_to_ipfs(metadata_file_name)


#########################################################


def upload_to_ipfs(image_file_path):
    with Path(image_file_path).open("rb") as fp:
        image_binary = fp.read()
        ipfs_url = "http://127.0.0.1:8080"
        endpoint = "/api/v0/add"
        response = requests.post(ipfs_url + endpoint, files={"file": image_binary})
        ipfs_hash = response.json()["Hash"]
        filename = image_file_path.split("/")[-1:][0]
        image_uri = f"https://ipfs.io/ipfs/{ipfs_hash}?filename={filename}"
        print(image_uri)
        return image_uri
