#splits entire string and returns list
def split_times(times_str):
    comma_index = times_str.find(',')
    list_output= []
    while(comma_index != -1):
        day_time = times_str[0:comma_index]
        list_output.append(split_day_time(day_time))
        times_str = times_str[comma_index+1:len(times_str)]
        comma_index = times_str.find(',')       
    list_output.append(split_day_time(times_str))
    return list_output
#splits just one day and it's hours
def split_day_time(day_time_str):
    day = day_time_str[0:day_time_str.find('=')]
    day_time_str = day_time_str[day_time_str.find('='):len(day_time_str)]
   
    opening , closing = split_hours(day_time_str)
    list_out = [day,opening,closing]
    return list_out
#splits the hours
def split_hours(hours_str):
    hours_str = hours_str[1:len(hours_str)]
    comma = hours_str.find("-")
    opening = hours_str[0:comma]
    closing = hours_str[comma+1:len(hours_str)]
    return(opening,closing)



#these are formats for each function
# times_str = "Monday=17:30-21:30, Wednesday=17:30-21:30, Thursday=17:0-21:0, Friday=17:0-22:0, Saturday=17:0-22:0, Sunday=17:0-21:0"
# day_time_str ="\"Monday\":\"17:30-21:30\""
# hours_str = "\"17:30-21:30\""
#
# x = split_times(times_str)
# print(x)
