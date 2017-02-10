from app.factories import TimerTaskFactory
from app.task_manager import TaskManager
from app.accessory_logger import AccessoryLogger

task_manager = TaskManager()
timer_task_factory = TimerTaskFactory()
accessory_logger = AccessoryLogger()


while True:
	
	accessory_logger.log()
	task_manager.run_tasks(timer_task_factory.get_tasks())

	time.sleep(30)