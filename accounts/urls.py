from django.urls import path
from .views import GetCompanyDocumentsToAuditor, GetCompaniesList, CreateProfile, GetProfile, UpdateProfile, \
    DeleteProfile, GetCompanyDocuments, LoadDocument, AcceptInvite, CreateInvite, UpdateDocumentInfo

urlpatterns = [
    path("create-profile", CreateProfile.as_view(), name="create-profile"),
    path("get-profile", GetProfile.as_view(), name="get-profile"),
    path("update-profile", UpdateProfile.as_view(), name="update-profile"),
    path("delete-profile", DeleteProfile.as_view(), name="delete-profile"),
    path("get-company-documents", GetCompanyDocuments.as_view()),
    path("load-document", LoadDocument.as_view()),
    path("create-invite", CreateInvite.as_view()),
    path("accept-invite", AcceptInvite.as_view()),
    path("get-companies-list", GetCompaniesList.as_view()),
    path("get-company-documents-to-auditor", GetCompanyDocumentsToAuditor.as_view()),
    path("update-document-info", UpdateDocumentInfo.as_view())
]
