import json
import requests
import os
from prettytable import PrettyTable
import sys

url = "http://10.8.215.31:8083/jwt-api-token-auth/"
headers = {
    "Content-Type": "application/json",
}

## Check -c tag with credential file ## START
if len(sys.argv) < 3 or sys.argv[1] != "-c":
    print("Invalid command-line arguments. Please provide the Credential file Path using the '-c' tag.")
    sys.exit(1)

data_file_path = sys.argv[2]

# Check if the 'data.txt' file exists
if not os.path.isfile(data_file_path):
    print("The specified 'data.txt' file does not exist.")
    sys.exit(1)

# Read the value of the 'data' variable from the text file
with open(data_file_path, 'r') as file:
    data = json.load(file)

## Check -c tag with credential file ## END

## Generating API Token ## START
response = requests.post(url, data=json.dumps(data), headers=headers)
token = response.json()["token"]

## Generating API Token ## END

## Declearing Functions

# Fetching Gatepass Details via API # START
def get_gatepass(eid,token):
    emp_api_response = requests.get(f"http://10.8.215.31:8083/personnel/api/employees/?emp_code={eid}", headers={"Authorization": f"jwt {token}", **headers}) 
    return emp_api_response

# Fetching Gatepass Details via API # END

# Printing Table # START
def print_table(api_data):
    
    
    table = PrettyTable()
    table.field_names = ["Gatepass ID", "Name", "Agency", "Agency Code", "Fingerprint", "Registerd On"]
    #Add the data rows to the table
    sorted_emp_data = sorted(api_data, key=lambda x: (x[1], x[0]))
    
    for row in sorted_emp_data:
        table.add_row(row)

    #Print the table
   

    # Iterate through each row in the table
    for row in table._rows:
    # Check if the value in the second column is "NOT FOUND"
        if "NOT FOUND" in row:
            # Get the index of the row
            row_index = table._rows.index(row)
            
            # Modify the text color of the row
            table._rows[row_index] = [f"\033[93m{cell}\033[0m" for cell in row]


    print(table)
    
# Printing Table # END

if len(os.sys.argv) == 1:
    print("No argument passed.")
    exit()
else:
      if '-i' not in os.sys.argv:
        emp_data= []
        
        user_input= os.sys.argv[3]
        
        gatepass_list = user_input.split(",")
        

        for item in gatepass_list:
            
            api_response = get_gatepass(item,token)
            if "data" in api_response.json() and len(api_response.json()["data"]) > 0:
                emp_name=api_response.json()['data'][0]['full_name']
                emp_dept=api_response.json()['data'][0]['department']['dept_name']
                dept_code=api_response.json()['data'][0]['department']['dept_code']
                emp_fingerprint=api_response.json()['data'][0]['fingerprint']
                emp_registeredOn=api_response.json()['data'][0]['hire_date']
                emp_data.append([item, emp_name, emp_dept, dept_code, emp_fingerprint, emp_registeredOn])
            else:
                emp_data.append([item, "NOT FOUND", "", "", "", ""])
        
        

        print_table(emp_data)
        
        
      else:
        i_index = os.sys.argv.index('-i')
        if len(os.sys.argv) <= i_index + 1:
            print("No input filename specified after -i tag.")
        else:
            input_filename = os.sys.argv[i_index + 1]
            print("Input filename:", input_filename)






# # Printing results in header


# if "data" in emp_api_response.json() and len(emp_api_response.json()["data"]) > 0:
#             # Extract the employee's full name
#             full_name = emp_api_response.json()["data"][0]["full_name"]
# else:
#     print("Noting Found")
#     sys.exit(1)







