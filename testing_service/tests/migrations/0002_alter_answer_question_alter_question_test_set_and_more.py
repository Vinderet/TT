# Generated by Django 4.2.10 on 2024-02-16 21:20

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('tests', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='answer',
            name='question',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='answers', to='tests.question'),
        ),
        migrations.AlterField(
            model_name='question',
            name='test_set',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='questions', to='tests.testset'),
        ),
        migrations.DeleteModel(
            name='User',
        ),
    ]
