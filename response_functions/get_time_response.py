from datetime import date

def get_time_response(req, CMU_dining_dict):
    result = req.get("result")
    parameters = result.get("parameters")
    location = parameters.get("location")
    location_status = parameters.get("location-status")
    
    # reqDate == "" or "YYYY-DD-MM"
    reqDate = parameters.get("date")
    date_responses = ["on Sunday.",
                      "on Monday.", 
                      "on Tuesday.", 
                      "on Wednesday.", 
                      "on Thursday.", 
                      "on Friday.", 
                      "on Saturday."]

    # reqDate: 0 is Sunday, 1 Monday, ..., 6 Saturday             
    if reqDate == "":
        reqDate = (date.today().weekday() + 1) % 7
        speech_date = "today."
    else:
        reqDate = reqDate.split("-")
        reqDate = (date(int(reqDate[0]), 
                        int(reqDate[1]), 
                        int(reqDate[2])).weekday() + 1) % 7
        speech_date = date_responses[reqDate]



    if location_status == "open":
        time = modify_time(get_time(location, "start", reqDate, CMU_dining_dict))

    elif location_status == "close": 
        time = modify_time(get_time(location, "end", reqDate, CMU_dining_dict))
    else:
        time_start = modify_time(get_time(location, "start", reqDate, CMU_dining_dict))
        time_end = modify_time(get_time(location, "end", reqDate, CMU_dining_dict))

    if time == None or time_start == None or time_end == None:
        return (location + " is not open " + speech_date)
    else:
        
        if location_status == "open":
            return (location + " opens at " + time + " " + speech_date)
        
        elif location_status == "close":
            return (location + " closes at " + time + " " + speech_date)

        elif location_status == "":
            return (location + " opens at " + time_start + 
                    " and closes at " + time_end + " " + speech_date)
            
        else:
            return ("There was an error in retrieving the times for " + location)


def get_time(location, status, date, CMU_dining_dict):
    # location
    #   type: string
    #   content: location name
    #
    # status
    #   type: string
    #   content: "start"/"end"
    #
    # date
    #   type: int
    #   content: 0 is Sunday, 1 Monday, ..., 6 Saturday

    info = CMU_dining_dict[location]
    for day in info["times"]:
        if day["start"]["day"] == date:
            return (day[status]["hour"], day[status]["min"])
    else:
        # location is not open on day date
        return (None,None)


def modify_time(hour, minute)
    # hour
    #   type: int
    #   content: hour time 0-23
    #
    # minute
    #   type: int
    #   content: minute time 0-59

    if hour == None and minute == None:
        return None

    # changing military time to standard time and returning it as a string
    if hour == 0:
        (hour, time_suffix) = ("12", "am")
    elif hour < 12:
        (hour, time_suffix) = (str(hour), "am")
    elif hour == 12:
        (hour, time_suffix) = (str(hour), "pm")
    else:
        (hour, time_suffix) = (str(hour - 12), "pm")

    # prevents 8:5 instead of 8:05
    if minute < 10:
        minute = "0" + str(minute)
    else:
        minute = str(minute)

    return (hour + ":" + minute + " " + time_suffix)
