import json

import requests

json_text = '{"messages":[{"message":"This is the first message","timestamp":"2021-06-04 16:40:53"},{"message":"And ' \
            'this is a second message","timestamp":"2021-06-04 16:41:01"}]} '
string_text = json.loads(json_text)
print(string_text["messages"][1]["message"])




methods_list = ["get", "post", "put", "delete"]
parameters_methods_list = [{"method":"GET"}, {"method":"POST"}, {"method":"PUT"}, {"method":"DELETE"}]

for i in methods_list:
        for param in parameters_methods_list:
                response = requests.request(i,"https://playground.learnqa.ru/ajax/api/compare_query_type", params=param)
                if response.status_code == 200:
                        print(f"method {i} with parameter params={param} has following result {response} with status code {response.status_code}")