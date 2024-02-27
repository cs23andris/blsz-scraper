import os
import yaml


def config_parser(pathname: str = None) -> dict:
    """This function is used to parse the  app config file and return it as a dictionary.
    Parameters
    ----------
    pathname : str, optional
        The path of the app config file. Defaults to None.
    Returns
    -------
    dict
        A dictionary containing the config information
    """

    if pathname is None:
        base_path = os.path.dirname(os.path.abspath(__file__))
        config_file_path = os.path.join(base_path, "config.yaml")
    else:
        config_file_path = pathname
    with open(config_file_path) as router_config_yaml:
        rc = yaml.load(router_config_yaml, Loader=yaml.SafeLoader)

    return rc


def get_config_by_team(parsed_config: dict, team_name: str) -> dict:
    """This function is used to get the config for a specific team from the parsed config file."""
    
    return [
        schedule
        for schedule in parsed_config["schedules"]
        if schedule["team_name"] == team_name
    ][0]


def get_credentials_path() -> str:
    """This function is used to get the path of the credentials file for the google calendar authentication."""
    
    base_path = os.path.dirname(os.path.abspath(__file__)).removesuffix("/app")
    credentials_path = os.path.join(base_path, ".credentials", "credentials.json")
    return credentials_path
