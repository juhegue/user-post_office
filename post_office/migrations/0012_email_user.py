

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('post_office', '0011_models_help_text'),
    ]

    operations = [
        migrations.AddField(
            model_name='email',
            name='user_id',
            field=models.IntegerField(blank=True, null=True)
        ),
    ]
