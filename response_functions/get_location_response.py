
def get_location_response(req, CMU_dining_dict):
    result = req.get("result")
    parameters = result.get("parameters")
    location = parameters.get("location")
    
    directions = CMU_dining_dict[location]["location"] # string

    return (location + " is located in the " + directions)
