import sys
# setting path
sys.path.append('../')

from openai import OpenAI
import json
from weather import forecast, marine
from dict2xml import dict2xml
from models.Destination import Destination
from models.Coordinates import Coordinates

client = OpenAI(
    project="proj_0v741Xdrt8NvmO2kOs1prFcr",
    api_key="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"
)

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
            "content": "You are a sailboat expert, providing useful insights to the captain in JSON.\n"
            # Pass the json schema to the model. Pretty printing improves results.
            f" The JSON object must use the schema: {json.dumps(Destination.model_json_schema(), indent=2)}"
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
    <goal>
        <comfort>Various</comfort>
        <maxTripDuration>08:00</maxTripDuration>
    </goal>
</sailingData>
Based on provided location, weather forecast, marine forecast, boatInfo and goal could you please provide me with 3 destinations to travel?
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