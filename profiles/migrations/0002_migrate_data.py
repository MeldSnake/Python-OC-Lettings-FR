# Generated by Django 3.0 on 2023-05-06 19:09

from django.db import migrations
from django.apps.registry import Apps


profile_map_props = {
    "user": "user",
    "favorite_city": "favorite_city",
}


def MigrateData(apps: Apps, schema_editor):
    """Migration des anciennces donnée depuis les anciennes table de oc_lettings_site vers lettings"""
    old_profile_t = apps.get_model("oc_lettings_site", "Profile")
    new_profile_t = apps.get_model("profiles", "Profile")

    # Re-Creation de tous les anciens profiles dans la nouvelle table.
    for profile in old_profile_t.objects.all():
        # Obtention des valeures de l'ancien profile.
        props = {k: getattr(profile, v) for k, v in profile_map_props.items()}
        # Creation du nouveau profile. (Si le profile n'existe pas dans la table).
        _ = new_profile_t.objects.get_or_create(**props)


def UnMigrateData(apps: Apps, schema_editor):
    """Inversement de la migration @see MigrateData"""
    new_profile_t = apps.get_model("oc_lettings_site", "Profile")
    old_profile_t = apps.get_model("profiles", "Profile")

    # Re-Creation de tous les anciens profiles dans la nouvelle table.
    for profile in new_profile_t.objects.all():
        # Obtention des valeures de l'ancien profile.
        props = {k: getattr(profile, v) for k, v in profile_map_props.items()}
        # Creation du nouveau profile. (Si le profile n'existe pas dans la table).
        _ = old_profile_t.objects.get_or_create(**props)



class Migration(migrations.Migration):
    dependencies = [
        ("profiles", "0001_initial"),
    ]

    operations = [
        migrations.RunPython(MigrateData, UnMigrateData),
    ]
