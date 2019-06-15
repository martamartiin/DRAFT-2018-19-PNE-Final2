class Seq:
    def __init__(self, strbases):
        self.strbases = strbases

    def len(self):
        return len(self.strbases)

    def complement(self):
        complementary_seq = ""
        dic_bases = {"A":"T","G":"C","C":"G","T":"A"} #creating a dictionary with the complementary bases.
        for s_base in self.strbases: #loop within the bases of the sequence
            for base, complement in dic_bases.items(): #loop within the itemes in the diccionary
                complementary_seq += complement

            complement = Seq(complementary_seq)
        return complement

    def reverse(self):
        reverse_seq = self.strbases[::-1] #chainging the order of the bases.
        reversed = Seq(reverse_seq) #creating the sequence
        return reversed


    def count(self, base):
        number_b = self.strbases.count(base)
        return number_b

    def perc(self, base):
        nb = self.strbases.count(base)
        tl = len(self.strbases)
        perc = round((nb/tl)*100, 1)
        return perc
#END