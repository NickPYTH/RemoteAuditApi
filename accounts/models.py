from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone


class DocumentStatus(models.Model):
    status = models.CharField(max_length=200, blank=True, null=True, verbose_name="Статус документа")

    def __str__(self):
        return self.status


class Employer(models.Model):
    first_name = models.CharField(max_length=200, blank=True, null=True, verbose_name="Имя")
    surname = models.CharField(max_length=200, blank=True, null=True, verbose_name="Фамилия")
    second_name = models.CharField(max_length=200, blank=True, null=True, verbose_name="Отчество")

    def __str__(self):
        return '{0} {1} {2}'.format(self.first_name, self.surname, self.second_name)


class Company(models.Model):
    company_name = models.CharField(max_length=200, blank=True, null=True, verbose_name="Название")
    company_organization_form = models.CharField(max_length=200, blank=True, null=True,
                                                 verbose_name="Организационно-правовая форма")
    company_location = models.CharField(max_length=200, blank=True, null=True, verbose_name="Адресс")
    company_registration_number = models.CharField(max_length=200, blank=True, null=True,
                                                   verbose_name="Номер свидетельства о государственной регистрации")
    company_licence_registration_date = models.CharField(max_length=200, blank=True, null=True,
                                                         verbose_name="Дата свидетельства о государственной регистрации",
                                                         default=timezone.now())
    company_activities = models.CharField(max_length=200, blank=True, null=True,
                                          verbose_name="Виды деятельности")

    def __str__(self):
        return self.company_name


class AuditorCompany(models.Model):
    auditor_company_name = models.CharField(max_length=200, blank=True, null=True, verbose_name="Название")
    auditor_company_location = models.CharField(max_length=200, blank=True, null=True, verbose_name="Адресс")
    auditor_company_registration_date = models.CharField(max_length=200, blank=True, null=True,
                                                         verbose_name="Дата свидетельства о государственной регистрации",
                                                         )
    auditor_company_registration_number = models.CharField(max_length=200, blank=True, null=True,
                                                           verbose_name="Номер свидетельства о государственной регистрации")
    auditor_company_licence_number = models.CharField(max_length=200, blank=True, null=True,
                                                      verbose_name="Номер лицензии")
    auditor_company_licence_registration_date = models.CharField(max_length=200, blank=True, null=True,
                                                                 verbose_name="Дата предоставлении лицензии")
    auditor_company_licence_licenceOrganisation = models.CharField(max_length=200, blank=True, null=True,
                                                                   verbose_name="Орган выдавший лицензию")
    auditor_company_employers = models.ManyToManyField(Employer, blank=True, null=True,
                                                       verbose_name="Работники аудиторской компании")

    auditor_company_clients_companies = models.ManyToManyField(Company, blank=True, null=True,
                                                               verbose_name="Клиенты аудиторской компании")

    def __str__(self):
        return self.auditor_company_name


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="profile")

    is_employer = models.BooleanField(default=False, verbose_name="Работник")
    employer = models.ForeignKey(Employer, on_delete=models.CASCADE, blank=True, null=True,
                                 verbose_name="Связанный работник")

    is_company = models.BooleanField(default=False, verbose_name="Компания")
    company = models.ForeignKey(Company, on_delete=models.CASCADE, blank=True, null=True,
                                verbose_name="Связанная компания")

    is_auditor_company = models.BooleanField(default=False, verbose_name="Аудиторская компания")
    auditor_company = models.ForeignKey(AuditorCompany, on_delete=models.CASCADE, blank=True, null=True,
                                        verbose_name="Связанная аудиторская компания")

    def __str__(self):
        if self.is_employer:
            return "Пользователь " + self.employer.first_name + " " + self.employer.surname + " " + self.employer.second_name
        elif self.is_company:
            return "Компания " + self.company.company_name
        else:
            return "Аудиторская компания " + self.auditor_company.auditor_company_name


class Document(models.Model):
    name = models.CharField(max_length=200, verbose_name="Наименование документа", blank=True, null=True)
    company = models.ForeignKey(Company, on_delete=models.CASCADE, verbose_name="Документ компании", blank=True, null=True)
    link = models.CharField(max_length=200, verbose_name="Ссылка на файл в хранилище", blank=True, null=True)
    file = models.FileField(upload_to='')
    status = models.ForeignKey(DocumentStatus, on_delete=models.CASCADE, verbose_name="Статус документа", blank=True, null=True)
    comment = models.CharField(max_length=600, blank=True, null=True, verbose_name="Замечания")
    last_edit_date = models.CharField(max_length=200, blank=True, null=True, verbose_name="Последняя дата изменения")
    last_edit_by = models.ForeignKey(Employer, on_delete=models.CASCADE, blank=True, null=True, verbose_name="Кто вносил последнии правки")

    def __str__(self):
        if self.company is not None:
            return self.name + " " + self.company.company_name
        else:
            return self.name + " "


class Invites(models.Model):
    company = models.ForeignKey(Company, on_delete=models.CASCADE, blank=True, null=True)
    auditor = models.ForeignKey(AuditorCompany, on_delete=models.CASCADE, blank=True, null=True)
    code = models.CharField(max_length=100, blank=True, null=True)


class EmployerDocument(models.Model):
    employer = models.ForeignKey(Profile, on_delete=models.CASCADE)
    document = models.ForeignKey(Document, on_delete=models.CASCADE)

    def __str__(self):
        return self.employer.employer.first_name + ' ' + self.employer.employer.surname + ' ' + self.document.name
