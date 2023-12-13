import textwrap
from datetime import datetime, date, timedelta

def charges_sort(p_name):
    charge_counter = 0
    times = []
    charges = []
    sentences = []
    new_charges = []
    new_times = []
    

    counter = 0

    with open("charges.txt", "r") as f:
        lines = f.readlines()
        for line in lines:
            if line not in ["Body Cam\n","BOT\n"] and " 0 seconds" not in line:
                if " â€” " in line:
                    new_line = line.replace(" â€” ","").replace(" AM","AM").replace(" PM","PM")
                    charge_counter += 1
                    if "Today" in new_line:
                        today = datetime.today().strftime('%m/%d/%Y')
                        new_line = new_line.replace("Today",today).replace(" at","")
                        # print(today)
                    if "Yesterday" in new_line:
                        yesterday = (datetime.today() - timedelta(days = 1)).strftime('%m/%d/%Y')
                        new_line = new_line.replace("Yesterday",yesterday).replace(" at","")
                        # print(yesterday)


                    times.append(new_line)
                else:
                    if len(line) < 20:
                        new_line = ("," + line).replace("\n","")

                        charges[len(charges)-1] = charges[len(charges)-1].replace("\n","")
                        charges[len(charges)-1] += new_line
                        
                    else:
                        new_line = line.replace('\n',"")
                        charges.append(new_line)
                    # split_line = new_line.split(" for ")
                    # print(split_line)
                # f.write(new_line)



            counter += 1


    

    for i in range(len(times)):
        time = times[i].replace("\n","").replace(" ","\n")
        times[i] = time

    # print(times)
    # print(charges)

    table = {}

    new_counter = 0


    loop_counter = 0
    # print(charges)
    for item in charges:
        # print(item)
        items = item.split(" arrested ")
        items.pop(0)
        string = "".join(items)
        items = string.split(" for ")
        if items[0] not in table.keys():
            table[items[0]] = {}
        original_name = items[0]
        # print(original_name)
        if original_name == p_name:
            # print(original_name)
            
            items.pop(0)
            string = "".join(items)
            items = string.split(" with the charges ")

            items[1] = items[1].split(",")

            # print(items)

            if new_counter == 0:
                table[original_name] = []

            new_times.append(times[loop_counter])

            time = new_times[new_counter]
            table[original_name].append({time:{"Charges":items[1],"Sentence":items[0]}})

            new_charges.append(items[1])
            sentences.append(items[0])



            # table[name][times[new_counter]] = {}
            # table[name][times[new_counter]]["Sentence"] = items[0]
            # table[name][times[new_counter]]["Charges"] = items[1]

            
            new_counter += 1


        loop_counter += 1


    return [table,new_times,new_charges,sentences,original_name]



def charges_format(charge):
    wrapper = textwrap.TextWrapper(width=16) 
    word_list = wrapper.wrap(text=charge) 
    caption = ''
    for ii in word_list[:-1]:
        caption = caption + ii + '\n'
    caption += word_list[-1]
    
    return caption

# def charges_format_2(charges):
#     if len(charges) == 2:


def time_to_timestamp(time):

    new_time = time.split("\n")
    mdy = new_time[0].split("/")

    # print(mdy)


    formatted = f"{mdy[2]}-{mdy[0]}-{mdy[1]} "
    if len(new_time[1]) == 6:
        working_time = "0"+new_time[1]
    else:
        working_time = new_time[1]



    if "PM" in working_time:
        working_time = (str(int(working_time[:2])+12)) + working_time[2:]

    working_time = working_time.replace("PM",":00").replace("AM",":00")

    final = formatted + working_time

    # format_string = "%Y-%m-%d %H:%M:%S"
    # datetime_object = datetime.strptime(final, format_string)

    # return datetime_object

    return final

# charges_sort("charges.txt")