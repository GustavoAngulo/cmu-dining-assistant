
def get_info_response(req, CMU_dining_dict):
    result = req.get("result")
    parameters = result.get("parameters")
    location = parameters.get("location")
    
    return CMU_dining_dict[location]["description"] + \
            " Is there anything else I can help with?" # string

