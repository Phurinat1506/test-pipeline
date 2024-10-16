# import time
# from bson import ObjectId
# from flask import jsonify, request, Blueprint
# from model import init
# import yaml
# import copy
# from datetime import datetime, timedelta,timezone

# from module.share import sla
# try:
#     from yaml import CLoader as Loader, CDumper as Dumper
# except ImportError:
#     from yaml import Loader, Dumper

# CONFIG_FILE = './config.yaml'

# try:
#     file_stream = open(CONFIG_FILE, "r", encoding='utf-8')
#     # Load configuration into config
#     Config = yaml.load(file_stream, Loader=Loader)
#     file_stream.close()
# except Exception as e:
#     print("Read configuration file error:", e)
#     exit(1)

# open_ticket_bp_v1 = Blueprint('open_ticket_bp_v1', __name__,)
# @open_ticket_bp_v1.route('/api/v1/ticket/opened/list' , methods=['GET'])
# def ticketlist():
#     try:
        
#         coll_ticket = init.database()['ticket_center']["ticket"]
#         def search_with_pagination(query_params, page, page_size):
#             total = coll_ticket.count_documents({'status':"opened"})
#             pipeline = []
            
#             # Default match stage (if query params provided)
#             match_stage = {}
#             match_stage['status'] = "opened"
#             # Search query if any (can modify based on your search logic)
            
#             if query_params.get('search') is not None:
                
#                 all_search_fields = ["ticket_no","type","status", "cno", "customer", "subject", "group", "service","priority", "last_unixtime"]
#                 list_field = [{"{}".format(field): {"$regex":  query_params.get('search'), "$options": "i"}} for field in all_search_fields]
#                 match_stage["$or"] = list_field
#             # # Date filtering (only apply if both dates are provided)
#             if query_params.get('start_date') is not None and query_params.get('end_date') is not None:
                
#                 start_date = time.mktime(datetime.strptime(query_params['start_date'], "%Y-%m-%d").timetuple())
#                 end_date = time.mktime(datetime.strptime(query_params['end_date'], "%Y-%m-%d").timetuple())
#                 match_stage['unixtime'] = {
#                     '$gte': float(start_date),
#                     '$lte':  float(end_date)
#                 }
#             elif query_params.get('start_date') is not None:
                
#                 start_date = time.mktime(datetime.strptime(query_params['start_date'], "%Y-%m-%d").timetuple())
#                 match_stage['unixtime'] = {
#                      '$gte': float(start_date)
#                 }
#             elif query_params.get('end_date') is not None:
                
#                 end_date = time.mktime(datetime.strptime(query_params['end_date'], "%Y-%m-%d").timetuple())
#                 match_stage['unixtime'] = {
#                     '$lte':  float(end_date)
#                 }
            
#             # Add the match stage if it's not empty
            
#             if match_stage:
#                 pipeline.append({'$match': match_stage})
#             count = len(list(coll_ticket.aggregate(pipeline)))
            
#             # Pagination stages
#             pipeline.append({'$skip': (page - 1) * page_size})  # Skip for pagination
#             pipeline.append({'$limit': page_size})  # Limit for pagination
            
#             # Execute aggregation pipeline
#             result = list(coll_ticket.aggregate(pipeline))
            
#             return total,count,result

        
#         # Example usage
#         get_params = request.args
#         query_params = {
#             'search' : get_params.get("search", None),
#             'start_date' : get_params.get("start_date", None),
#             'end_date' : get_params.get("end_date", None)
#         }
        
#         page = get_params.get("page", 1)
#         limit = get_params.get("limit", 20)
        
#         if type(page) == str or type(limit) == str:
#             if len(page) == 0 or len(limit) == 0:
#                 page = 1
#                 limit = 20

#         try:
#             total,count,result = search_with_pagination(query_params, page=int(page), page_size=int(limit))

#         except Exception as e:
#             message = {
#                 'message_status': 400,
#                 'message': 'Bad request datetime invalid format'
#             }
#             resp = jsonify(message)
#             resp.status_code = 400
            
#             return resp
        
#         result = sla.sla_of_ticketlist(result)
        
#         for r in result:
#             r['assigned_to'] = r['group']
#             r['notify_time'] = r['open_at']
#             r["id"] = str(r["_id"])
#             del(r["_id"])

        
#         message = {
#             'message_status': 200,
#             'message': 'Get opened ticketlist success',
#             'count':count,
#             'total':total,
#             'result': result,
            
#         }
#         resp = jsonify(message)
#         resp.status_code = 200
        
#         return resp
#     except Exception as e:
#         print(e,flush=True)
#         message = {
#             'message_status': 500,
#             'message': 'SERVER ERROR',
#             "error": str(e) 
#         }
#         resp = jsonify(message)
#         resp.status_code = 500
        
#         return resp

# @open_ticket_bp_v1.route('/api/v1/ticket/opened/detail/<string:id>' , methods=['GET'])
# def detail(id):
#     try:
#         coll_ticket = init.database()['ticket_center']["ticket"]
#         def is_valid_objectid(oid):
#             try:
#                 return ObjectId(oid)
#             except:
#                 return False
            
#         if is_valid_objectid(id):
#             id = is_valid_objectid(id)
#             result = coll_ticket.find_one({'_id':id,'status':'opened'})
            
            
#             if result is not None:
#                 result['assigned_to'] = result['group']
#                 sla_result = sla.sla_of_detail_ticket(result) 
#                 result['total_activity_time'] = sla_result['total_activity_time']
#                 result['sla_remain_percent'] = sla_result['sla_remain_percent']
#                 result['sla_of_ticket'] = sla_result['sla_of_ticket']
#                 result['notify_time'] = result['open_at']

#                 result["id"] = str(result["_id"])
#                 del(result["_id"])

#                 message = {
#                     'message_status': 200,
#                     'message': 'Get detail opened ticket success',
#                     'result': result
#                 }
#                 resp = jsonify(message)
#                 resp.status_code = 200
                
#                 return resp
                
#             else:
#                 message = {
#                     'message_status': 400,
#                     'message': 'Bad request'
#                 }
#                 resp = jsonify(message)
#                 resp.status_code = 400
                
#                 return resp
#         else:
#             message = {
#                 'message_status': 400,
#                 'message': 'Bad request'
#             }
#             resp = jsonify(message)
#             resp.status_code = 400
            
#             return resp
        
#     except Exception as e:
#         print(e,flush=True)
#         message = {
#             'message_status': 500,
#             'message': 'SERVER ERROR',
#             "error": str(e) 
#         }
#         resp = jsonify(message)
#         resp.status_code = 500
        
#         return resp

