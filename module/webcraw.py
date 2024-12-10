from bs4 import BeautifulSoup
from urllib.request import urlopen
import requests as req
import mechanize
import http.cookiejar
import re
import json

def login(userName , passWord) :
  url = "https://regis.src.ku.ac.th/res/"
  html = urlopen(url)
  soup = BeautifulSoup(html , 'html.parser')

  # Login Into Nisit Menu.php
  cj = http.cookiejar.CookieJar()
  br = mechanize.Browser()
  br.set_cookiejar(cj)

  try:
      br.open("https://regis.src.ku.ac.th/res/")
  except Exception as e:
      print(e)
      return -1

  #Login
  br.select_form(nr=0)  # Select first form in page
  username_field = br.form.find_control(id="login-username")
  username_field.value = userName
  password_field = br.form.find_control(id="login-password")
  password_field.value = passWord

  br.submit() # Submit form

  redirect_url = "https://regis.src.ku.ac.th/res/menu_nisit.php"
  br.open(redirect_url)
  html_content = br.response().read()

  #Get Element
  try : 
    soup = BeautifulSoup(html_content, 'html.parser')
    content = soup.find("div", {"id": "collapse05"})
    tr_elements = content.find_all("tr")
  except : 
    return -1 

  # Scraping data from table rows
  data_list = []
  current_term = ""
  temp_current_term = ""
  term = ""

  # Get td element tag and clean
  for tr in tr_elements:
    try : 
      td_elements = tr.find_all('td')
      text_contents = [element.get_text(strip=True) for element in td_elements]
      data_list.append(text_contents)
    except : 
      return - 1
  # print(data_list)

  # # JSON Maker
  # print(data_list)
  json_data = {}


  for row in range(1, len(data_list)):
      if (data_list[row][0] not in json_data and data_list[row][0].startswith("ภาค")):
          term = data_list[row][0]
          term = term.split(" ")

          temp_current_term = ""
          if (term[0].endswith("ต้น")) :
            temp_current_term += "First"
          if (term[0].endswith("ปลาย")) :
            temp_current_term += "Second"

          temp_current_term += term[-1]
          current_term = temp_current_term
          
          # Initialize both the list and the Overall section for the term
          json_data[current_term] = {"courses": [], "Overall": {}}
      
      elif "หน่วยกิต/gpa เทอมนี้" in data_list[row][0] and current_term:
          gpa_values = re.findall(r'\d+\.?\d*', data_list[row][0])
          print(gpa_values)
          # Add gpa_values to Overall section
          json_data[current_term]["Overall"]["Credit"] = gpa_values[0]
          json_data[current_term]["Overall"]["TotalCredit"] = gpa_values[2]
          if len(gpa_values) == 3:
              json_data[current_term]["Overall"]["GPA"] = "In Progress"
              json_data[current_term]["Overall"]["TotalGPA"] = gpa_values[2]
          else:
              json_data[current_term]["Overall"]["GPA"] = gpa_values[1]
              json_data[current_term]["Overall"]["TotalGPA"] = gpa_values[3]
      
      elif current_term and len(data_list[row]) >= 6:
          # Create a new course object
          obj = {
              "id": data_list[row][0],
              "Type": data_list[row][1],
              "SName": data_list[row][2],
              "Credit": data_list[row][3],
              "Grade": data_list[row][4],
              "Weight": data_list[row][5]
          }
          # Append the course object to the list for the current term
          json_data[current_term]["courses"].append(obj)

  try :
    with open('Mo.json', 'w') as f:
        json.dump(json_data, f)
  except :
    print("Can not Write A file")
    
  return json_data

# login('b6530250476' , 'Owen_xz1735')