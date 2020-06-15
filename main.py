if __name__ == "__main__":
    import logging

    from killer import bot
    from killer import utils

    utils.init_logging()

    args = utils.parse_args()
    config = utils.config_parser(args["config"])
    utils.check_config(config)

    main = bot.Bot(config)
    main.start()
    main.run()
