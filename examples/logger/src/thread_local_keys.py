import concurrent.futures
from threading import current_thread

from aws_lambda_powertools import Logger

logger = Logger(service="payment")


def process_payments(payment_id):
    thread = current_thread
    additional_log_attributes = {"thread": thread, "payment_id": payment_id}
    logger.append_keys(**additional_log_attributes)
    logger.info("Start processing payment")
    logger.info("End processing payment")


with concurrent.futures.ThreadPoolExecutor(max_workers=5) as executor:
    futures = [executor.submit(process_payments, payment_id) for payment_id in range(10)]
    for future in concurrent.futures.as_completed(futures):
        future.result()
