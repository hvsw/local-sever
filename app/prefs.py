from  app.configs import MongoConfig, ArduinoAccessoryConfig, ServiceConfig, AccessoryLoggerConfig

MongoConfig.server_address = "localhost"
MongoConfig.server_port = 27017
MongoConfig.db_name = "420bits"

ArduinoAccessoryConfig.i2c_address = 0x04

ServiceConfig.loop_wait_seconds = 30

AccessoryLoggerConfig.min_interval_between_logs = 30