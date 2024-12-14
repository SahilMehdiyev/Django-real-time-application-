from celery import shared_task
from celery.schedules import crontab
from celery import Celery

app = Celery('crypto_proj')

@shared_task
def create_test_object(name):
    from positions.models import Test  
    Test.objects.create(name=name)

@app.on_after_configure.connect
def setup_periodic_tasks(sender, **kwargs):
    sender.add_periodic_task(
        crontab(minute="*/1"),  
        run_create_objs.s(),
        name="Create test objects every minute"
    )

@shared_task
def run_create_objs():
    create_test_object.delay(name="new2024")
