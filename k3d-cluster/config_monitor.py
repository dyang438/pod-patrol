#!/usr/bin/env python3
import os
import time
import json
import logging
from pathlib import Path

# Set up logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger('config-monitor')

# Constants
STATUS_FILE = '/usr/src/app/status.json'
CHECK_INTERVAL = 10  # seconds

def check_config():
    """Check if the required environment variable is set correctly"""
    try:
        # Check for REQUIRED_ENV (which should come from MISSING_KEY in ConfigMap)
        required_env = os.environ.get('REQUIRED_ENV')

        # Also check if the actual correct key's value is available
        correct_value = os.environ.get('CORRECT_KEY')

        if required_env:
            logger.info(f"REQUIRED_ENV is set to: {required_env}")
            status = "healthy"
            message = "Configuration is properly set"
        else:
            logger.warning("REQUIRED_ENV is not set!")
            if correct_value:
                logger.info(f"However, CORRECT_KEY is available with value: {correct_value}")
                message = "REQUIRED_ENV missing but CORRECT_KEY is available"
            else:
                logger.warning("CORRECT_KEY is also not available")
                message = "Both REQUIRED_ENV and CORRECT_KEY are missing"
            status = "unhealthy"

        # Save status to file for the web service to read
        result = {
            "status": status,
            "message": message,
            "timestamp": time.time()
        }

        Path(STATUS_FILE).parent.mkdir(parents=True, exist_ok=True)
        with open(STATUS_FILE, 'w') as f:
            json.dump(result, f)

        return status, message

    except Exception as e:
        logger.error(f"Error checking configuration: {str(e)}")
        result = {
            "status": "error",
            "message": f"Error checking configuration: {str(e)}",
            "timestamp": time.time()
        }

        try:
            with open(STATUS_FILE, 'w') as f:
                json.dump(result, f)
        except:
            logger.error("Could not write status file")

        return "error", str(e)

def main():
    logger.info("Config monitoring service starting...")

    while True:
        status, message = check_config()
        logger.info(f"Config status: {status} - {message}")
        time.sleep(CHECK_INTERVAL)

if __name__ == "__main__":
    main()