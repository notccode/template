# Generated by Django 5.1.5 on 2025-01-14 23:33

import datetime
import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Cursos',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('nombre', models.CharField(max_length=100, unique=True)),
                ('descripcion', models.CharField(max_length=500)),
                ('fecha_inicio', models.DateTimeField(default=datetime.datetime.now)),
                ('fecha_fin', models.DateTimeField(blank=True, null=True)),
                ('activo', models.BooleanField(default=True)),
            ],
        ),
        migrations.CreateModel(
            name='Estudiantes',
            fields=[
                ('rut', models.CharField(max_length=12, primary_key=True, serialize=False)),
                ('nombre', models.CharField(max_length=150)),
                ('email', models.EmailField(max_length=200)),
                ('fecha_registro', models.DateTimeField(default=datetime.datetime.now)),
            ],
        ),
        migrations.CreateModel(
            name='Inscripcion',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('fecha_inscripcion', models.DateTimeField(default=datetime.datetime.now)),
                ('curso', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app.cursos')),
                ('estudiante', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app.estudiantes')),
            ],
        ),
    ]