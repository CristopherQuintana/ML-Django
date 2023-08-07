# Generated by Django 4.2.2 on 2023-08-05 20:46

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='PublicacionData',
            fields=[
                ('id', models.TextField(primary_key=True, serialize=False)),
                ('title', models.TextField()),
                ('condition', models.TextField()),
                ('price', models.IntegerField()),
                ('permalink', models.TextField()),
                ('thumbnail', models.TextField()),
                ('sold_quantity', models.IntegerField()),
                ('available_quantity', models.IntegerField()),
                ('seller_id', models.TextField()),
                ('seller_nickname', models.TextField()),
                ('brand', models.TextField(blank=True)),
                ('line', models.TextField(blank=True)),
                ('model', models.TextField(blank=True)),
                ('shipping', models.BooleanField()),
                ('visits_last_month', models.IntegerField(null=True)),
                ('date_retrieved', models.DateTimeField()),
            ],
        ),
        migrations.CreateModel(
            name='Tokens',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('access_token', models.TextField()),
                ('refresh_token', models.TextField()),
                ('expiration_date', models.DateTimeField()),
            ],
        ),
        migrations.CreateModel(
            name='Impresoras',
            fields=[
                ('publicaciondata_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='tablets.publicaciondata')),
            ],
            bases=('tablets.publicaciondata',),
        ),
        migrations.CreateModel(
            name='Notebooks',
            fields=[
                ('publicaciondata_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='tablets.publicaciondata')),
            ],
            bases=('tablets.publicaciondata',),
        ),
        migrations.CreateModel(
            name='PCs',
            fields=[
                ('publicaciondata_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='tablets.publicaciondata')),
            ],
            bases=('tablets.publicaciondata',),
        ),
        migrations.CreateModel(
            name='Tablets',
            fields=[
                ('publicaciondata_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='tablets.publicaciondata')),
            ],
            bases=('tablets.publicaciondata',),
        ),
    ]