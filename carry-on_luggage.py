#-*- coding:utf-8 -*-
import unittest

#class of luggage
class luggage:
    def __init__(self,width,long,hight,weight):
        self.A=width
        self.B=long
        self.C=hight
        self.W=weight
    def is_valid(self):
        if(self.A>0 and self.B>0 and self.C>0 and self.W>0):
            return True
        else:
            return False

    # check the luggage whether normal or not

    #the maxsize of luggage in forigner:  A+B+C<=300 and W<=45
    def is_normal_of_foreign(self):
        if (self.A+self.B+self.C<=300 and self.weight<=45):
            return True
        else:
            return False

    # the maxsize of luggage in domestic:  A<=40 B<=60 C<=100 W<50
    def is_normal_of_domestic(self):
        if (self.A <= 40 and self.B <= 60 and self.C <= 100 and self.W<50):
            return True
        else:
            return False

#the cost of domestic
#the domestic luggage should be A<=40 B<=60 C<=100 W<=50,otherwise you should split the luggage
#moreover,if you have more than one luggage,the cost of more luggages will be charged by current price of economical ticket
class domestic():
    def __init__(self,p,f):
        self.price=p
        self.flight=f

    #to chosse a right way to  get the cost
    def calculate(self, num,lug):
        if (self.flight == 'first_class'):
            return self.cost(40, num, lug)
        elif (self.flight == 'business_class'):
            return self.cost(30, num, lug)
        elif (self.flight == 'economy_class'):
            return self.cost(20, num, lug)
        elif (self.flight == 'infant_class'):
            return self.cost(10, num, lug)
        else:
            return 0,0

    # calculate the cost of  first_class
    #free_of_weight--> first_class:40 , business_class:30 , economy_class:20 , infant:10
    def cost(self, free_of_weight,num, lug):
        cost = 0
        i = 0  # index of which luggage
        while (i < num):
            if (not lug[i].is_valid() or not lug[i].is_normal_of_domestic()):
                return 0, i + 1  # the first paragrame 0:means number invalid 1:means number normal,the second means while is invalid
            else:
                if(i==0):#the first luggage should be treat Specially
                    if(lug[i].W>free_of_weight):
                        cost += (lug[i].W-free_of_weight)*self.price
                else:
                    cost+=lug[i].W*self.price
            i+=1
        return 1, cost

#the cost of area1
class area1():
    def __init__(self,f):
        self.flight=f

    # to chosse a right way to  get the cost
    def calculate(self, num,lug):
        if (self.flight == 'first_class'):
            return self.first_class(num, lug)
        elif (self.flight == 'business_class'):
            return self.business_class(num, lug)
        elif (self.flight == 'economy_class'):
            return self.economy_class(num, lug)
        elif (self.flight == 'infant_without_seat'):
            return self.infant_without_seat(num, lug)
        else:
            return 0,0

    #calculate the cost of  first_class
    def first_class(self, num,lug):
        cost=0
        i=0 #index of which luggage
        j=0 #numbers of normal luggage
        while(i<num):
            if(not lug[i].is_valid() or not lug[i].is_normal_of_foreign()):
                return 0,i+1#the first paragrame 0:means number invalid 1:means number normal ; the second means while is invalid
            else:
                if(lug[i].W>32):
                    cost += 3000
                elif(lug[i].A+lug[i].B+lug[i].C>158):
                    cost += 1000
                else:
                    j+=1
            i+=1
        if(j>3):#not oversize or overweight but over numbers
            cost += 1000
            if(j>4):#over 4 more pieces
                cost += 2000*(i-4)
        return 1,cost

    # calculate the cost of  bussiness_class
    def business_class(self, num,lug):
        cost = 0
        i = 0  # index of which luggage
        j = 0  # numbers of normal luggage
        while (i < num):
            if (not lug[i].is_valid() or not lug[i].is_normal_of_foreign()):
                return 0, i + 1
            else:
                if (lug[i].W > 32):
                    cost += 3000
                elif (lug[i].A + lug[i].B + lug[i].C > 158):
                    cost += 1000
                else:
                    j += 1
            i += 1
        if (j > 2):  # not oversize or overweight but over numbers
            cost += 1000
            if j>3:#over 3 more pieces
                cost += 2000 * (i - 3)
        return 1, cost

    # calculate the cost of  economy_class
    def economy_class(self, num,lug):
        cost = 0
        i = 0  # index of which luggage
        j = 0  # numbers of normal luggage
        while (i < num):
            if (not lug[i].is_valid() or not lug[i].is_normal_of_foreign()):
                return 0, i + 1
            else:
                if (lug[i].W > 23 and lug[i].W <= 32):
                    cost += 1000
                elif(lug[i].W > 32):
                    cost += 3000
                elif (lug[i].A + lug[i].B + lug[i].C > 158):
                    cost += 1000
                else:
                    j += 1
            i += 1
        if (j > 2):  # not oversize or overweight but over numbers
            cost += 1000
            if j > 3:  # over 3 more pieces
                cost += 2000 * (i - 3)
        return 1, cost

    # check  infant taking no seat whether normal
    #note: the infant must take flight with guardian ,the not qualified luggage should be added to guardian
    def infant_without_seat(self,lug):
        if (lug.A + lug.B + lug.C > 158 and lug.W<=10):
            return True
        else:
            return False

