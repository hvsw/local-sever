from app.models.mongodbmodel import MongoDBModel

class Note(MongoDBModel):
	id = None
	text = ""
	timestamp = 0.0
	user = 0

	def __init__(self, json_object):
		if json_object.has_key("_id"):
			self.id = json_object["_id"]

		self.text = json_object["text"] if json_object.has_key("text") else None
		self.user = json_object["user"] if json_object.has_key("user") else None
		self.name = json_object["timestamp"] if json_object.has_key("timestamp") else None

	def mongo_json_representation(self):
		json_representation_object = {"text": self.text, "timestamp": self.timestamp, "user": self.user}
		if self.id is not None:
			json_representation_object["_id"] = self.id

		return json_representation_object