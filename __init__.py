import logging

applogger = logging.getLogger('app')
applogger.setLevel(logging.INFO)
sh = logging.StreamHandler()
sh.setFormatter(logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s"))
applogger.addHandler(sh)