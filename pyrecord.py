import sys
from pycategory import*
import datetime as dt
class record:
    def __init__(self,time,category,name,price):
        self.set_time(time)
        self.set_category(category)
        self.set_name(name)
        self.set_price(price)
    def set_time(self,t):
        self._time = t 
    def set_category(self,c):
        self._category = c
    def set_name(self,n):
        self._name = n
    def set_price(self,p):
        self._price = p
    def __repr__(self):
        return f'{self.time} {self.category} {self.name} {self.price}'
    def __eq__(self,other):
        if type(self) != type(other):
            return False
        else:
            return self.time == other.time and self.category == other.category and self.name==other.name and self.price == other.price
    @property
    def get_time(self):
        return self._time
    @property
    def get_category(self):
        return self._category
    @property
    def get_name(self):
        return self._name
    @property
    def get_price(self):
        return self._price
    time = property(lambda self:self.get_time,
                    lambda self,t:self.set_time(t))
    category = property(lambda self:self.get_category,
                        lambda self,c:self.set_category(c))
    name = property(lambda self:self.get_name,
                    lambda self,n:self.set_name(n))
    price = property(lambda self:self.get_price,
                     lambda self,p:self.set_price(p))
class records:
    def __init__(self):
        '''skip each line of the file "records.txt" if it's not of the form 'meal breakfast -50'
        or the first category is not in the original classification list otherwise we read each
        'meal breakfast -50' as a tuple ('meal','breakfast',-50)   
        '''
        cate = categories()
        tmp_items = []
        self._money = 0
        self._items = []
        try:
            with open('records.txt','r') as fh:
                try:
                    self._money = int(fh.readlines()[0][:-1])
                    fh.seek(0)
                    for line in fh.readlines():
                        tmp_items.append(line[:-1])
                    tmp_items.pop(0)
                    for idx,item in enumerate(tmp_items):
                        try:
                            if len(item.split()) != 4:
                                tmp_items.pop(idx)
                                print('Skip item because of invalid form')
                            elif cate.find_category(item.split()[1]) == False:
                                raise ValueError
                            else:
                                self._items.append(record(str(item.split()[0]),item.split()[1],item.split()[2],int(item.split()[3])))
                        except (ValueError,IndexError):
                            sys.stderr.write('Skip item because of invalid form\n')
                except ValueError:
                    sys.stderr.write('Invalid value for money. Set to 0 by default.\n')
                    self._money = 0
                except IndexError:
                    sys.stderr.write('Empty reccord. Set to zero by default.\n')
                    self._money = 0
        except FileNotFoundError:
            self._money = 0
    def get_items_str(self):
        return list(map(lambda item:str(item.time)+' '+str(item.category)+' '+str(item.name)+' '+str(item.price),self._items))         
    def set_money(self,m):
        if m != '': 
            self._money = int(m)
    def add(self,new_record):
        '''Add item into the list and check if it's in the form like 'meal breakfast -50'
    we report a failure if it's not as the form or the category is invalid
    '''
        try:
            item = new_record
            error_message = ''
            #item = item.split()[0],item.split()[1],item.splt()[2],int(item.split()[3])#item = '{} {}'.format(item[0],item[1])  #meal breakfast -50 => (meal,breakfast,-50)
            item = item.split()
            if len(item) < 3 or 4 < len(item):
                raise IndexError
            elif len(item) == 3:
                item = str(dt.date.today()),item[0],item[1],int(item[2]) 
            elif len(item) == 4:
                try:
                    date = dt.date.fromisoformat(item[0])
                except:
                    print('here')
                    error_message = 'Invalid date format! set to today by default\n'
                    date = str(dt.date.today())
                item = date,item[1],item[2],int(item[3]) 
            cate = categories()
            if not cate.find_category(item[1],cate._categories):
                raise SyntaxError
            self._money += item[3]
            self._items.append(record(str(item[0]),item[1],item[2],int(item[3])))      #add into list
            return True,' '.join([str(i) for i in item]),error_message
        except SyntaxError:
            sys.stderr.write('There is no such category!!\n')
            sys.stderr.write('Fail to add the record.\n')
            return False,None,'There is no such category!!\n'
        except IndexError:
            sys.stderr.write('The format of a record should be like this:\n 2020-06-08(optional) meal breakfast -50.\n')
            sys.stderr.write('Fail to add the record.\n')
            return False,None,'The format of a record should be like this:\n2020-06-08(optional) meal breakfast -50.\n'
        except ValueError:
            sys.stderr.write('The price should be an integer\n')
            sys.stderr.write('Fail to add the record.\n')  
            return False,None,'The price should be an integer\n' 
    def view(self):
        '''Show the current list with the category, the name and the price
        finally we show the money we have now'''
        print('Here\'s your expense and income records:')
        print('Date       Category        Description          Amount')
        print('========== =============== ==================== ======')
        for item in self._items:
            print('{:10} {:15} {:20} {:6}'.format(item.time,item.category,item.name,item.price))
        print('======================================================')
        print(f'Now you have {self._money} dollars.')     
    def delete(self,record):
        '''Remove an item with the specific name '''
        self._money -= record.price
        self._items.remove(record)
        
    def find(self,tar):
        '''First check if we have such category then use filter to collect 
        the one with the category or subcategory
        finally show the total of the out put items'''
        
        target = tar
        cate = categories()
        check_set = cate.find_subcategories(target)
        if len(check_set)==0:
            return 0,'There is no such category!!',None
        check_set = set(check_set)
        out_put = self._items
        out_put = filter(lambda x:x.category in check_set,out_put)
        #print(f'Here is the categories {check_set}')
        print(f'Here\'s your expense and income records under category "{target}":')
        print('Date       Category        Description          Amount')
        print('========== =============== ==================== ======')
        found_list = []
        money = 0
        for item in out_put:
            money += item.price
            print('{:10} {:15} {:20} {:6}'.format(item.time,item.category,item.name,item.price))
            found_list.append(' '.join([str(item.time),item.category,item.name,str(item.price)]))
        print('======================================================')
        print(f'The total amount above is {money}.')  
        if len(found_list)==0:
            return 1,'There is no such record!!',None
        return 2,found_list,money        
    def save(self):
        '''Write the current list into the file 'records.txt' as the form 'meal breakfast -50' '''
        with open('records.txt','w') as fh:
            fh.write(str(self._money)+'\n')
            for item in self._items:
                fh.write(' '.join((str(item.time),item.category,item.name,str(item.price)))+'\n')
        return    
