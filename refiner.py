import json

file = input("File: ")
# voteStart = input("Vote Start: ")
# voteEnd = input("Vote End: ") 

with open(file, "r", encoding="utf-8") as f:
    data = json.load(f)
 
del data["channel"]
del data["guild"]
del data["exportedAt"]
del data["dateRange"]
for i in data["messages"]:
    del i["timestamp"]
    del i['type']
    del i['timestampEdited']
    del i ['callEndedTimestamp']
    del i['isPinned']
    del i['attachments']
    del i['embeds']
    del i['stickers']
    del i['reactions']
    del i['mentions']
    del i['inlineEmojis']
    del i["author"]["discriminator"]
    del i["author"]["nickname"]
    del i["author"]["color"]
    del i["author"]["isBot"]
    del i["author"]["avatarUrl"]
    for ii in i["author"]["roles"]:
        del ii['color']
        del ii['position']
        del ii['id']

with open("RefinedData\Palavras.json", "w", encoding="utf-8") as f:
    json.dump(data, f, indent=2)