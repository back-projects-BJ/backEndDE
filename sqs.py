
import boto3

aws_access_key_id = 'AKIAYEIE6WITLXIU6YWL'
aws_secret_access_key = '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'

sqs = boto3.client(
    'sqs',
    region_name='us-east-2',
    aws_access_key_id=aws_access_key_id,
    aws_secret_access_key=aws_secret_access_key
)
queue_url = 'https://sqs.us-east-2.amazonaws.com/558893019686/LaMasVeloz'
# Lista para guardar los mensajes procesados

processed_messages = []
def process_messages():
    while True:
        response = sqs.receive_message(
            QueueUrl=queue_url,
            AttributeNames=['All'],
            MessageAttributeNames=['All'],
            MaxNumberOfMessages=10,
            VisibilityTimeout=30,
            WaitTimeSeconds=20
        )

        if 'Messages' in response:
            receipt_handles = [message['ReceiptHandle'] for message in response['Messages']]
            # Solo llamar a delete_message_batch si hay al menos un mensaje
            if receipt_handles:
                sqs.delete_message_batch(
                    QueueUrl=queue_url,
                    Entries=[{'Id': str(i), 'ReceiptHandle': receipt_handle} for i, receipt_handle in enumerate(receipt_handles)]
                )
            for message in response['Messages']:
                processed_message = f"Mensaje Procesado: {message['Body']}"
                # print(processed_message)
                # Agregar el mensaje procesado a la lista
                processed_messages.append(processed_message)