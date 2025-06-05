#!/usr/bin/env python3
from boto3 import client
import logging
from colorama import Fore, Style, init

init(autoreset=True)

class ColorFormatter(logging.Formatter):
    COLORS = {
        logging.DEBUG: Fore.CYAN,
        logging.INFO: Fore.GREEN,
        logging.WARNING: Fore.YELLOW,
        logging.ERROR: Fore.RED,
        logging.CRITICAL: Fore.MAGENTA,
    }

    def format(self, record):
        color = self.COLORS.get(record.levelno, "")
        message = super().format(record)
        return f"{color}{message}{Style.RESET_ALL}"

handler = logging.StreamHandler()
handler.setFormatter(ColorFormatter('%(levelname)s: %(message)s'))
logging.basicConfig(level=logging.INFO, handlers=[handler])
 

def list_dynamo_tables():
    dynamodb = client('dynamodb')
    response = dynamodb.list_tables()
    if 'TableNames' not in response:
        logging.warning("No DynamoDB tables found.")
        return []
    logging.info("List of DynamoDB tables: %s", response['TableNames'])
    return response['TableNames']

def list_dummy_data(table_name: str):
    dynamodb = client('dynamodb')
    try:
        response = dynamodb.scan(TableName=table_name)
        items = response.get('Items', [])
        if not items:
            logging.info("No items found in table: %s", table_name)
        else:
            logging.info("Items in table %s: %s", table_name, items)
    except Exception as e:
        logging.error("Failed to list data from table %s: %s", table_name, e)
        raise

def insert_dummy_data(table_name: str) -> None:
    dynamodb = client('dynamodb')
    try: 
        for i in range(1, 10):
            item = {
                'id': {'S': f'item-{i}'},
                'timestamp': {'S': '2023-10-01T00:00:00Z'},
                'value': {'N': str(i)}
            }
            dynamodb.put_item(TableName=table_name, Item=item)
        logging.info("Dummy data inserted into table: %s", table_name)
        list_dummy_data(table_name)
    except Exception as e:
        logging.error("Failed to insert dummy data into table %s: %s", table_name, e)
        raise



def main():
    try: 
        print("Welcome to the DynamoDB Table Lister!")
        logging.info("Starting to list DynamoDB tables...")
        tables = list_dynamo_tables()
        if tables:
            logging.info("DynamoDB Tables: %s", tables)
        else:
            logging.info("No DynamoDB tables available.")
    except Exception as e:
        logging.error("An error occurred while listing DynamoDB tables: %s", e)
        exit(1)

    for i in range(len(tables)):
        table_name = tables[i]
        if table_name.startswith("DynamoDBStack-MyTable794EDED1"):
            logging.info("Inserting dummy data into table: %s", table_name)
            try:
                insert_dummy_data(table_name)
            except Exception as e:
                logging.error("An error occurred while inserting dummy data into table %s: %s", table_name, e)
                exit(1)
            finally:
                logging.info("Dummy data insertion completed for table: %s", table_name)
        else:
            logging.info("Skipping table: %s", table_name)
            continue


if __name__ == "__main__":
    main()