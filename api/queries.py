from prompt import get_result
from datetime import datetime
import logging
from utils import obj_convert

logging.basicConfig(level=logging.ERROR)
logger = logging.getLogger(__name__)

def getTripPlan_resolver(obj, info, loc):
    try:
        logger.debug(f"Received location input: {loc}")
        
        if not loc:
            raise ValueError("Location input is empty")
            
        location = obj_convert.dict2loc(loc)
        logger.debug(f"Created Location object: {location}")
        
        localDateTime = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        logger.debug(f"Current datetime: {localDateTime}")
        
        dict = obj_convert.string2dict(get_result(location, localDateTime))
        result = obj_convert.dict2dest(dict.get('destinations', []))
        logger.debug(f"Got result from get_result: {result}")
            
        if not result:
            raise ValueError("No results returned from get_result")
            
        payload = {
            "success": True,
            "destinations": result,
            "errors": None
        }
        return payload
        
    except AttributeError as e:
        logger.error(f"AttributeError: {str(e)}")
        payload = {
            "success": False,
            "destinations": [],
            "errors": [f"Invalid location format: {str(e)}"]
        }
    except ValueError as e:
        logger.error(f"ValueError: {str(e)}")
        payload = {
            "success": False,
            "destinations": [],
            "errors": [str(e)]
        }
    except Exception as e:
        logger.error(f"Unexpected error: {str(e)}")
        payload = {
            "success": False,
            "destinations": [],
            "errors": ["An unexpected error occurred"]
        }
    return payload