#the cost of area2
class area2():
    def __init__(self,f):
        self.flight=f

    # to chosse a right way to  get the cost
    def calculate(self, num,lug):
        if (self.flight == 'first_class'):
            return self.first_class(num, lug)
        elif (self.flight == 'business_class'):
            return self.business_class(num, lug)
        elif (self.flight == 'economy_class'):
            return self.economy_class(num, lug)
        elif (self.flight == 'infant_without_seat'):
            return self.infant_without_seat(num, lug)
        else:
            return 0,0

    #calculate the cost of  first_class
    def first_class(self, num,lug):
        cost=0
        i=0 #index of which luggage
        j=0 #numbers of normal luggage
        while(i<num):
            if(not lug[i].is_valid() or not lug[i].is_normal_of_foreign()):
                return 0,i+1#the first paragrame 0:means number invalid 1:means number normal ; the second means while is invalid
            else:
                if(lug[i].W>32):
                    cost += 3000
                elif(lug[i].A+lug[i].B+lug[i].C>158):
                    cost += 1000
                else:
                    j+=1
            i+=1
        if(j>3):#not oversize or overweight but over numbers
            cost += 450
            if(j>4):#over 4 more pieces
                cost += 1300*(i-4)
        return 1,cost

    # calculate the cost of  bussiness_class
    def business_class(self, num,lug):
        cost = 0
        i = 0  # index of which luggage
        j = 0  # numbers of normal luggage
        while (i < num):
            if (not lug[i].is_valid() or not lug[i].is_normal_of_foreign()):
                return 0, i + 1
            else:
                if (lug[i].W > 32):
                    cost += 3000
                elif (lug[i].A + lug[i].B + lug[i].C > 158):
                    cost += 1000
                else:
                    j += 1
            i += 1
        if (j > 2):  # not oversize or overweight but over numbers
            cost += 450
            if j>3:#over 3 more pieces
                cost += 1300 * (i - 3)
        return 1, cost

    # calculate the cost of  economy_class
    def economy_class(self, num,lug):
        cost = 0
        i = 0  # index of which luggage
        j = 0  # numbers of normal luggage
        while (i < num):
            if (not lug[i].is_valid() or not lug[i].is_normal_of_foreign()):
                return 0, i + 1
            else:
                if(lug[i].W > 32):
                    cost += 3000
                elif (lug[i].A + lug[i].B + lug[i].C > 158):
                    cost += 1000
                else:
                    j += 1
            i += 1
        if (j > 1):  # not oversize or overweight but over numbers
            cost += 450
            if j > 3:  # over 3 more pieces
                cost += 1300 * (i - 2)
        return 1, cost

    # check  infant taking no seat whether normal
    #note: the infant must take flight with guardian ,the not qualified luggage should be added to guardian
    def infant_without_seat(self,lug):
        if (lug.A + lug.B + lug.C > 158 and lug.W<=10):
            return True
        else:
            return False

