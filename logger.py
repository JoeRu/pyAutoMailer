import logging
import os
#-------------Output Logger
# create logger
logger = logging.getLogger(os.path.basename(__file__))
#logger.setLevel(logging.INFO)
logger.setLevel(logging.DEBUG)
# create console handler with a higher log level
ch = logging.StreamHandler()
#ch.setLevel(logging.INFO)
ch.setLevel(logging.DEBUG)

# create file handler which logs even debug messages
fh = logging.FileHandler('pyAutomail.log')
fh.setLevel(logging.ERROR)

# create formatter and add it to the handlers
#formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
formatter = logging.Formatter('%(levelname)s - %(message)s')
fh.setFormatter(formatter)
ch.setFormatter(formatter)
# add the handlers to the logger
logger.addHandler(fh)
logger.addHandler(ch)
#-------------Output Logger