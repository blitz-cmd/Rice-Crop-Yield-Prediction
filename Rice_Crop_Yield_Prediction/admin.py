from django.contrib import admin
from Rice_Crop_Yield_Prediction.models import Rice

class RiceAdmin(admin.ModelAdmin):
    list_display=["id","state_name","distict_name","crop_year","season","crop","temperature","precipitation","humidity","area","production"]

admin.site.register(Rice,RiceAdmin)