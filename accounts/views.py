import random

from rest_framework.views import APIView
from rest_framework.generics import CreateAPIView, UpdateAPIView, DestroyAPIView
from rest_framework.permissions import IsAuthenticated, AllowAny
from django.contrib.auth.models import User
from rest_framework.response import Response
from validate_email import validate_email
from .models import Profile, Document, DocumentStatus, Invites
from .serializers import UserProfileSerializer


class CreateProfile(CreateAPIView):
    """
    post:
      Создание профиля пользователя
    """
    serializer_class = UserProfileSerializer
    permission_classes = [AllowAny]


class GetProfile(APIView):
    """
    get:
        Получение профиля пользователя
    """
    serializer_class = UserProfileSerializer
    permission_classes = [IsAuthenticated]

    def get(self, request):
        username = self.request.user
        user = User.objects.get(username=username)
        profile = Profile.objects.get(user=user)
        if profile.is_company:
            documents = []
            for document in Document.objects.filter(company=profile.company).all():
                edit_by = 'Абсолютно никто'
                status = DocumentStatus.objects.get(status='in_work').status
                if document.last_edit_by is not None:
                    edit_by = document.last_edit_by.first_name + ' ' + document.last_edit_by.surname
                if document.status is not None:
                    status = document.status.status
                documents.append({
                    'name': document.name,
                    'comment': document.comment,
                    'status': status,
                    'link': document.link,
                    'last_edit_date': document.last_edit_date,
                    'last_edit_by': edit_by
                })
            company_info = {
                'type': 'company',
                'company_name': profile.company.company_name,
                'company_organization_form': profile.company.company_organization_form,
                'company_location': profile.company.company_location,
                'company_registration_number': profile.company.company_registration_number,
                'company_licence_registration_date': profile.company.company_licence_registration_date,
                'company_activities': profile.company.company_activities,
                'company_documents': documents,
                'email': user.email,
            }
            return Response(company_info)
        elif profile.is_auditor_company:
            employers = []
            clients = []

            for employer in profile.auditor_company.auditor_company_employers.all():
                employers.append({
                    'name': employer.first_name,
                    'surname': employer.surname,
                    'second_name': employer.second_name,
                })
            for client in profile.auditor_company.auditor_company_clients_companies.all():
                clients.append({
                    'company_name': client.company_name,
                    'company_location': client.company_location,
                })
            auditor_info = {
                'type': 'auditor',
                'auditor_company_name': profile.auditor_company.auditor_company_name,
                'auditor_company_location': profile.auditor_company.auditor_company_location,
                'auditor_company_registration_date': profile.auditor_company.auditor_company_registration_date,
                'auditor_company_registration_number': profile.auditor_company.auditor_company_registration_number,
                'auditor_company_licence_number': profile.auditor_company.auditor_company_licence_number,
                'auditor_company_licence_registration_date': profile.auditor_company.auditor_company_licence_registration_date,
                'auditor_company_licence_licenceOrganisation': profile.auditor_company.auditor_company_licence_licenceOrganisation,
                'auditor_company_employers': employers,
                'auditor_company_clients_companies': clients,
                'email': user.email,
            }
            return Response(auditor_info)


class GetCompanyDocuments(APIView):
    """
        get:
            Получение списка документов компании
        """
    serializer_class = UserProfileSerializer
    permission_classes = [IsAuthenticated]

    def get(self, request):
        username = self.request.user
        user = User.objects.get(username=username)
        company = Profile.objects.get(user=user).company
        documents = []
        for document in Document.objects.filter(company=company).all():
            edit_by = 'Абсолютно никто'
            status = DocumentStatus.objects.get(status='in_work').status
            if document.status is not None:
                status = document.status.status
            if document.last_edit_by is not None:
                edit_by = document.last_edit_by.first_name + ' ' + document.last_edit_by.surname
            documents.append({
                'name': document.name,
                'comment': document.comment,
                'link': document.link,
                'status': status,
                'last_edit_by': edit_by,
                'last_edit_date': document.last_edit_date
            })

        return Response(documents)


class LoadDocument(APIView):
    serializer_class = UserProfileSerializer
    permission_classes = [IsAuthenticated]

    def post(self, request):
        username = self.request.user
        user = User.objects.get(username=username)
        company = Profile.objects.get(user=user).company
        file = self.request.FILES['file']
        file_name = self.request.POST['name']
        Document.objects.create(file=file, name=file_name, company=company).save()
        return Response('ok')


