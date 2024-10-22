from django.contrib import admin
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from lms.views import *
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from rest_framework import permissions

# schema_view = get_schema_view(
#     openapi.Info(
#         title="Library Management System API",
#         default_version='v1',
#         description="API documentation for Library Management System",
#         contact=openapi.Contact(email="support@library.com"),
#     ),
#     public=True,
#     permission_classes=(permissions.AllowAny,),  # توجه کنید که اینجا از تاپل استفاده شده است
# )

router = DefaultRouter()
router.register(r'books', BookViewSet)
router.register(r'authors', AuthorViewSet)
router.register(r'borrowers', BorrowerViewSet)
router.register(r'reviews', ReviewViewSet)
router.register(r'books/most-borrowed', BookViewSet)


urlpatterns = [
   path('admin/', admin.site.urls),
   path('', include(router.urls)),
   path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
   path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),

   # path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
   # path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),

]




