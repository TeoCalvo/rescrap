def get_value_mark(bs_obj, mark, value ):
    result = [ i for i in bs_obj.findAll( mark ) if value in i.text ]
    return result
