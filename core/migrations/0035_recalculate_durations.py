# Generated by Django 5.1.2 on 2024-11-02 17:32
from django.db import migrations
from django.utils import timezone

from core.utils import timezone_aware_duration


class Migration(migrations.Migration):

    def calculate_timezone_aware_durations(apps, schema_editor):
        """
        Adjust incorrect stored durations. Previously these were calculated
        with the user's timezone and did not account for DST. There is no
        reverse code for this migration as we don't know what timezone the
        original duration calculation used.
        """
        for model_name in ["Feeding", "Pumping", "Sleep", "TummyTime"]:
            model = apps.get_model("core", model_name)
            for instance in model.objects.all():
                new_duration = timezone_aware_duration(instance.start, instance.end)
                if instance.duration != new_duration:
                    instance.duration = new_duration
                    instance.save()

    dependencies = [
        ("core", "0034_alter_tag_options"),
    ]

    operations = [
        migrations.RunPython(
            calculate_timezone_aware_durations, migrations.RunPython.noop
        )
    ]