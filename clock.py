from apscheduler.schedulers.blocking import BlockingScheduler
from sql import *
sched = BlockingScheduler()

@sched.scheduled_job('interval', seconds=60)
def add_new():
	add_new_reservations()
	print("Added new reservations to database")
	print ("Sleeping to avoid database conflict")
	time.sleep(60)
	print ("Sleeping to avoid database conflict")
	delete_old()
	print("Removed deleted reservations from database")

sched.start()
