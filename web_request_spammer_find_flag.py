def queueRequests(target, wordlists):
    # Create a request engine with high concurrency
    engine = RequestEngine(endpoint=target.endpoint,
                           concurrentConnections=10,
                           requestsPerConnection=100,
                           pipeline=False)

    # Send the same request repeatedly
    for i in range(1000):  # Send 1000 requests
        engine.queue(target.req)  # No %s placeholder needed

def handleResponse(req, interesting):
    # Check if the response contains the flag (HTB{...})
    if 'HTB{' in req.response: # mycase its 'HTB{'
        table.add(req)  # Add the request to the results table if the flag is found wha t should be the file name for this task for python
