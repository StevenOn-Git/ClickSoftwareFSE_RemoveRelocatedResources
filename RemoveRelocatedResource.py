from AllThingsClick import (prodObjectCheck, GetClickObjectsBatch, parse_task_key_in_exception_message,
                            UpdateClickObject)
import requests
'''
.Description
Delete Relocated Resource

.Version
Original Release - Steve On - 20230726
Added mechanism to parse exception message dynamically using two string patterns - Steve On - 20240201

'''


def remove_req_engineers_payload(task_key):
    """Returns a payload to remove the task key constraint."""
  
    return {
        "@objectType": "Task",
        "@createOrUpdate": True,
        "Key": task_key,
        "RequiredEngineers": []
    }


def parse_task_key_in_exception_message(exception_message, first_string_pattern, second_string_pattern):
    """Divide the exception message by the first string pattern and then use the second string pattern to return
    the click task key. Time: O(n) | Space O(n) where n is the string character in each match."""
  
    string_patterns = [first_string_pattern, second_string_pattern]
    first_sp_match_exception_message = exception_message[exception_message.index(string_patterns[0]):]
    second_sp_match = first_sp_match_exception_message[len(string_patterns[1]) +
                                                       first_sp_match_exception_message.index(string_patterns[1]):]
    matches = [num for num in second_sp_match if num != ')']

    return int("".join(matches))


def delete_click_object(obj_name, key, click_url, username, password):
    """Recursively, attempt to delete the relocated resource. The base case occurs when the API hits status code 204
    to show that the object is successfully deleted. Time: O(n) | Space O(n) but you need to consider the network
    traffic. It'll be much more efficient if we take the exception message and interrogate filtered Task collections
    by the required engineer key and remove all those keys first before retrying this function."""
  
    url = click_url + obj_name + '/' + str(key)
    try:
        from requests.auth import HTTPBasicAuth
        headers = {'Content-type': 'application/json', 'Accept': 'text/plain'}
        r = requests.delete(url=url, headers=headers, auth=(username, password))
        if r.status_code == 204:
            return
        elif r.status_code == 500:
            err = r.json()
            for error in err['InnerErrors']:
                print(error['ExceptionMessage'])
                task_key = parse_task_key_in_exception_message(
                    error['ExceptionMessage'], "RequiredEngineers", "(key=")
                UpdateClickObject(remove_req_engineers_payload(task_key), click_url + "Task", username, password)
                delete_click_object(obj_name, key, click_url, username, password)

    except Exception as e:
        print(e)

# How to call this function
# delete_click_object(obj_name="Engineer", key=1234567, url="https://int-host-name-of-POD/so/api/objects/", username="admin@[clickTenant]", password="pwd")
