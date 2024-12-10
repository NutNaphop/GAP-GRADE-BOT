import json
import copy


def sendMessage(userID, data_sub):
    with open("./flex.json", encoding="utf8") as f:
        data = json.load(f)

    form = {
        "type": "bubble",
        "size": "giga",
        "body": {
            "type": "box",
            "layout": "vertical",
            "contents": [
                {"type": "text", "text": "เกรดของฉัน", "size": "xl", "weight": "bold"},
                {"type": "text", "text": "Year ... Term ..."},
                {"type": "separator", "margin": "md", "color": "#000000"},
                {
                    "type": "box",
                    "layout": "horizontal",
                    "contents": [
                        {
                            "type": "text",
                            "text": "วิชา",
                            "align": "start",
                            "weight": "bold",
                        },
                        {
                            "type": "text",
                            "text": "หน่วยกิต",
                            "align": "center",
                            "weight": "bold",
                        },
                        {
                            "type": "text",
                            "text": "เกรด",
                            "align": "end",
                            "weight": "bold",
                        },
                    ],
                },
                {"type": "box", "layout": "horizontal", "contents": []},
            ],
        },
    }

    index = 0
    print(data_sub.keys())
    data["to"] = userID
    print(data["to"])
    year = 1
    term = 0
    for semester in data_sub.values():
        if term == 2:
            year += 1
            term = 1
        else:
            term += 1
        data["messages"][0]["contents"]["contents"][index]["body"]["contents"][1][
            "text"
        ] = f"ปี {year} เทอม {term}"
        for course in semester["courses"]:
            subject = course["SName"]
            credit = course["Credit"]
            grade = course["Grade"]
            format_ = [
                {"type": "text", "text": subject, "align": "start", "size": "xs"},
                {"type": "text", "text": credit, "align": "center", "size": "xs"},
                {"type": "text", "text": grade, "align": "end", "size": "xs"},
            ]
            data["messages"][0]["contents"]["contents"][index]["body"][
                "contents"
            ].append({"type": "box", "layout": "horizontal", "contents": format_})
        if index < len(data_sub.keys()):  # Corrected condition
            GPA = f"เกรดเฉลี่ย : {semester['Overall']['GPA']}"
            CreditTerm = f"หน่วยกิต : {semester['Overall']['Credit']}"
            format_ = [
                {
                    "type": "text",
                    "text": CreditTerm,
                    "align": "start",
                    "size": "md",
                    "weight": "bold",
                },
                {
                    "type": "text",
                    "text": GPA,
                    "align": "end",
                    "size": "md",
                    "weight": "bold",
                },
            ]
            data["messages"][0]["contents"]["contents"][index]["body"][
                "contents"
            ].append(
                {"type": "separator", "margin": "xl", "color": "#000000"},
            )
            data["messages"][0]["contents"]["contents"][index]["body"][
                "contents"
            ].append({"type": "box", "layout": "horizontal", "contents": format_})
            if index < len(data_sub.keys()) - 1:
                data["messages"][0]["contents"]["contents"].append(copy.deepcopy(form))
        index += 1

    # Save the updated JSON back to file
    with open("./updated_flex.json", "w", encoding="utf8") as f:
        json.dump(data, f, indent=4, ensure_ascii=False)

    f.close()
    return data


def sendQuickReply(userID):
    rep = {
        "to": userID,
        "messages": [
            {
                "type": "text",
                "text": "เลือกสิ่งที่ต้องการได้เลยครับ",
                "quickReply": {
                    "items": [
                        {
                            "type": "action",
                            "action": {
                                "type": "message",
                                "label": "ดูผลการเรียน",
                                "text": "ผลการเรียน",
                            },
                        },
                        {
                            "type": "action",
                            "action": {
                                "type": "message",
                                "label": "สอนสมัครสมาชิก",
                                "text": "สอนสมัครสมาชิก",
                            },
                        },
                        {
                            "type": "action",
                            "action": {
                                "type": "message",
                                "label": "เกี่ยวกับเรา",
                                "text": "เกี่ยวกับเรา",
                            },
                        },
                        {
                            "type": "action",
                            "action": {
                                "type": "message",
                                "label": "ติดต่อเรา",
                                "text": "ติดต่อ",
                            },
                        },
                    ]
                },
            }
        ],
    }
    return rep


def sendHelp(userID):
    response = {
        "to": userID,
        "messages": [
            {
                "type": "flex",
                "altText": "This is a Flex Message",
                "contents": {
                    "type": "bubble",
                    "body": {
                        "type": "box",
                        "layout": "vertical",
                        "contents": [
                            {
                                "type": "box",
                                "layout": "horizontal",
                                "contents": [
                                    {
                                        "type": "box",
                                        "layout": "vertical",
                                        "contents": [
                                            {
                                                "type": "image",
                                                "aspectMode": "cover",
                                                "size": "full",
                                                "url": "https://media.discordapp.net/attachments/1044084393817415730/1098114936451895366/H90fb66987af642708083ec4b310b00a4L-removebg-preview_1.png?ex=661f5b3a&is=660ce63a&hm=5bf633c21af8f76c2d0785a143338cc528d5ff5f4df9d4e5b4b0a2192f56624d&=&format=webp&quality=lossless&width=437&height=437",
                                            }
                                        ],
                                        "cornerRadius": "100px",
                                        "width": "72px",
                                        "height": "72px",
                                    },
                                    {
                                        "type": "box",
                                        "layout": "vertical",
                                        "contents": [
                                            {
                                                "type": "text",
                                                "contents": [
                                                    {
                                                        "type": "span",
                                                        "text": "ณภพเอง :",
                                                        "weight": "bold",
                                                        "color": "#000000",
                                                    },
                                                    {"type": "span", "text": "     "},
                                                    {
                                                        "type": "span",
                                                        "text": "ถ้ามีปัญหาสามารถติดต่อได้ทางอีเมล",
                                                    },
                                                ],
                                                "size": "sm",
                                                "wrap": "true",
                                            },
                                            {
                                                "type": "box",
                                                "layout": "baseline",
                                                "contents": [
                                                    {
                                                        "type": "text",
                                                        "text": "nutnaphop24@gmail.com",
                                                        "size": "sm",
                                                        "color": "#000000",
                                                    }
                                                ],
                                                "spacing": "sm",
                                                "margin": "md",
                                            },
                                        ],
                                    },
                                ],
                                "spacing": "xl",
                                "paddingAll": "20px",
                            }
                        ],
                        "paddingAll": "0px",
                    },
                },
            }
        ],
    }
    return response
