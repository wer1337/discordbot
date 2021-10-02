import yaml

class Config:
    def __init__(self):
        pass
        
    def open_yaml(self):
        with open("app_config.yml", "r") as config:
            return yaml.safe_load(config)
        