class CreateInvite(APIView):
    serializer_class = UserProfileSerializer
    permission_classes = [IsAuthenticated]

    def get(self, request):
        username = self.request.user
        user = User.objects.get(username=username)
        company = Profile.objects.get(user=user).company
        code = random.randint(5000, 10000)
        Invites.objects.filter(company=company).all().delete()
        Invites.objects.create(company=company, code=code)
        return Response({'code': code})


class AcceptInvite(APIView):
    serializer_class = UserProfileSerializer
    permission_classes = [IsAuthenticated]

    def post(self, request):
        username = self.request.user
        user = User.objects.get(username=username)
        auditor = Profile.objects.get(user=user).auditor_company
        code = self.request.POST['code']
        invite = Invites.objects.get(code=code)
        invite.auditor = auditor
        invite.save()
        auditor.auditor_company_clients_companies.add(invite.company)
        auditor.save()
        return Response('ok')


class GetCompaniesList(APIView):
    serializer_class = UserProfileSerializer
    permission_classes = [IsAuthenticated]

    def get(self, request):
        username = self.request.user
        user = User.objects.get(username=username)
        companies_list = []
        if Profile.objects.get(user=user).auditor_company is not None:
            companies = Profile.objects.get(user=user).auditor_company.auditor_company_clients_companies.all()
            for company in companies:
                companies_list.append({
                    'name': company.company_name,
                    'location': company.company_location,
                    'activities': company.company_activities,
                    'org_form': company.company_organization_form,
                    'reg_number': company.company_registration_number,
                    'reg_date': company.company_licence_registration_date,
                })
            return Response(companies_list)
        else:
            return Response([])


class GetCompanyDocumentsToAuditor(APIView):
    """
        get:
            Получение списка документов компании
        """
    serializer_class = UserProfileSerializer
    permission_classes = [IsAuthenticated]

    def post(self, request):
        username = self.request.user
        user = User.objects.get(username=username)
        company = Profile.objects.get(user=user).auditor_company.auditor_company_clients_companies.get(company_name=self.request.POST['name'])
        documents = []
        for document in Document.objects.filter(company=company).all():
            edit_by = 'Абсолютно никто'
            status = DocumentStatus.objects.get(status='in_work').status
            if document.status is not None:
                status = document.status.status
            if document.last_edit_by is not None:
                edit_by = document.last_edit_by.first_name + ' ' + document.last_edit_by.surname
            documents.append({
                'name': document.name,
                'comment': document.comment,
                'link': document.link,
                'status': status,
                'last_edit_by': edit_by,
                'last_edit_date': document.last_edit_date
            })

        return Response(documents)


class UpdateDocumentInfo(APIView):
    serializer_class = UserProfileSerializer
    permission_classes = [IsAuthenticated]

    def post(self, request):
        username = self.request.user
        user = User.objects.get(username=username)
        document_name = self.request.POST['document_name']
        if self.request.POST['status'] != 'false':
            status = DocumentStatus.objects.get(status='done')
        else:
            status = DocumentStatus.objects.get(status='in_work')
        document = Document.objects.get(name=document_name)
        document.status = status
        document.comment = self.request.POST['comment']
        document.save()

        return Response('ok')


class DeleteProfile(DestroyAPIView):
    """
    delete:
        Удаление профиля пользователя
    """
    serializer_class = UserProfileSerializer
    permission_classes = [IsAuthenticated]

    def delete(self, request, *args, **kwargs):
        username = self.request.user
        User.objects.get(username=username).delete()
        return Response({
            'status': 'ok'
        })


class UpdateProfile(UpdateAPIView):
    """
    patch:
        Изменение данных профиля пользователя
    """
    serializer_class = UserProfileSerializer
    permission_classes = [IsAuthenticated]

    def patch(self, request, *args, **kwargs):
        user = User.objects.get(username=self.request.user)
        if 'username' in self.request.POST:
            username = self.request.POST['username']
            if len(username.strip()) < 4:
                return Response(status=400, data={
                    'username': 'username is short'
                })
            if len(User.objects.filter(username=username)) != 0:
                return Response(status=400, data={
                    'username': 'username exists'
                })
            user.username = username
        if 'email' in self.request.POST:
            email = self.request.POST['email']
            if not validate_email(email):
                return Response(status=400, data={
                    'email': 'bad email'
                })
            user.email = email
        user.save()
        if 'forms' in self.request.POST:
            user_profile = Profile.objects.get(user=user)
            user_profile.save()
        return Response({
            'status': 'ok'
        })
