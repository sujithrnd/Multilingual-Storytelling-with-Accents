import logging

#For logging purpose
#@author Sujith KS
class Logger:
    #Debug messages
    def debug(self,message):
            # Basic configuration
        logging.basicConfig(level=logging.DEBUG)
        logging.debug(message)
        return logging



    # Basic configuration
    #logging.basicConfig(level=logging.DEBUG)
    # Example log messages
    #logging.debug("This is a debug message.")
    #logging.info("This is an info message.")
    #logging.warning("This is a warning message.")
    #logging.error("This is an error message.")
    #logging.critical("This is a critical message.")
