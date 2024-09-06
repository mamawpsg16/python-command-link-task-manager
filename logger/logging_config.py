from logging.config import dictConfig

# Define the logging configuration dictionary
log_config = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'default': {
            'format': '[%(levelname)s:%(asctime)s] - {%(pathname)s:%(lineno)d} - %(message)s',
        },
        'simple': {
            'format': '%(levelname)s - %(message)s'
        },
    },
    'handlers': {
        'file': {
            'class': 'logging.FileHandler',
            'level': 'ERROR',  # Log only ERROR and CRITICAL messages
            'formatter': 'default',
            'filename': 'error.log',  # File to which errors are logged
        },
        'console': {
            'class': 'logging.StreamHandler',
            'level': 'DEBUG',  # Log all levels to the console
            'formatter': 'simple',
        },
    },
    'loggers': {
        'myapp': {
            'handlers': ['file', 'console'],
            'level': 'DEBUG',  # Set logger level to DEBUG
            'propagate': False,
        },
    },
    'root': {
        'handlers': ['file'],
        'level': 'DEBUG',  # Set root logger level to DEBUG
    },
}

def setup_logging():
    dictConfig(log_config)
