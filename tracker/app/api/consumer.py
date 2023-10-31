import asyncio
import aio_pika
import ast
import requests

# works with this jenkins plugin: https://github.com/jenkinsci/mq-notifier-plugin
# Entering queue:
# "state": "QUEUED",
# "url": "http://urltojenkins:port/jenkins/job/myjob/",
# "parameters": [
#     "parameter1":"parametervalue",
#     "parameter2":"otherparametervalue"
# ]

# Leaving queue:
# "state": "DEQUEUED",
# "DEQUEUE_REASON": "BUILDING",
# "url": "http://urltojenkins:port/jenkins/job/myjob/",
# "parameters": {
#     "parameter1": "parametervalue",
#     "parameter2": "otherparametervalue"
# }

# Build started:
# "state": "STARTED",
# "url": "http://urltojenkins:port/jenkins/job/myjob/buildnumber/",
# "causes": {
#     "UserIdCause",
#     "Started by user Bunny McQueen"
# },
# "parameters": {
#     "parameter1": "parametervalue",
#     "parameter2": "otherparametervalue"
# }

# Build finished:
# "state": "COMPLETED",
# "url": "http://urltojenkins:port/jenkins/job/myjob/buildnumber/",
# "status": "SUCCESS",
# "parameters": {
#     "parameter1": "parametervalue",
#     "parameter2": "otherparametervalue"
# }

# if need more build data use this url to get it from jenkins
# https://urltojenkins/job/somejob/somebuildnumber/api/python?pretty=true&token=sometoken

async def on_message(message: aio_pika.IncomingMessage):
    tracker = ast.literal_eval(message.body.decode("utf-8"))

    state = tracker.get('state', None)
    url = tracker.get('url', None)
    parameters = dict(tracker.get('parameters', {}))
    causes = tracker.get('causes', 'NA')
    status = tracker.get('status', 'NA')

    for param in parameters.keys():
        print(f"key: {param}, value: {parameters[param]}")

    url_list = url.split('/')
    job_name = url_list[-3]
    build_number = int(url_list[-2])

    # payload = dict(
    #     job_name=job_name,
    #     build_number=build_number,
    #     state=state,
    #     url=url,
    #     parameters=str(parameters),
    #     causes=causes,
    #     status=status
    # )
    payload = {
        "job_name":job_name,
        "build_number": build_number,
        "state": state,
        "url": url,
        "parameters": str(parameters),
        "causes": causes,
        "status": status
    }

    print(payload)

    if state in ['QUEUED', 'DEQUEUED']:
        print(f"Ignoring state: {state}")
    elif state == 'STARTED':
        print(f"State: STARTED")
        # await crud.post(payload)
        r = requests.post(url='http://api:8000/builds/', json=payload,
                          headers={"Content-Type": "application/json"})
        print(r.text)
    elif state == 'COMPLETED':
        print(f"State: COMPLETED")
        # build = await crud.get_by_build_number(build_number)
         # await crud.put(dict(build).get('id'), payload)
    else:
        print(f"wrong state: {state}")
