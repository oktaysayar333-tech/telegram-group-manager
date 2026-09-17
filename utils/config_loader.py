import yaml
import sys

def load_config(path='config.yaml'):
    """
    Load configuration from a YAML file.

    Args:
        path (str): Path to the YAML configuration file.

    Returns:
        dict: Dictionary containing the loaded credentials.

    Raises:
        SystemExit: If the file is not found, a key is missing, or YAML parsing fails.
    """
    try:
        with open(path, 'r', encoding='utf-8') as file:
            return yaml.safe_load(file)['credentials']
    except (FileNotFoundError, KeyError, yaml.YAMLError) as e:
        print(f"Error loading configuration: {e}")
        sys.exit(1)