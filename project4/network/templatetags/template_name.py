from django import template

register = template.Library()

# Used Registry to access dictionary items in my template, in this app its accessed in index.html
# please ensure to have registers and filters installed, you can use 'pip install django-registration' and 'pip install django-filter', or use pip3 instead of pip if using python3.x version.
@register.filter
def get_item(dictionary, key):
    return dictionary.get(key)

@register.filter
def check_contains(dictionary, args):
    arg_list = args.split(',')
    items=dictionary[arg_list[0]]
    for item in items:
        if item == arg_list[1]:
            return True 
    return False

@register.filter
def check_item(list, item):
    print("check from list!!!")
    for user in list:
        print("User: ", user.username)
        if user.follower.username == item:
            return True 
    return False

@register.filter  
def contains(list, item):
    if item in list:
        return True
    else:
        return False
    