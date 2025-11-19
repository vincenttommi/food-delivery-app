from  django.contrib import admin
from django.urls import include,path
from drf_spectacular.views import(SpectacularAPIView,SpectacularRedocView,SpectacularSwaggerView)




urlpatterns = [
    path("api/schema", SpectacularAPIView.as_view(),name="schema"),
     
    #Swagger UI
    path(
        "api/docs/", SpectacularSwaggerView.as_view(url_name="schema"), name="swagger-ui",
    ),

    #Redoc (optional)
    path("api/redoc/", SpectacularRedocView.as_view(url_name="schema"), name="redoc"),
    path("admin/", admin.site.urls),
    path('api/core/', include('core.urls')),
    path('api/menu/', include('menu.urls')),
    path('api/orders/', include('orders')),
    path('api/payments/', include('payments.urls')),
    path('api/delivery/', include('delivery.urls')),
    path('api/feedback/', include('feedback.urls')),
    path('api/chat/', include('messaging.urls')),
    path('api/notifications/', include('notifications.urls')),
    path('api/earnings/',  include('notifications.urls')),
]