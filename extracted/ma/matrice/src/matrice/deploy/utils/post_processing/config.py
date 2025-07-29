APP_NAME_TO_USECASE = {
    "people_counting": "people_counting",
    "mask_detection": "mask_detection",
    "vehicle_monitoring": "vehicle_monitoring",
    "weapon_detection" : "weapon_detection",
    "traffic_sign_monitoring" : "traffic_sign_monitoring",
    "flare_analysis" : "flare_analysis",
}

APP_NAME_TO_CATEGORY = {
    "people_counting": "general",
    "mask_detection": "mask_detection",
    "vehicle_monitoring": "traffic",
    "weapon_detection" : "security",
    "traffic_sign_monitoring" : "traffic",
    "flare_analysis" : "flare_detection",
}

def get_usecase_from_app_name(app_name: str) -> str:
    normalized_app_name = app_name.lower().replace(" ", "_").replace("-", "_")
    return APP_NAME_TO_USECASE.get(app_name, APP_NAME_TO_USECASE.get(normalized_app_name))

def get_category_from_app_name(app_name: str) -> str:
    normalized_app_name = app_name.lower().replace(" ", "_").replace("-", "_")
    return APP_NAME_TO_CATEGORY.get(app_name, APP_NAME_TO_CATEGORY.get(normalized_app_name))
