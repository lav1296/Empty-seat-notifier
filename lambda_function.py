import json
from bs4 import BeautifulSoup
import boto3
import requests

def lambda_handler(event, context):
    newHeaders = {'Connection':'keep-alive',
    'sec-ch-ua':'" Not A;Brand";v="99", "Chromium";v="99", "Google Chrome";v="99"',
    'sec-ch-ua-mobile':'?0',
    'User-Agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/99.0.4844.83 Safari/537.36',
    'Content-Type':'application/x-www-form-urlencoded; charset=UTF-8',
    'Accept':'text/html, /; q=0.01',}

    string = "{'Cloud':'30635', 'UI/UX':'31281','TI':'31343'}"
    term="202330"
    Dict = eval(string)
    client=boto3.client('sns')
    for subs in Dict:
        data="term="+term+"&courseReferenceNumber="+Dict[subs]
        response = requests.post('x',
                            data=data,
                            headers=newHeaders)
        print(response.text)
        soup = BeautifulSoup(response.text, "html.parser")

        actualSeats = soup.find('span', class_='status-bold', text='Enrolment Seats Available:')
        WaitlistSeats=soup.find('span', class_='status-bold', text='Waitlist Seats Available:')
        actualSeat =int(actualSeats.next_sibling.next_sibling.text.strip())
        waitlistSeat=int(WaitlistSeats.next_sibling.next_sibling.text.strip())
        print ("available",actualSeat)
        print ("waitlistSeat",waitlistSeat)
        
        if actualSeat>0:
            print ("available",actualSeat)
            response = client.publish(
            TopicArn='',
            Message=subs+"is Avaliable "+str(actualSeat),
            Subject='URGENT Subject Available'
            )
        if waitlistSeat>0:
            print ("waitlistSeat",waitlistSeat)
            response = client.publish(
            TopicArn='',
            Message=subs+" is Avaliable "+str(actualSeat),
            Subject='URGENT Subject Available',
            MessageStructure='string',
            MessageAttributes={
            'string': {
                'DataType': 'string',
                'StringValue': 'string',
                'BinaryValue': b'bytes'
            }
            },
            )
    return {
        'statusCode': 200,
        'body': json.dumps('Hello from Lambda!')
    }