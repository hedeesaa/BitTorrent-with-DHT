import json 



class JsonHandler: 

    def json_to_dic(self,data):
        decoded_data=data.decode('utf-8')
        dic_data=json.loads(decoded_data)
        return dic_data


    def dic_to_json(self,data):
        json_data=json.dumps(data)
        encoded_data=json_data.encode('utf-8')
        return encoded_data

