#David Crawford - Payloads Demonstration - The purpose of this class is to demonstrate retrieving sensitive data from
#an external database source using payloads. We accomplish this through several steps:
#1. In this environment, we send a request to run an external data report using a lucene query id
#2. The report is run and we receive an id for the job
#3. We request the data from this job id
#4. The user is prompted to delete the requested data from its output location.

import urllib.request as urllib2
import ssl
import time
import sys
import re
import requests
from pdb import set_trace
from distutils.util import strtobool

def main():
    #Initializes the static values
    lucene_query_id = "ID"
    filename = "FILENAME.FORMAT"

    #User credentials for the web service you're using
    auth = {"USER":"USERNAME",
                  "TOKEN":"TOKEN"}

    #Sends a request to run the report based on the id
    resp = requests.get(("URL/%s/" % lucene_query_id), headers=auth).text

    #Regex on the returned XML structure to snag the job ID
    jobID = re.findall(r'<result_id>([^<]*)</result_id>', resp)[0]
    print('The Job ID is: {0}'.format(jobID))

    for x in range(600):
        #The report might not be done, so wait a little bit
        time.sleep(2)

        #Send a request for the given job
        resp = requests.get(("URL/%s/" % jobID), headers=auth).text
        print(x, resp)

        #Check if it's done by looking at the appropriate XML tag
        if "<status>COMPLETE</status>" in resp:
            try:
                #Get the result of the output in the form of a file
                data = requests.get(("URL/{0}/output/{1}".format(jobID,filename)), headers=auth).text
            except requests.HTTPError:
                #If it didn't work, we'll have to check the logs and find out why on our own
                print('The file {0}.xml could not be retrieved'.format(filename))
                break
            else:
                #Create a file and write the value of our job into it
                with open("{0}".format(filename),"w") as wf:
                    wf.write(data)
                print('File {0} created.'.format(filename))
            break

    #We may not want to keep files on the database server, so prompt to delete it
    delete_results = user_prompt_to_delete('Would you like to delete job {0}?'.format(jobID))
    if delete_results:
        print('Deleting job {0}...'.format(jobID))
        #Send a delete request to the server with the job id to remove
        resp = requests.request('DELETE', ("URL/%s" % jobID))
        print(resp.text)

def user_prompt_to_delete(question):
    sys.stdout.write('%s [y/n]: ' % question)
    while True:
        try:
            return strtobool(input().lower())
        except ValueError:
            sys.stdout.write('Please respond with \'y\' or \'n\'.\n')

main()