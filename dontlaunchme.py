import SQLHashTable

def count_different_symbols(str1, str2):
    c=0
    for i in range(0, len(str1)):
        if (str1[i] != str2[i]):
            c+=1

    return c


sql = SQLHashTable.HashTable()

a = sql.get_all_elements()

#print (a[0])
#print(a[1])
print (count_different_symbols(a[0][1], a[0][1]))