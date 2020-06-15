import configparser


def config_parser(config_file):
    config = configparser.ConfigParser()
    config.read(config_file)
    return config
