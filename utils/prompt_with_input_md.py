import sys
# setting path
sys.path.append('../')

from openai import OpenAI
import json
from weather import forecast, marine
from dict2xml import dict2xml
from models.Destination import Destination
from models.Coordinates import Coordinates

client = OpenAI()

def get_result(location, localtime):
    latitude = str.split(location['Coordinates'], ',')[0]
    longitude = str.split(location['Coordinates'], ',')[1]
    coords = Coordinates(lat=latitude, lon=longitude)
    weather_json = forecast(coords)
    marine_json = marine(coords)

    weather_dict = json.loads(weather_json)
    marine_dict = json.loads(marine_json)

    weather_xml = dict2xml(weather_dict, wrap="weather", indent="       ")
    marine_xml = dict2xml(marine_dict, wrap="marine", indent="      ")

    messages = [    
        {
            "role": "system",
            "content": """
            You are a sailboat expert.
            Your main objective is to provide a weeks plan for a User, who wants to plan his sailing journey. 
            User provides you with sailingData which contains his current location, weather information (wind + marine wave data) for his location, his boat information and his experience in sailing.
            When user provides you with all the data, you provide him with 1 week planned trip which contains:
            - each day nearby port to travel
            - each port coordinates
            - distance between ports in Nautical Miles
            - each trip duration in hours and minutes (00:00)
            - safety aspect based on weather and experience of the sailor for each day

            Provide the output in JSON only and no additional text."""
            # Pass the json schema to the model. Pretty printing improves results.
            # f" The JSON object must use the schema: {json.dumps(Destination.model_json_schema(), indent=2)}"
        },
        {
            "role": "user",
            "content": f"""
<sailingData>
    <location>
        <name>{location['Name']}</name>
        <region>{location['Region']}</region>
        <lat>{coords.lat}</lat>
        <lon>{coords.lon}</lon>
        <localtime>{localtime}</localtime>
    </location>
    {weather_xml}
    {marine_xml}
    <boatInfo>
        <boatType>Cruising Yacht</boatType>
        <length>12.5</length>
        <width>4.2</width>
        <waterlineDepth>1.8</waterlineDepth>
        <mastHeight>16.0</mastHeight>
        <displacement>8500</displacement>
        <keelType>Fin keel</keelType>
        <sailArea>75</sailArea>
        <enginePower>25</enginePower>
        <fuelCapacity>200</fuelCapacity>
        <rudderType>Skeg-hung</rudderType>
        <crewSize>6</crewSize>
        <hullMaterial>Fiberglass</hullMaterial>
    </boatInfo>
    <experience>
        <yearsOfExperience>7</yearsOfExperience>
        <experienceLevel>Intermediate</experienceLevel>
        <typeOfWaterSailed>
            <waterType>Coastal</waterType>
            <waterType>Inland Waters</waterType>
        </typeOfWaterSailed>
        <typesOfBoatsSailed>
            <boatType>Monohull</boatType>
            <boatType>Dinghy</boatType>
        </typesOfBoatsSailed>
        <certifications>
            <certification>ASA 101 Basic Keelboat Sailing</certification>
            <certification>ASA 103 Coastal Navigation</certification>
        </certifications>
        <totalMilesSailed>2500</totalMilesSailed>
        <soloSailingExperience>No</soloSailingExperience>
        <sailingCoursesTraining>
            <course>Coastal Cruising</course>
            <course>Advanced Seamanship</course>
        </sailingCoursesTraining>
    </experience>
</sailingData>
    """
        }
    ]
    completion = client.beta.chat.completions.parse(
        model="gpt-4o",
        temperature=1,
        max_tokens=8000,
        messages=messages,
        seed=42,
        response_format={"type": "json_object"} # Destination
    )
    input = messages[1]['content']
    return input, completion.choices[0].message.content