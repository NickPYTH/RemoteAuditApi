from validate_email import validate_email
from rest_framework import serializers
from .models import Profile, Company, AuditorCompany
from django.contrib.auth.models import User
from django.contrib.auth.hashers import check_password, make_password
from django.utils import timezone


class UserProfileSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField(read_only=True)
    def validate(self, attrs):
        request_data = self.context.get('request').data
        if str(request_data.get('type')) == 'company':
            return {'attrs': {
                'type': str(request_data.get('type')),
                'username': str(request_data.get('username')),
                'password': str(request_data.get('password')),
                'email': str(request_data.get('email')),
                'company_name': str(request_data.get('company_name')),
                'company_organization_form': str(request_data.get('company_organization_form')),
                'company_location': str(request_data.get('company_location')),
                'company_registration_number': str(request_data.get('company_registration_number')),
                'company_licence_registration_date': str(request_data.get('company_licence_registration_date')),
                'company_activities': str(request_data.get('company_activities')),
            }}
        elif str(request_data.get('type')) == 'auditor':
            return {'attrs': {
                'type': str(request_data.get('type')),
                'username': str(request_data.get('username')),
                'password': str(request_data.get('password')),
                'email': str(request_data.get('email')),
                'auditor_company_name': str(request_data.get('auditor_company_name')),
                'auditor_company_location': str(request_data.get('auditor_company_location')),
                'auditor_company_registration_date': str(request_data.get('auditor_company_registration_date')),
                'auditor_company_registration_number': str(request_data.get('auditor_company_registration_number')),
                'auditor_company_licence_number': str(request_data.get('auditor_company_licence_number')),
                'auditor_company_licence_registration_date': str(request_data.get('auditor_company_licence_registration_date')),
                'auditor_company_licence_licenceOrganisation': str(request_data.get('auditor_company_licence_licenceOrganisation')),
            }}

    def create(self, validated_data):
        attrs = validated_data.get('attrs')
        if attrs.get('type') == 'company':
            user = User.objects.create(
                username=attrs.get('username'),
                email=attrs.get('email'),
                password=make_password(attrs.get('password')))
            company = Company.objects.create(
                company_name=attrs.get('company_name'),
                company_organization_form=attrs.get('company_organization_form'),
                company_location=attrs.get('company_location'),
                company_registration_number=attrs.get('company_registration_number'),
                company_licence_registration_date=attrs.get('company_licence_registration_date'),
                company_activities=attrs.get('company_activities')
                )
            user_profile = Profile.objects.create(
                user=user,
                is_company=True,
                company=company,
            )
            company.save()
            return user_profile
        elif attrs.get('type') == 'auditor':
            user = User.objects.create(
                username=attrs.get('username'),
                email=attrs.get('email'),
                password=make_password(attrs.get('password')))
            auditorCompany = AuditorCompany.objects.create(
                auditor_company_name=attrs.get('auditor_company_name'),
                auditor_company_location=attrs.get('auditor_company_location'),
                auditor_company_registration_date=attrs.get('auditor_company_registration_date'),
                auditor_company_registration_number=attrs.get('auditor_company_registration_number'),
                auditor_company_licence_number=attrs.get('auditor_company_licence_number'),
                auditor_company_licence_registration_date=attrs.get('auditor_company_licence_registration_date'),
                auditor_company_licence_licenceOrganisation=attrs.get('auditor_company_licence_licenceOrganisation'),
            )
            user_profile = Profile.objects.create(
                user=user,
                is_auditor_company=True,
                auditor_company=auditorCompany,
            )
            auditorCompany.save()
            return user_profile

    class Meta:
        model = Profile
        exclude = []
