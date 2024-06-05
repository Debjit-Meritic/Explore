import requests, requests.cookies
import json
from datetime import datetime
import time

BASE_URL = "http://54.175.243.106:8338/newton/v1"
LIST_MERTIC = "/metric/list"
LOGIN = "/session/login"
GET_METRIC_BY_ID = "/metric"
GET_MODEL_BY_ID = "/datamodel"
GET_COLUMN_VALUES = "/data/getColumnValues"
GENERATE_ANALYSIS_TREE = "/analysisTree/generateTree"

class NewtonClient:
    def __init__(self):
        print("//////////////////////NEW CLIENT////////////////////////\n")
        self.base_url = BASE_URL
        self.jar = requests.cookies.RequestsCookieJar()
        self.jar.set('SESSION', 'debc396c-9a71-44f7-82d3-87ad7f60c21c')
        self.columnHeaderDict = {}
        self.metricLogicalColHeader = ""
        self.metricCache = {}
        self.modelCache = {}
        


    def login(self):
        url = self.base_url + LOGIN
        print(url)
        headers = {'Content-Type': 'application/json', 'Connection': 'keep-alive'}
        response = requests.post(url, headers = headers)
        print(response)
        return response



    def listMetric(self):
        url = self.base_url + LIST_MERTIC
        print(url)

        headers = {'Content-Type': 'application/json', 'Connection': 'keep-alive'}
        response = requests.post(url, cookies = self.jar, headers = headers, json = {})
        print(response)

        metrics = []
        if(response.status_code != 200):
            pass
        else:
            for metric in response.json()['metric_headers']:
                metrics.append({
                     'name': metric['name'],
                     'id': metric['id']
                    })
            
            # with open('metrics.txt', 'w') as file:
            #     file.write(json.dumps(metrics, indent = 4))
            #     file.close()
            
        return json.dumps(metrics, indent = 4)   



    def getMetricByID(self, id):
        present = False
        response_json = {}
        if id in self.metricCache:
            response_json = self.metricCache[id]
            if (time.time() - response_json["last_updated"])/60 < 15:
                present = True
                print("<Response retrieved from cache>")

        if not present:
            url = self.base_url + GET_METRIC_BY_ID + "/" + id + "?includeEdges=true"
            print(url)

            headers = {'Content-Type': 'application/json', 'Connection': 'keep-alive'}
            response = requests.get(url, cookies = self.jar, headers = headers)
            print(response)

            metric_info = {}
            if(response.status_code != 200):
                return json.dumps({})
            else:
                response_json = response.json()
                response_json["last_updated"] = time.time()
                self.metricCache[id] = response_json

        
        
        self.metricLogicalColHeader = response_json["header"]
        # print(self.metricLogicalColHeader)

        name = response_json["header"]["name"]
        owner_id = response_json["header"]["owner_id"]
        rel_attrs = []
        for attr in response_json["edges"]:
            if attr["edge_type"] == "ATTRIBUTE_EDGE":
                rel_attrs.append({
                    "name": attr["related_attribute"]["name"],
                    "id": attr["related_attribute"]["id"],
                    "type": "ATTRIBUTE"
                    })

        metric_info = {
            "name": name,
            "owner_id": owner_id,
            "related_attributes": rel_attrs
        }

            # with open('metricinfo.txt', 'w') as file:
            #     file.write(json.dumps(response.json(), indent = 4))
        
        return json.dumps(metric_info, indent = 4)
    


    def getModelByID(self, id):
        present = False
        response_json = {}
        if id in self.modelCache:
            response_json = self.modelCache[id]
            if (time.time() - response_json["last_updated"])/60 < 15:
                present = True
                print("<Response retrieved from cache>")

        if not present:
            url = self.base_url + GET_MODEL_BY_ID + "/" + id
            print(url)

            headers = {'Content-Type': 'application/json', 'Connection': 'keep-alive'}
            response = requests.get(url, cookies = self.jar, headers = headers)
            print(response)

            if(response.status_code != 200):
                return json.dumps({})
            else:
                response_json = response.json()
                response_json["last_updated"] = time.time()
                self.modelCache[id] = response_json
        
        temporal_cols = []
        columnHeaderDict = {}
        
        for col in response_json["columns"]:
            columnHeaderDict[col["header"]["name"]] = col["header"]

            if col["column_type"] == "TEMPORAL":
                name = col["header"]["name"]
                col_id = col["header"]["id"]
                temporal_cols.append({
                    "name": name,
                    "id": col_id,
                    "type": "TEMPORAL"
                })

        self.columnHeaderDict = columnHeaderDict
        # print(json.dumps(self.columnHeaderDict, indent = 4))

        # with open('modelinfo.txt', 'w') as file:
        #     file.write(json.dumps(response.json(), indent = 4))        
        
        return json.dumps(temporal_cols, indent = 4)



    def getColumnValues(self, id, type):
        present = False
        cached_response = {}
        if id in self.columnInfoCache:
            cached_response = self.columnInfoCache[id]
            if (time.time() - response_json["last_updated"])/60 < 15:
                present = True
                print("<Response retrieved from cache>")
                 
                

        if not present:
            url = self.base_url + GET_COLUMN_VALUES + "?logicalColumnId=" + id
            print(url)

            headers = {'Content-Type': 'application/json', 'Connection': 'keep-alive'}
            response = requests.get(url, cookies = self.jar, headers = headers, json = {})
            print(response)

            if(response.status_code != 200):
                return json.dumps({})
            else:
                response_json = response.json()
            # with open('columninfo.txt', 'w') as file:
            #     file.write(json.dumps(response.json(), indent = 4))
        
            # print(response.json())
            if type == "TEMPORAL":
                dateList = []
                for x in response_json:
                    dt_object = datetime.fromtimestamp(x)
                    month = dt_object.strftime('%m')
                    year = dt_object.strftime('%Y')
                    date = [int(month), int(year)]
                    dateList.append(date)
                cached_response = {
                    "values": dateList,
                    "last_updated": time.time()
                }
                
            else:
                cached_response = {
                    "values": response_json,
                    "last_updated": time.time()
                }
                
            self.columnInfoCache[id] = cached_response

        return json.dumps(cached_response["values"])



    def getMetricLogicalColHeader(self):
        return self.metricLogicalColHeader



    def getColumnInfoByName(self, name):
        return self.columnHeaderDict[name]



    def generateAnalysisTree(self, body):
        url = self.base_url + GENERATE_ANALYSIS_TREE
        print(url)

        headers = {'Content-Type': 'application/json', 'Connection': 'keep-alive'}
        response = requests.post(url, cookies = self.jar, headers = headers, json = body)
        print(response)

        if(response.status_code != 200):
            return response
        else:
            with open('analysistree.txt', 'w') as file:
                file.write(json.dumps(response.json(), indent = 4))

            return response
   

if __name__ == "__main__":
    client = NewtonClient()
    # response = client.listMetric()
    # response = client.getMetricByID("9bfeeee0-3404-4af6-9352-fa98f4a231cc")
    # response = client.getModelByID("31a0fcda-dff1-437f-8f6a-986f8a14de59")
    response = client.getColumnValues("34095e55-b9b0-4268-ac73-36f6ef15092a", "ATTRIBUTE") 
    # if(response.status_code == 200):
    #     # print(json.dumps(response.json(), indent = 4))
    #     print(response)
    # else:
    #     print("Failure - " + str(response.status_code))
    # print(response)
    # print(client.metricCache)

    