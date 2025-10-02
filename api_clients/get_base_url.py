import configparser
import os


CONFIG_FILE_PATH = os.path.join(os.path.dirname(__file__), '../config.ini')

def load_config(config_path):
    """
    Reads and parses the configuration file.
    
    Args:
        config_path (str): The path to the configuration file.
        
    Returns:
        configparser.ConfigParser: The loaded configuration object.
    """
    config = configparser.ConfigParser()
    
    if not os.path.exists(config_path):
        raise FileNotFoundError(f"Configuration file not found at: {config_path}")

    # Read the file
    config.read(config_path)
    return config


def extract_base_url(section):
    """
    Retrieves the BASE_URL from the specified section of the configuration file.
    
    Args:
        section (str): The section in the config file where BASE_URL is located.
        
    Returns:
        str: The BASE_URL value.
    """
    config = load_config(CONFIG_FILE_PATH)
    
    if section not in config:
        raise ValueError(f"Section '{section}' not found in the configuration file.")
    
    if 'BASE_URL' not in config[section]:
        raise ValueError(f"'BASE_URL' not found in section '{section}'.")
    
    return config[section]['BASE_URL']