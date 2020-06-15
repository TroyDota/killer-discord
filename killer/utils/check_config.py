import logging

log = logging.getLogger("killer")

config_sections = {"main": ["token", "prefix"]}


def check_config(config):
    for section, fields in config_sections.items():
        if section not in config:
            raise InvalidConfig(f"[{section}] section not in config.")
        for field in fields:
            if field not in config[section]:
                raise InvalidConfig(f"{field} not in {section} section in config.")


class InvalidConfig(Exception):
    pass