#the cost of area3
class area3():
    def __init__(self,f):
        self.flight=f
    # to chosse a right way to  get the cost
    def calculate(self, num,lug):
        if (self.flight == 'first_class'):
            return self.first_class(num, lug)
        elif (self.flight == 'business_class'):
            return self.business_class(num, lug)
        elif (self.flight == 'economy_class'):
            return self.economy_class(num, lug)
        elif (self.flight == 'infant_without_seat'):
            return self.infant_without_seat(num, lug)
        else:
            return 0,0

    #calculate the cost of  first_class
    def first_class(self, num,lug):
        cost=0
        i=0 #index of which luggage
        j=0 #numbers of normal luggage
        while(i<num):
            if(not lug[i].is_valid() or not lug[i].is_normal_of_foreign()):
                return 0,i+1#the first paragrame 0:means number invalid 1:means number normal ; the second means while is invalid
            else:
                if(lug[i].W>32):
                    cost += 3000
                elif(lug[i].A+lug[i].B+lug[i].C>158):
                    cost += 1000
                else:
                    j+=1
            i+=1
        if(j>3):#not oversize or overweight but over numbers
            cost += 1000
            if(j>4):#over 4 more pieces
                cost += 2000*(i-4)
        return 1,cost

    # calculate the cost of  bussiness_class
    def business_class(self, num,lug):
        cost = 0
        i = 0  # index of which luggage
        j = 0  # numbers of normal luggage
        while (i < num):
            if (not lug[i].is_valid() or not lug[i].is_normal_of_foreign()):
                return 0, i + 1
            else:
                if (lug[i].W > 32):
                    cost += 3000
                elif (lug[i].A + lug[i].B + lug[i].C > 158):
                    cost += 1000
                else:
                    j += 1
            i += 1
        if (j > 2):  # not oversize or overweight but over numbers
            cost += 1000
            if j>3:#over 3 more pieces
                cost += 2000 * (i - 3)
        return 1, cost

    # calculate the cost of  economy_class
    def economy_class(self, num,lug):
        cost = 0
        i = 0  # index of which luggage
        j = 0  # numbers of normal luggage
        while (i < num):
            if (not lug[i].is_valid() or not lug[i].is_normal_of_foreign()):
                return 0, i + 1
            else:
                if (lug[i].W > 23 and lug[i].W <= 32):
                    cost += 2000
                elif(lug[i].W > 32):
                    cost += 3000
                elif (lug[i].A + lug[i].B + lug[i].C > 158):
                    cost += 1000
                else:
                    j += 1
            i += 1
        if (j > 2):  # not oversize or overweight but over numbers
            cost += 1000
            if j > 3:  # over 3 more pieces
                cost += 2000 * (i - 3)
        return 1, cost

    # check  infant taking no seat whether normal
    #note: the infant must take flight with guardian ,the not qualified luggage should be added to guardian
    def infant_without_seat(self,lug):
        if (lug.A + lug.B + lug.C > 158 and lug.W<=10):
            return True
        else:
            return False

#the cost of area4
class area4():
    def __init__(self,f):
        self.flight=f

    # to chosse a right way to  get the cost
    def calculate(self, num,lug):
        if (self.flight == 'first_class'):
            return self.first_class(num, lug)
        elif (self.flight == 'business_class'):
            return self.business_class(num, lug)
        elif (self.flight == 'mz_economy_class'):
            return self.mz_economy_class(num, lug)
        elif (self.flight == 'economy_class'):
            return self.economy_class(num, lug)
        elif (self.flight == 'infant_without_seat'):
            return self.infant_without_seat(num, lug)
        else:
            return 0,0

    #calculate the cost of  first_class
    def first_class(self, num,lug):
        cost=0
        i=0 #index of which luggage
        j=0 #numbers of normal luggage
        while(i<num):
            if(not lug[i].is_valid() or not lug[i].is_normal_of_foreign()):
                return 0,i+1#the first paragrame 0:means number invalid 1:means number normal ; the second means while is invalid
            else:
                if(lug[i].W>32):
                    cost += 3000
                elif(lug[i].A+lug[i].B+lug[i].C>158):
                    cost += 1000
                else:
                    j+=1
            i+=1
        if(j>3):#not oversize or overweight but over numbers
            cost += 450
            if(j>4):#over 4 more pieces
                cost += 1300*(i-4)
        return 1,cost

    # calculate the cost of  bussiness_class
    def business_class(self, num,lug):
        cost = 0
        i = 0  # index of which luggage
        j = 0  # numbers of normal luggage
        while (i < num):
            if (not lug[i].is_valid() or not lug[i].is_normal_of_foreign()):
                return 0, i + 1
            else:
                if (lug[i].W > 23 and lug[i].W <= 32):
                    cost += 1000
                elif(lug[i].W > 32):
                    cost += 3000
                elif (lug[i].A + lug[i].B + lug[i].C > 158):
                    cost += 1000
                else:
                    j += 1
            i += 1
        if (j > 3):  # not oversize or overweight but over numbers
            cost += 450
            if j>4:#over 3 more pieces
                cost += 2000 * (i - 4)
        return 1, cost

    # calculate the cost of  MingZhu economy_class
    def mz_economy_class(self, num, lug):
        cost = 0
        i = 0  # index of which luggage
        j = 0  # numbers of normal luggage
        while (i < num):
            if (not lug[i].is_valid() or not lug[i].is_normal_of_foreign()):
                return 0, i + 1
            else:
                if (lug[i].W > 23 and lug[i].W <= 32):
                    cost += 1000
                elif (lug[i].W > 32):
                    cost += 3000
                elif (lug[i].A + lug[i].B + lug[i].C > 158):
                    cost += 1000
                else:
                    j += 1
            i += 1
        if (j > 2):  # not oversize or overweight but over numbers
            cost += 450
            if j > 3:  # over 3 more pieces
                cost += 1300 * (i - 3)
        return 1, cost

    # calculate the cost of  economy_class
    def economy_class(self, num,lug):
        cost = 0
        i = 0  # index of which luggage
        j = 0  # numbers of normal luggage
        while (i < num):
            if (not lug[i].is_valid() or not lug[i].is_normal_of_foreign()):
                return 0, i + 1
            else:
                if (lug[i].W > 23 and lug[i].W <= 32):
                    cost += 1000
                elif(lug[i].W > 32):
                    cost += 3000
                elif (lug[i].A + lug[i].B + lug[i].C > 158):
                    cost += 1000
                else:
                    j += 1
            i += 1
        if (j > 1):  # not oversize or overweight but over numbers
            cost += 450
            if j > 3:  # over 3 more pieces
                cost += 1300 * (i - 3)
        return 1, cost

    # check  infant taking no seat whether normal
    #note: the infant must take flight with guardian ,the not qualified luggage should be added to guardian
    def infant_without_seat(self,lug):
        if (lug.A + lug.B + lug.C > 158 and lug.W<=10):
            return True
        else:
            return False

