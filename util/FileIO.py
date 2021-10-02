import yaml
import json

class Config:
    def __init__(self):
        pass
        
    def open_yaml(self):
        with open("app_config.yml", "r") as config:
            return yaml.safe_load(config)
        

def import_json(key_name: str):
    with open(f"util/emojis.json", "r") as json_file:
        json_data = json.load(json_file)
        
    return json_data[key_name]