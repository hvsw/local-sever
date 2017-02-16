from constants import MongoConfig
from app.models.accessory import Accessory
from app.models.accessorylog import AccessoryLog
from app.models.timer import Timer
from app.models.timertask import TimerTask

import pymongo
from pymongo import MongoClient
from bson.objectid import ObjectId

class AbstractFactory(object):
	client = None
	db = None
	table = None

	def __init__(self):
		self.client = MongoClient(MongoConfig.server_address, MongoConfig.server_port)
		self.db = self.client[MongoConfig.db_name]
		

class AccessoryFactory(AbstractFactory):
	def __init__(self):
		AbstractFactory.__init__(self)
		self.table = self.db.accessories

	def insert_or_update(self, accessory):
		where = {"_id": accessory.id}

		accessory_mongo_object = accessory.mongo_json_representation()
		if self.table.find(where).count() > 0:
			accessory_mongo_object.pop("_id")
			self.table.update(where, accessory_mongo_object,True)
		else:
			self.table.insert(accessory_mongo_object)


class TimerTaskFactory(AbstractFactory):
	def __init__(self):
		AbstractFactory.__init__(self)
		self.table = self.db.tasks

	def insert(self, timer_task):
		to_save = timer_task.mongo_json_representation()
		if to_save.has_key("_id") and self.table.find({"_id": ObjectId(to_save["_id"])}).count() > 0:
			id = ObjectId(to_save["_id"])
			to_save.pop("_id")
			print self.table.update({"_id": id}, to_save, True)

			return str(id)
		else :
			to_save.pop("_id",None)
			return str(self.table.insert(to_save))

	def delete(self, task_id):
		result = self.table.delete_many({"_id": ObjectId(task_id)})
		return result.deleted_count > 0

	def get_tasks(self):
		db_tasks = self.table.find({"timer": {"$exists": True}})
		tasks = []
		for db_task in db_tasks:
			task = TimerTask(db_task)
			tasks.append(task)

		return tasks

	def get_tasks_for_api(self):
		find_object = {}
		tasks = self.table.find(find_object)

		tasks_json = []
		for task in tasks:
			task["_id"] = str(task["_id"])
			tasks_json.append(task)

		response = {
			"tasks": tasks_json
		}

		return response

class AccessoryLogFactory(AbstractFactory):
	def __init__(self):
		AbstractFactory.__init__(self)
		self.table = self.db.data_log

	def insert(self, accessory_log):
		return self.table.insert_one(accessory_log.mongo_json_representation())

	def get_logs_for_api(self, from_timestamp = 0, limit = 0):
		find_object = {"timestamp": {"$gt": float(from_timestamp)}}
		logs = self.table.find(find_object).limit(limit).sort("timestamp", 1)

		max_log_timestamp = 0.0
		logs_json = []
		for log in logs:
			log["_id"] = str(log["_id"]) 
			logs_json.append(log)
			max_log_timestamp = max(max_log_timestamp, float(log["timestamp"]))


		response = {
			"max_log_timestamp": max_log_timestamp,
			"total_results": logs.count(),
			"logs": logs_json
		}

		return response