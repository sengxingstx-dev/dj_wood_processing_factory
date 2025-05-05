import os


def wood_inventory_storage(instance, filename):
    wood_inventory_id = instance.id
    if wood_inventory_id is None:
        wood_inventory_id = "new"
    ext = filename.split(".")[-1]
    new_filename = f"wood_{wood_inventory_id}_image.{ext}"
    return os.path.join("wood/images/", new_filename)
