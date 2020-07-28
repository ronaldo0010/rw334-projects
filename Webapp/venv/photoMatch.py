import os

def get_pID(file_line):
    photo = file_line.find("photo_id")
    sub_line =  file_line[photo+12:len(file_line)]
    comma = sub_line.find(",")
    return(sub_line[0:comma-1])

photo = open("photo2.json")
photo_id_list = []
for j in photo:
    photo_id_list.append(get_pID(j) + ".jpg")

photo.close()
count = 0
directory = r"/home/jaakie/PycharmProjects/Project_2/venv/app/static/photos"
for filename in os.listdir(directory):
    if filename.endswith(".jpg") and filename in photo_id_list:
        count+=1
        continue
    else:
        os.remove(filename)
        continue
print(count)
