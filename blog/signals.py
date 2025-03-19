from django.contrib.auth.models import Group, Permission

def create_group_permission(sender, **kwargs):
    try:
        # Create groups
        readers_group, created = Group.objects.get_or_create(name="Readers")
        editors_group, created = Group.objects.get_or_create(name="Editors")
        authors_group, created = Group.objects.get_or_create(name="Authors")

        # Create permissions
        readers_permissions = [
            Permission.objects.get(codename = "view_post"),
        ]

        authors_permissions = [
            Permission.objects.get(codename="add_post"),
            Permission.objects.get(codename="delete_post"),
            Permission.objects.get(codename="change_post"),
        ]
        can_publish, created = Permission.objects.get_or_create(codename="can_publish", content_type_id=8, name="Can publish post")

        editors_permissions = [
            can_publish,
            Permission.objects.get(codename="add_post"),
            Permission.objects.get(codename="delete_post"),
            Permission.objects.get(codename="change_post"),
        ]

        # Assigning permission to groups
        readers_group.permissions.set(readers_permissions)
        authors_group.permissions.set(authors_permissions)
        editors_group.permissions.set(editors_permissions)

    except Exception as e:
        print(f"Error occurred as {e}")
    print("Groups and permissions created successfully")
