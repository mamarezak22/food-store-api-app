def store_picture_upload_to(filename , instance):
    return f'stores/{instance.name}/filename'
def food_picture_upload_to(filename,instance):
    return f'stores/{instance.store}/foods/{instance.name}/filename'