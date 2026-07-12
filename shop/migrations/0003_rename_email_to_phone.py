from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("shop", "0002_contactmessage"),
    ]

    operations = [
        migrations.RenameField(
            model_name="contactmessage",
            old_name="email",
            new_name="phone",
        ),
        migrations.AlterField(
            model_name="contactmessage",
            name="phone",
            field=models.CharField(max_length=30, verbose_name="Telefon"),
        ),
    ]
