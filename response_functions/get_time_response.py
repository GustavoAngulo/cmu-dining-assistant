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

    if reqDate == "":
        reqDate = (date.today().weekday() + 1) % 7
        speech_date = "today."
    else:
        reqDate = reqDate.split("-")
        reqDate = (date(int(reqDate[0]), 
                        int(reqDate[1]), 
                        int(reqDate[2])).weekday() + 1) % 7
        speech_date = date_responses[reqDate]

    # reqDate: 0 is Sunday, 1 Monday, ..., 6 Saturday


    if location_status == "open":
        location_status = "start"
    else:  
        location_status = "end"
     
    
    hour, minute = get_time(location, location_status, reqDate, CMU_dining_dict)

    if hour == None and minute == None:
        return (location + " is not open " + speech_date)
    else:
        # changing military time to standard time
        if hour == 0:
            (hour, time_suffix) = (12, "am")
        elif hour < 12:
            (hour, time_suffix) = (hour, "am")
        elif hour == 12:
            (hour, time_suffix) = (hour, "pm")
        else:
            (hour, time_suffix) = (hour - 12, "pm")

        # prevents 8:5 instead of 8:05
        if minute < 10:
            minute = "0" + str(minute)
        else:
            minute = str(minute)

        if location_status == "start":
            return (location + (" opens at %d:" % (hour)) 
                        + minute 
                        + " " + time_suffix 
                        + " " + speech_date)
        else:
            return (location + (" closes at %d:" % (hour)) 
                        + minute 
                        + " " + time_suffix 
                        + " " + speech_date)





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



