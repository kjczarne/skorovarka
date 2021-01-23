import yaml

def parse_yaml(file_path=None):

    if not file_path:
        file_path = ".svk-hints.yaml"
    
    with open(file_path, "r") as f:
        yaml_obj = yaml.full_load(f)
    
    return yaml_obj