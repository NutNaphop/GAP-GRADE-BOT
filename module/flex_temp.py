import json

with open('./flex.json', encoding='utf8') as f , open('./data.json', encoding='utf8') as f2 , open('./updated_flex.json', encoding='utf8') as f3:
    data = json.load(f)
    data_sub = json.load(f2)
    test = json.load(f3)
    
# Edit Semester And Year
print(test['messages'][0])
# data['messages'][0]['contents']['contents'][0]['body']['contents'][1]['text'] = data_sub
form = {
    "type": "bubble",
    "size": "giga",
    "body": {
      "type": "box",
      "layout": "vertical",
      "contents": [
        {
          "type": "text",
          "text": "My GPA",
          "size": "xl",
          "weight": "bold"
        },
        {
          "type": "text",
          "text": "Year ... Term ..."
        },
        {
          "type": "separator",
          "margin": "md",
          "color": "#000000"
        },
        {
          "type": "box",
          "layout": "horizontal",
          "contents": [
            {
              "type": "text",
              "text": "Subject",
              "align": "start",
              "weight": "bold"
            },
            {
              "type": "text",
              "text": "Credit",
              "align": "center",
              "weight": "bold"
            },
            {
              "type": "text",
              "text": "Grade",
              "align": "end",
              "weight": "bold"
            }
          ]
        },
        {
          "type": "box",
          "layout": "horizontal",
          "contents": [
          ]
        }
      ]
    }
  }

data['messages'][0]['contents']['contents'].append(form)

print(data['messages'][0]['contents']['contents'])


# # Subject Grade Credit -> need to copy one by one
# # Subject
# print(data['messages'][0]['contents']['contents'][0]['body']['contents'][3]['contents'][0]['text'])
# # Credit
# print(data['messages'][0]['contents']['contents'][0]['body']['contents'][3]['contents'][1]['text'])
# # Grade
# print(data['messages'][0]['contents']['contents'][0]['body']['contents'][3]['contents'][2]['text'])

# Copy and append from Contents[3] to Contents[4]
# for key in data :
#     data['messages'][0]['contents']['contents'][0]['body']['contents'][1]['text'] = key
#     for cate in data_sub[key] : 
#         print(cate['SName'] , cate['Credit'] , cate['Grade'])
#         subject = cate['SName']
#         credit = cate['Credit']
#         grade = cate['Grade']
#         format = [{ 
#         'type': 'text', 'text': subject, 'align': 'start', 'size':'xs'}, 
#         {'type': 'text', 'text': credit, 'align': 'center','size':'xs'}, 
#         {'type': 'text', 'text': grade, 'align': 'end', 'size':'xs'}]
#         data['messages'][0]['contents']['contents'][0]['body']['contents'].append({"type": "box","layout": "horizontal" ,"contents": format})
    

# Output the updated JSON
# print(json.dumps(data, indent=4, ensure_ascii=False))

# Save the updated JSON back to file if needed
with open('./updated_flex2.json', 'w', encoding='utf8') as f:
    json.dump(data, f, indent=4, ensure_ascii=False)

f.close() 
f2.close() 
f3.close()