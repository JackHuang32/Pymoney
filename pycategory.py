class categories:
    my_categories = ["expense",["food",["meal","snack","drink"],"transportation",["bus","railway"]],\
            "income",["salary","bonus"]]
    def __init__(self):
        self._categories = ["expense",["food",["meal","snack","drink"],"transportation",["bus","railway"]],\
            "income",["salary","bonus"]]

    def find_category(self,category,categories = my_categories):
        '''This function is for finding whether the category is in our category list, if yes
        we return the position otherwise we return False '''
        for cate in enumerate(categories):
            if cate[1] == category:
                return [cate[0],]
            elif type(cate[1]) == list:
                tmp = self.find_category(category,cate[1])
                if tmp != False:
                    return [cate[0],]+tmp 
        return False   
    def view_categories(self,cate = my_categories,time = 0):
        '''Show our specified categories with main categories and subcategories'''
        for items in cate:
            if type(items) != list:
                print(' '*2*time+'- '+items)
            else:
                self.view_categories(items,time+1)
    def get_category_str(self,cate = my_categories,time=0):
        for items in cate:
            if type(items) != list:
                yield ' '*2*time+'- '+items+'\n'
            else:
                yield from self.get_category_str(items,time+1)
    def find_subcategories(self,target):
        def sub_categories_gen(target,categories = self._categories,found = False):
            #print(categories)
            if type(categories) == list:
                for idx,category in enumerate(categories):
                    yield from sub_categories_gen(target,category,found)
                    if category == target and categories[-1] != category and type(categories[idx+1])==list:
                        yield from sub_categories_gen(target,categories[idx+1],True)
            else:
                if target == categories or found:
                    #print(f'collect {categories} !!')
                    yield categories
        return [i for i in sub_categories_gen(target)] 