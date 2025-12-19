"""Модели works."""
from django.db import models


class Categories(models.Model):
    """Модель для категорий вакансий."""

    name = models.TextField()


class Cities(models.Model):
    """Модель для городов."""

    name = models.TextField()


class Employers(models.Model):
    """Модель для работодателей."""

    name = models.TextField()


class Vacancies(models.Model):
    """Модель для вакансий.

    Содержит название, описание, категорию, работодателя
    город и зарплату.
    """

    name = models.TextField()
    description = models.TextField()
    city = models.ForeignKey(
        Cities,
        on_delete=models.CASCADE,
        related_name='city'
    )
    category = models.ForeignKey(
        Categories,
        on_delete=models.CASCADE,
        related_name='category'
    )
    employer = models.ForeignKey(
        Employers,
        on_delete=models.CASCADE,
        related_name='employer'
    )
    salary_lower = models.IntegerField()
    salary_upper = models.IntegerField()
