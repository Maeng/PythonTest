
# coding: utf-8

teststr = input("Input String with () : ")

def checkstr(str) :
    if str.startswith(')') or str.endswith('(') :  
        return False
    else :  
        cntfrt = 0
        cntlst = 0
        for i in range(len(str)) : 
            if(str[i] == '(') : cntfrt += 1
            elif(str[i] == ')') : 
                cntlst += 1
                if cntlst > cntfrt : return False
            #input string include not "(" or ")"
            else : return False

        if cntfrt == cntlst : 
            return True

#print the result in prompt
#print(checkstr(teststr))

checkstr(teststr)

