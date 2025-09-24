import os
from celery import Celery
from celery.signals import worker_process_init

redis_url = os.getenv("REDIS_URL", "redis://localhost:6379")

celery_app = Celery("affpilot")

@worker_process_init.connect
def init_worker(**kwargs):
    """Initialize worker process to avoid thread-local issues."""
    from celery.app.trace import reset_worker_optimizations
    reset_worker_optimizations()

celery_app.conf.update(
    broker_url=redis_url,
    result_backend=redis_url,
    task_serializer='json',
    accept_content=['json'],
    result_serializer='json',
    timezone='UTC',
    enable_utc=True,
    include=[
        'app.tasks.ai_info_article',
        'app.tasks.ai_review_article',
    ],
    worker_prefetch_multiplier=1,
)