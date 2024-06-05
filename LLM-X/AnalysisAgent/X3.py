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