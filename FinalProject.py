booklist = open("booklist.txt","r").read().split("\n")
librarylog = open("librarylog.txt","r").read().split("\n")
currentDay = int(librarylog[-1])
del librarylog[-1]

def canCheckOut(person,book):
    copies = 0
    #Initial Copies
    for x in booklist:
        if book == x.split("#")[0]:
            copies += int(x.split("#")[1])
    #Copies currently in library -- add one if a new one is added or one is returned, subtract if one is checked out
    for x in librarylog:
        if book == x.split("#")[1]:
            if x.split("#")[2] == "True" or x.split("#")[2] == "False":
                copies += 1
            elif x.split("#")[3] == "RET":
                copies += 1
            else:
                copies -=1
    #Check out-able if there's more than 1 copy in the library, if they have less than $50 in fines, and if they don't currently have it checked out. If they have it checked out, they can return it, so to test for this we can just call the canReturn function (defined below)
    if copies < 1 or fines(person) > 50 or canReturn(person,book):
        return False
    return True

def fines(person):
    fines = 0
    ret = []
    bor = []
    needtopay = []
    #Index books checked out and returned in bor and ret respectively, also handle all fines paid
    for x in librarylog:
        ls = x.split("#")
        if ls[2] == person:
            if ls[0] == "PAY":
                fines -= int(ls[3])
            elif ls[3] == "RET":
                ret.append(ls)
            else:
                bor.append(ls)
    #Match check-outs with returns. If a book is overdue, add it (along with the number of days it's overdue by) to needtopay
    for x in bor:
        returned = False
        for y in range(0,len(ret)):
            if x[1] == ret[y][1]:
                returned = True
                if int(x[3])+int(x[0]) < int(ret[y][0]):
                    needtopay.append(x[1] + "#" + str(int(ret[y][0])-int(x[3])-int(x[0])))
                ret[y] = "|#|#|#|" #Placeholder, nothing in ret is ever going to read |#|#|#|, but it won't throw index out of bounds errors later because of the #s in it
                break
        if returned == False:
            if int(x[3]) < currentDay:
                needtopay.append(x[1] + "#" + str(currentDay - int(x[3])-int(x[0])))
    #Check if books in needtopay are important and increment fines accordingly
    for x in needtopay:
        important = False
        for y in booklist:
            if x.split("#")[0] == y.split("#")[0] and y.split("#")[2] == "True":
                important = True
        for y in librarylog:
            if x.split("#")[0] == y.split("#")[1] and y.split("#")[2] == "True":
                important = True
        if important:
            fines += int(x.split("#")[1])*15
        else:
            fines += int(x.split("#")[1])*5
    return fines

def canReturn(person,book):
    bookscheckedout = 0
    #Increment bookscheckedout if person checks out book, decrement if person returns book
    for x in librarylog:
        if x.split("#")[1] == book and x.split("#")[2] == person:
            if x.split("#")[3] == "RET":
                bookscheckedout -= 1
            else:
                bookscheckedout += 1
    if bookscheckedout > 0:
        return True
    return False

def lateFeesList():
    output = []
    peopleList = []
    #Make a list of all the people
    for x in librarylog:
        if x.split("#")[2] != "True" and x.split("#")[2] != "False":
            if x.split("#")[2] not in peopleList:
                peopleList.append(x.split("#")[2])
    #For each person, check if they have fines. If they do, add to output
    for x in peopleList:
        if fines(x) != 0:
            output.append(x + "#" + str(fines(x)))
    #Sort by fine amount, descending
    output.sort(key = lambda x: int(x.split("#")[1]), reverse = True)
    return output

def bookUsage():
    denom = []
    num = []
    #Process total number of book-days from booklist
    for x in booklist:
        denom.append(x.split("#")[0]+"#"+str((currentDay-1)*int(x.split("#")[1])))
    #Account for any book-days from books added after day 0
    for x in librarylog:
        if x.split("#")[2] == "True" or x.split("#")[2] == "False":
            alreadyThere = False
            for y in range(0,len(denom)):
                if denom[y].split("#")[0] == x.split("#")[1]:
                    denom[y] = denom[y].split("#")[0] + "#" + str(int(denom[y].split("#")[1]) + currDay - int(x.split("#")[0]))
                    alreadyThere = True
                    break
            if alreadyThere == False:
                denom.append(x.split("#")[1] + "#" + str(currentDay-int(x.split("#")[0])))
    #Index all books for the numerator portion
    for x in denom:
        num.append(x.split("#")[0] + "#0")
    #Every time a book is checked out, check for when it's returned (up till current day if it isn't returned). Increment num for that book by the number of days it was checked out.
    for x in range(0,len(librarylog)):
        if librarylog[x].split("#")[0] == "PAY" or librarylog[x].split("#")[2] == "True" or librarylog[x].split("#")[2] == "False" or librarylog[x].split("#")[3] == "RET":
            pass
        else:
            title = librarylog[x].split("#")[1]
            person = librarylog[x].split("#")[2]
            found = False
            for y in range(x+1,len(librarylog)):
                if librarylog[y].split("#")[2] == "True" or librarylog[y].split("#")[2] == "False" and librarylog[x].split("#")[3] != "RET":
                    pass
                else:
                    if title == librarylog[y].split("#")[1] and person == librarylog[y].split("#")[2]:
                        for z in range(0,len(num)):
                            if num[z].split("#")[0] == title and found == False:
                                num[z] = num[z].split("#")[0] + "#" + str(int(num[z].split("#")[1]) + int(librarylog[y].split("#")[0]) - int(librarylog[x].split("#")[0]))
                                found = True
            if found == False:
                for y in range(0,len(num)):
                    if title == num[y].split("#")[0]:
                        num[y] = num[y].split("#")[0] + "#" + str(int(num[y].split("#")[1]) + currentDay - int(librarylog[x].split("#")[0]))
                        break
    output = []
    #Math to get from num and denom to percentages
    for x in range(0,len(num)):
        output.append(num[x].split("#")[0] + "#" + str(int(float(10000*int(num[x].split("#")[1])/int(denom[x].split("#")[1])))/100))
    #Sort by percentages, descending
    output.sort(key = lambda x: float(x.split("#")[1]), reverse = True)
    return output

def main():
    feeslist = lateFeesList()
    usage = bookUsage()
    print("Students with Late Fees:")
    for x in feeslist:
        print("     " + x.split("#")[0] + ": $" + x.split("#")[1])
    print("\nMost Used Books:")
    for x in usage:
        print("     " + x.split("#")[0] + ": " + x.split("#")[1] + "%")

main()
