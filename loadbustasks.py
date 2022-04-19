import json

def load():
    with open("./bus.json") as reader:
        return json.loads(reader.read())