def calculate_cost_carry_on(area,flight,num,lug):
    if(area=='domestic'):
        dom=domestic(100,flight) #the parameter means the price of thee current economy ticket , the second means type of flight
        flag,cost=dom.calculate(num,lug)
        if flag==0:
            print 'you luggage message is invalid: luggage-->'+str(cost)
            return -1
        else:
            return cost
    elif(area=='area1'):
        a1=area1(flight)
        flag, cost = a1.calculate(num, lug)
        if flag==0:
            print 'you luggage message is invalid: luggage-->' + str(cost)
            return -1
        else:
            return cost
    elif(area=='area2'):
        a2=area2(flight)
        flag, cost = a2.calculate(num, lug)
        if flag==0:
            print 'you luggage message is invalid: luggage-->' + str(cost)
            return -1
        else:
            return cost
    elif(area=='area3'):
        a3=area3(flight)
        flag, cost = a3.calculate(num, lug)
        if flag==0:
            print 'you luggage message is invalid: luggage-->' + str(cost)
            return -1
        else:
            return cost
    elif(area=='area4'):
        a4=area4(flight)
        flag, cost = a4.calculate(num, lug)
        if flag==0:
            print 'you luggage message is invalid: luggage-->' + str(cost)
            return -1
        else:
            return cost
    else:
        return -1

class test(unittest.TestCase):
    def setUp(self):
        # area num luggage
        # width,long,hight,weight
        lug = []
    def tearDown(self):
        print 'end...'
    def test_one(self):
        area = 'domestic'
        flight = 'first_class'
        lug = []
        # domedstic
        lug.append(luggage(30, 30, 50, 40))  # normal
        num = 1
        print calculate_cost_carry_on(area, flight, num, lug)

    def test_two(self):
        area = 'domestic'
        flight = 'first_class'
        lug = []
        # domedstic
        lug.append(luggage(30, 30, 50, 40))  # normal
        lug.append(luggage(30, 30, 50, 40))  # overpieces
        num = 2
        print calculate_cost_carry_on(area, flight, num, lug)

    def test_three(self):
        area = 'domestic'
        flight = 'first_class'
        lug = []
        # domedstic
        lug.append(luggage(30, 30, 50, 40))  # normal
        lug.append(luggage(-1, 30, 50, 40))  # overpieces
        num = 2
        print calculate_cost_carry_on(area, flight, num, lug)


    # def test_t(self):
    #     area = 'domestic'
    #     flight = 'first_class'
    #     lug = []
    #     # domedstic
    #     lug.append(luggage(30, 30, 50, 40))  # normal
    #     lug.append(luggage(-1, 30, 50, 40))  # overpieces
    #     lug.append(luggage(30, 30, 50, 40))  # overpieces
    #     lug.append(luggage(30, 80, 50, 40))  # oversize
    #     lug.append(luggage(30, 30, 50, 55))  # overweight
    #     # lug[1]=luggage(30,40,70,100)
    #     num = 2
    #     print calculate_cost_carry_on(area, flight, num, lug)

if __name__ == '__main__':
    unittest.main()




    # a,b=is_normal('国内航班',lug)
    # print a
    # print b




