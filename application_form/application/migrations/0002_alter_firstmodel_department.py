# Generated by Django 4.2.2 on 2023-06-23 08:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('application', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='firstmodel',
            name='department',
            field=models.CharField(choices=[('AD', 'デザイン科'), ('EE', '電気工学科'), ('ME', '機械電子工学科'), ('CS', '情報工学科'), ('AC', '専攻科')], max_length=50),
        ),
    ]
