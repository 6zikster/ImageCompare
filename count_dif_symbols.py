class Count:
    @staticmethod
    def count_different_symbols(str1, str2):
        c = 0
        if (len(str1) != len(str2)):
            print (str(len(str1))+"; "+str(len(str2)) )
        for i in range(len(str1)):
            if str1[i] != str2[i]:
                c += 1
        return c
