import concurrent.futures
from contextvars import ContextVar
from threading import current_thread

from aws_lambda_powertools import Logger

logger = Logger(service="payment")
context_id = ContextVar("context_id")


def process_payments(payment_id):
    thread = current_thread().ident
    context_id.set(payment_id)
    print(f"thread: {thread}, context: {str(context_id.get())}, payment_id: {str(payment_id)}")
    additional_log_attributes = {"thread": "%(thread)s", "payment_id": payment_id, "context_id": context_id.get()}
    logger.append_keys(**additional_log_attributes)
    logger.info("Start processing payment")
    logger.info("End processing payment")


with concurrent.futures.ThreadPoolExecutor(max_workers=5) as executor:
    futures = [executor.submit(process_payments, payment_id) for payment_id in range(10)]
    for future in concurrent.futures.as_completed(futures):
        future.result()
