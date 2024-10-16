from datetime import datetime
from model import init

def sla_of_ticketlist(data):
    coll_priority = init.database()['static_data']['priority']
    for i in data:
        get_priority = coll_priority.find_one({'priority':i['priority']})
        
        if get_priority:
            
            #open_at = datetime.strptime(i['open_at'],"%Y-%m-%d %H:%M:%S.%f")
            
            last_unixtime =  datetime.fromtimestamp(i['last_unixtime'])
            open_at = datetime.strptime(i['open_at'].split('.')[0],"%Y-%m-%d %H:%M:%S")
            
            time_difference = last_unixtime - open_at
            total_seconds = int(time_difference.total_seconds())
            
            if total_seconds > 0:
                calculate_sla = get_priority['sla'] - total_seconds
                i['sla_remain_percent'] = round(calculate_sla * 100 / get_priority['sla'],2)
  
                i['total_activity_time'] = total_activity_time(total_seconds)
                
                if calculate_sla < 120:
                    i['sla_of_ticket'] = "Warning"
                    if calculate_sla < 0:
                        i['sla_of_ticket'] = "Over Due"
                
                elif calculate_sla >= 120:
                    i['sla_of_ticket'] = "On Time"   
            else:
                i['sla_remain_percent'] = ""
                i['total_activity_time'] = ""
                i['sla_of_ticket'] = ""
        else:
            i['sla_remain_percent'] = ""
            i['total_activity_time'] = ""
            i['sla_of_ticket'] = ""
    
    return data
    
    
def sla_of_detail_ticket(data):
    coll_priority = init.database()['static_data']['priority']
    get_priority = coll_priority.find_one({'priority':data['priority']})

    result = {}
    if get_priority:
        last_unixtime =  datetime.fromtimestamp(data['last_unixtime'])
        open_at = datetime.strptime(data['open_at'].split('.')[0],"%Y-%m-%d %H:%M:%S")
        
        time_difference = last_unixtime - open_at
        total_seconds = int(time_difference.total_seconds())
        

        if total_seconds > 0:
            calculate_sla = get_priority['sla'] - total_seconds

            result['sla_remain_percent'] = round(calculate_sla * 100 / get_priority['sla'],2)

            result['total_activity_time'] = total_activity_time(total_seconds)
            
            if calculate_sla < 120:
                result['sla_of_ticket'] = "Warning"
                if calculate_sla < 0:
                    result['sla_of_ticket'] = "Over Due"
            
            elif calculate_sla >= 120:
                result['sla_of_ticket'] = "On Time"
    
            
        else:
            result['sla_remain_percent'] = ""
            result['total_activity_time'] = ""
            result['sla_of_ticket'] = ""
        return result
    else:
        result['sla_remain_percent'] = ""
        result['total_activity_time'] = ""
        result['sla_of_ticket'] = ""
        return result
    
def total_activity_time(total_seconds):
    try:
    
        if total_seconds > 0:
            # แปลงเป็นชั่วโมง นาที และวินาที
            hours = total_seconds // 3600
            minutes = (total_seconds % 3600) // 60
            seconds = total_seconds % 60

            if len(str(hours))== 1:
                hours = f'0'+str(hours)
            if len(str(minutes))== 1:
                minutes = f'0'+str(minutes)
            if len(str(seconds))== 1:
                seconds = f'0'+str(seconds)

            remain_time = f'{hours}:{minutes}:{seconds}'
            return remain_time
        else:
            return "00:00:00"
    except:
        return "00:00:00"